import os
import json
import glob
import random
import requests
import shutil
import sys
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
from pathlib import Path
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Import upload functions
try:
    from upload.upload_instagram import upload_to_instagram
    from upload.upload_threads import upload_to_threads
    from upload.upload_facebook import upload_to_facebook, upload_to_facebook_story
    from upload.upload_to_youtube import upload_to_youtube
except ImportError as e:
    print(f"Error importing upload modules: {e}")
    # Still want to proceed or stop?
    pass

PROCESSED_DIR = "Processed_Videos"
PUBLISHED_LOG = "published_videos.json"

def get_already_published():
    if os.path.exists(PUBLISHED_LOG):
        with open(PUBLISHED_LOG, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def get_repost_counts():
    """Count how many times each video has been posted."""
    published = get_already_published()
    counts = {}
    for entry in published:
        vname = entry.get("video_name", "")
        counts[vname] = counts.get(vname, 0) + 1
    return counts

def mark_as_published(video_name, metadata):
    published = get_already_published()
    published.append({
        "video_name": video_name,
        "metadata": metadata
    })
    with open(PUBLISHED_LOG, 'w', encoding='utf-8') as f:
        json.dump(published, f, indent=4)

def select_video(specific_video=None):
    published = [item["video_name"] for item in get_already_published()]
    all_videos = sorted(glob.glob(os.path.join(PROCESSED_DIR, "*.mp4")))

    if specific_video:
        # specific_video might be a full path or just a filename
        if os.path.exists(specific_video):
            # It's a full path
            vid_path = specific_video
            name = os.path.basename(specific_video)
        else:
            # It's just a filename, join with PROCESSED_DIR
            vid_path = os.path.join(PROCESSED_DIR, specific_video)
            name = specific_video

        if os.path.exists(vid_path):
            if name in published:
                post_count = sum(1 for p in published if p == name)
                print(f"🔄 Video {name} was already published ({post_count}x) - Re-publishing (recycling)")
            return vid_path, name
        else:
            print(f"❌ Error: Specific video {name} not found")
            return None, None

    # Find unpublished videos first
    unpublished = [(vid, os.path.basename(vid)) for vid in all_videos if os.path.basename(vid) not in published]

    if unpublished:
        vid, name = unpublished[0]
        return vid, name

    # All videos published - use weighted random selection (less posted = more likely)
    if all_videos:
        repost_counts = get_repost_counts()
        weights = []
        for vid in all_videos:
            name = os.path.basename(vid)
            count = repost_counts.get(name, 0)
            weight = max(1, 1000 // (3 ** min(count, 6)))
            weights.append(weight)

        selected_vid = random.choices(all_videos, weights=weights, k=1)[0]
        name = os.path.basename(selected_vid)
        post_count = repost_counts.get(name, 0)
        print(f"🎲 All videos published. Weighted random reuse (posted {post_count}x): {name}")
        return selected_vid, name

    return None, None

def generate_caption():
    import random
    import time

    api_key = os.getenv("POLLINATIONS_API_KEY")
    model = os.getenv("AI_MODEL", "openai")

    fallback_titles = [
        "Picko the Parrot: Chaotic Morning! 🦜",
        "When Picko Thinks He's the Boss... 😂",
        "Picko's Funniest Moments: Green and Mean!",
        "Meet Picko: The Smartest (and Funniest) Parrot! 🌟",
        "Picko's Daily Dose of Chaos 🦜✨",
        "You Won't Believe What Picko Did Today!",
        "Picko the Parrot: The Ultimate Prankster",
        "Parrot Life: Picko's Hilarious Antics",
        "Picko Universe: Where Parrots Rule the House!",
        "That Parrot Stare... Picko is Planning Something!",
        "Picko vs. The Human: The Battle for Snacks 🍎",
        "The Secret Life of Picko the Parrot",
        "Picko's Morning Routine (It's Pure Madness)",
        "Parrot Wisdom by Picko 🦜",
        "Picko Universe: Daily Dose of Cute and Chaotic",
    ]

    fallback_descriptions = [
        "Welcome to Picko Universe! 🦜 Watch our favorite green parrot, Picko, as he takes over the house with his hilarious antics and adorable personality. From morning chaos to bedtime chats, there's never a dull moment with Picko around. If you love birds and funny animal moments, this is the place for you! Don't forget to like and follow for more daily parrot fun! 🌟 #parrot #funnyparrot #pickouniverse #greenparrot #funnyanimals #birds #talkingparrot #parrotlife #cutebirds #animalhumor #shorts #reels",
        "Picko is at it again! 😂 This cheeky green parrot has a mind of his own and a personality that's larger than life. Today's mission? Complete house domination! Watch until the end to see his funniest move yet. Picko Universe is dedicated to bringing you the best and most impressive parrot moments. Drop a comment if Picko made you smile today! 🦜✨ #parrot #funnyparrot #pickouniverse #greenparrot #funnyanimals #birds #talkingparrot #parrotlife #cutebirds #animalhumor #shorts #reels",
        "They say parrots are smart, but Picko is on another level! 🧠 Watch him outsmart his humans once again. Whether he's 'talking' back or finding new ways to get treats, Picko is the true star of the house. We hope this video makes your day a little brighter! Share this with a fellow bird lover! 🦜💚 #parrot #funnyparrot #pickouniverse #greenparrot #funnyanimals #birds #talkingparrot #parrotlife #cutebirds #animalhumor #shorts #reels",
        "Living with a parrot means never having a quiet moment — and we wouldn't have it any other way! 🦜 Picko is the heart of Picko Universe, and his energy is contagious. Just look at those feathers and that mischievous glint in his eye! Like if you think Picko is the cutest parrot on the internet! ⭐ #parrot #funnyparrot #pickouniverse #greenparrot #funnyanimals #birds #talkingparrot #parrotlife #cutebirds #animalhumor #shorts #reels",
        "Is it a bird? Is it a plane? No, it's Picko the Parrot causing trouble again! 🎭 From hilarious dances to unexpected squawks, Picko knows exactly how to get all the attention. Follow Picko Universe for your daily dose of green parrot chaos! What's the funniest thing your pet has ever done? Comment below! 👇 #parrot #funnyparrot #pickouniverse #greenparrot #funnyanimals #birds #talkingparrot #parrotlife #cutebirds #animalhumor #shorts #reels",
    ]

    if not api_key:
        chosen_title = random.choice(fallback_titles)
        chosen_desc = random.choice(fallback_descriptions)
        print("Warning: POLLINATIONS_API_KEY not found. Using fallback captions.")
        return chosen_title, chosen_desc

    vibes = [
        "cheeky and mischievous — focus on Picko's pranks and funny attitude",
        "adorable and wholesome — capture the sweet and loving side of our green friend",
        "energetic and chaotic — highlight the high-energy parrot madness",
        "curious and clever — show off how smart (and sneaky) Picko can be",
        "funny and relatable — make it about the 'struggles' of living with a parrot",
        "surprised and impressed — focus on Picko's amazing tricks and talking abilities",
        "sassy and dramatic — highlight Picko's big personality and dramatic reactions",
    ]
    chosen_vibe = random.choice(vibes)

    prompt = (
        f"Write a completely unique, funny, and impressive title and description for a short video of a "
        f"funny green parrot named Picko for the Facebook page 'Picko Universe'. "
        f"The page features Picko's hilarious antics, clever tricks, and chaotic parrot life. "
        f"Speak as the page admin — energetic, funny, and absolutely parrot-obsessed. "
        f"Make the vibe {chosen_vibe}. "
        f"The description should be engaging (3-5 sentences), realistic, and full of personality. "
        f"Include engagement calls-to-action such as: "
        f"- Like if Picko made you laugh! "
        f"- Comment your favorite parrot moment! "
        f"- Share this with someone who needs a smile! "
        f"- Follow Picko Universe for more daily parrot chaos! "
        f"Include relevant hashtags in ALL LOWERCASE such as #parrot #funnyparrot #pickouniverse #greenparrot #funnyanimals #birds #talkingparrot #parrotlife #cutebirds #animalhumor #shorts #reels. "
        f"Return ONLY a valid JSON object in this format: {{\"title\": \"<title>\", \"description\": \"<description>\"}} "
        f"Do not include any other text or markdown block backticks."
    )

    url = "https://gen.pollinations.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.9,
        "seed": random.randint(1, 999999)
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        content = data.get('choices', [{}])[0].get('message', {}).get('content', '')

        content = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(content)

        chosen_title = random.choice(fallback_titles)
        chosen_desc = random.choice(fallback_descriptions)
        return result.get("title", chosen_title), result.get("description", chosen_desc)
    except Exception as e:
        print(f"Error generating caption: {e}")
        return random.choice(fallback_titles), random.choice(fallback_descriptions)

def main():
    print("=" * 60)
    print("🚀 DAILY AUTOMATION STARTING")
    print("=" * 60)
    
    specific_video = sys.argv[1] if len(sys.argv) > 1 else None
    video_path, video_name = select_video(specific_video)
    if not video_path:
        print("✅ No new videos found to publish. Exiting.")
        return
        
    print(f"👉 Selected Video: {video_name}")
    print("🧠 Generating caption via Pollination AI...")
    title, description = generate_caption()
    
    print(f"📝 Title: {title}")
    print(f"📝 Description:\n{description}")
    
    # Combined caption for platforms that use a single text field
    combined_caption = f"{title}\n\n{description}"
    
    success_flags = {
        "instagram_reel": False,
        "instagram_story": False,
        "facebook_reel": False,
        "facebook_story": False,
        "threads": False,
        "youtube": False
    }
    
    # Instagram Reels
    try:
        result = upload_to_instagram(video_path, combined_caption, is_story=False)
        if result and result.get('status') == 'skipped':
            print(f"⚠️  Instagram Reel: Skipped ({result.get('reason', 'No credentials')})")
        else:
            success_flags["instagram_reel"] = True
    except Exception as e:
        print(f"❌ Instagram Reel upload failed: {e}")
        
    # Instagram Stories
    try:
        result = upload_to_instagram(video_path, combined_caption, is_story=True)
        if result and result.get('status') == 'skipped':
            print(f"⚠️  Instagram Story: Skipped ({result.get('reason', 'No credentials')})")
        else:
            success_flags["instagram_story"] = True
    except Exception as e:
        print(f"❌ Instagram Story upload failed: {e}")
        
    # Facebook Reels
    try:
        result = upload_to_facebook(video_path, description, title=title)
        if result and result.get('status') == 'skipped':
            print(f"⚠️  Facebook Reel: Skipped ({result.get('reason', 'No credentials')})")
        else:
            success_flags["facebook_reel"] = True
    except Exception as e:
        print(f"❌ Facebook Reel upload failed: {e}")
        
    # Facebook Stories
    try:
        result = upload_to_facebook_story(video_path)
        if result and result.get('status') == 'skipped':
            print(f"⚠️  Facebook Story: Skipped ({result.get('reason', 'No credentials')})")
        else:
            success_flags["facebook_story"] = True
    except Exception as e:
        print(f"❌ Facebook Story upload failed: {e}")
        
    # Threads
    try:
        result = upload_to_threads(video_path, combined_caption)
        if result and result.get('status') == 'skipped':
            print(f"⚠️  Threads: Skipped ({result.get('reason', 'No credentials')})")
        else:
            success_flags["threads"] = True
    except Exception as e:
        print(f"❌ Threads upload failed: {e}")
        
    # YouTube Shorts
    try:
        upload_to_youtube(video_path, title, description, tags=["parrot", "funnyparrot", "pickouniverse", "greenparrot", "funnyanimals", "birds", "talkingparrot", "parrotlife", "cutebirds", "animalhumor", "shorts", "reels"])
        success_flags["youtube"] = True
    except Exception as e:
        print(f"❌ YouTube upload failed: {e}")
        
    # Record as published regardless of partial success,
    # to avoid repeating the same video. Alternatively, only record if fully successful.
    print("\n✅ Marking video as published.")
    
    # Check if this is a recycled video (already in published_videos.json)
    published_list = get_already_published()
    is_recycled = any(item["video_name"] == video_name for item in published_list)
    
    if is_recycled:
        print(f"   🔄 This is a recycled video (re-publishing)")
    
    mark_as_published(video_name, {
        "title": title,
        "description": description,
        "success_flags": success_flags,
        "recycled": is_recycled
    })
    
    # Move the published video to Published_Videos folder
    published_dir = "Published_Videos"
    if not os.path.exists(published_dir):
        os.makedirs(published_dir)
        
    try:
        dest_path = os.path.join(published_dir, video_name)
        shutil.move(video_path, dest_path)
        print(f"📦 Moved published video to {dest_path}")
    except Exception as e:
        print(f"❌ Failed to move published video: {e}")
    
    print("🎉 DAILY AUTOMATION COMPLETE")

if __name__ == "__main__":
    main()
