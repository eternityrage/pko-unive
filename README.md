# 🦜 Picko Universe - Social Media Video Automation Pipeline

Automated video processing and social media publishing pipeline for **Picko Universe**, featuring the hilarious antics of **Picko the Parrot**. Fetches videos from Google Drive, upscales them, removes watermarks, and publishes to multiple social media platforms with engaging, AI-generated captions.

## 🚀 Features

- **Google Drive Integration**: Automatically fetch parrot videos from your Google Drive folder
- **Smart Video Processing**:
  - Upscale to 1080x1920 (vertical format for Reels/Shorts/TikTok)
  - Watermark removal (bottom-right corner)
  - Video enhancement (sharpening + clarity boost)
  - Audio enhancement (normalize volume + improve parrot squawks!)
- **AI-Powered Captions**: Auto-generated captions with:
  - Funny and chaotic parrot-focused content
  - Strong calls-to-action (CTAs)
  - Engagement drivers (likes, follows, comments)
  - Relevant parrot and animal hashtags
- **Multi-Platform Upload**:
  - Instagram Reels & Stories
  - Facebook Reels & Stories
  - Threads
  - YouTube Shorts

## 🎯 Channel Profile

**Picko Universe** - Featuring Picko the Parrot
- The smartest (and funniest) green parrot on the internet
- Daily doses of chaos, clever tricks, and adorable moments
- Dedicated to making you smile through animal humor
- Focus on community building and engagement

## 🔄 Automation Workflow

```
Google Drive (Picko Universe Videos folder)
        ↓
Fetch new video
        ↓
Process (upscale + enhance + watermark removal)
        ↓
Generate AI caption with CTAs (Funny & Impressive)
        ↓
Upload to all platforms
        ↓
Mark as published
```

## 📋 Prerequisites

1. **Python 3.8+**
2. **FFmpeg** installed and in PATH
3. **Google Cloud Project** with Drive API enabled
4. **Google Service Account** credentials
5. **Social Media API Credentials** (Instagram, Facebook, YouTube, etc.)

## 🔧 Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

**Windows:**
```bash
# Using winget
winget install FFmpeg

# Or download from https://ffmpeg.org/download.html
```

**Linux:**
```bash
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

### 3. Configure Google Drive (ONE TIME SETUP)

Follow the detailed guide in **[GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md)**

**Quick Setup:**

**Step A: Create Google Cloud Project**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (e.g., "Elira Zvenova Bot")

**Step B: Enable Drive API & Create Service Account**
1. Enable Google Drive API
2. Create a service account
3. Download JSON key file → Save as `credentials/google_credentials.json`

**Step C: Share Your Drive Folder**
1. Get your Google Drive folder ID from the URL
2. Share the folder with the service account email
3. Give it "Viewer" access

**Step D: Update .env**
```env
GOOGLE_DRIVE_FOLDER_ID=your-folder-id-here
GOOGLE_SERVICE_ACCOUNT_KEY=credentials/google_credentials.json
LOCAL_INPUT_DIR=Videos
```

### 4. Configure Social Media Credentials

Edit the `.env` file with your API credentials:

```env
# Instagram
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_ACCOUNT_ID=

# Facebook
FACEBOOK_ACCESS_TOKEN=
FACEBOOK_PAGE_ID=

# YouTube
YT_CLIENT_ID=
YT_CLIENT_SECRET=
YT_REFRESH_TOKEN=

# Threads
THREADS_ACCESS_TOKEN=
THREADS_USER_ID=

# AI Caption Generation
POLLINATIONS_API_KEY=
AI_MODEL=openai
```

### 5. Prepare Your Google Drive Folder

Create a folder structure like this in Google Drive:

```
Picko Universe Videos/
├── picko_funny_001.mp4
├── picko_talking_002.mp4
├── picko_dance_003.mp4
└── ...
```

The automation will:
- Fetch one video at a time
- Process it
- Upload to all platforms
- Track published videos to avoid duplicates

## 📁 Folder Structure

```
.
├── Videos/                 # Input folder (videos from Google Drive)
├── Processed_Videos/       # Processed videos (upscaled, extended, enhanced)
├── Published_Videos/       # Already published videos (archived)
├── credentials/            # Google service account JSON key
│   └── google_credentials.json
├── google_drive_fetch.py   # Google Drive integration
├── process_videos.py       # Video processing (extend + upscale + enhance)
├── daily_publisher.py      # Social media uploader with AI captions
├── auto_pipeline.py        # Main automation script
├── .env                    # Environment variables (API keys)
├── GOOGLE_DRIVE_SETUP.md   # Detailed Google Drive setup guide
└── requirements.txt        # Python dependencies
```

## 🎯 Usage

### Run the Complete Pipeline

```bash
python auto_pipeline.py
```

This will:
1. Fetch ONE new video from Google Drive
2. Check duration and extend if needed (6s → 12s)
3. Process the video (upscale + enhance + watermark removal)
4. Generate AI caption with CTAs
5. Upload to all social media platforms
6. Mark as published and archive

### Individual Steps

**Fetch from Google Drive only:**
```bash
python google_drive_fetch.py
```

**Process videos only:**
```bash
python process_videos.py
```

**Publish to social media only:**
```bash
python daily_publisher.py path/to/processed_video.mp4
```

## ⚙️ Customization

### Video Extension Threshold

Edit `process_videos.py` to change the duration threshold:

```python
# Currently extends videos ≤ 6.5 seconds
needs_looping = duration is not None and duration <= 6.5
```

### Watermark Position

Edit `process_videos.py` to adjust watermark removal area:

```python
# Adjust these values based on your watermark size/position
w_delogo = 180  # Width of watermark area
h_delogo = 80   # Height of watermark area
x_delogo = 1080 - w_delogo - 5  # Position from right
y_delogo = 1920 - h_delogo - 5  # Position from bottom
```

### Caption Generation

Edit the `generate_caption()` function in `daily_publisher.py` to customize:
- Dance styles/vibes
- Call-to-action messages
- Hashtag strategy
- AI model parameters

## 🎬 Video Processing Details

### For 6-Second Videos (Auto-Extended)

```
Original: 6 seconds
    ↓
Loop twice (concatenate)
    ↓
Result: 12 seconds
    ↓
Enhance:
- Upscale to 1080x1920
- Sharpening + clarity boost
- Watermark removal
- Audio normalization
```

### For Longer Videos

```
Original: >6 seconds
    ↓
Keep original length
    ↓
Enhance:
- Upscale to 1080x1920
- Sharpening + clarity boost
- Watermark removal
- Audio normalization
```

## 🛠️ Troubleshooting

### FFmpeg not found
Ensure FFmpeg is installed and in your system PATH.

### Google Drive connection error
- Verify `GOOGLE_DRIVE_FOLDER_ID` is correct
- Check that service account has access to the folder
- Ensure `credentials/google_credentials.json` exists

### "No videos found in Google Drive folder"
- Make sure videos are in MP4, MOV, AVI, or MKV format
- Verify the folder is shared with the service account
- Check that the folder ID is correct (from URL after `/folders/`)

### Upload failures
Check that all API tokens in `.env` are valid and haven't expired.

### Caption generation fails
- Verify `POLLINATIONS_API_KEY` is set
- Check API quota limits
- Fallback captions are used if AI fails

## 📝 Notes

- Videos are processed one at a time to avoid rate limits
- Already processed videos are tracked in `published_videos.json`
- Original audio is preserved and enhanced
- Processing time varies based on video length and quality
- 6-second videos are automatically extended to 12 seconds

## 🚨 Important

- Keep your `.env` file private (add to `.gitignore`)
- Never commit API tokens to GitHub
- Test with a single video before running bulk operations
- Back up your Google Drive folder regularly

## 🎉 What's New

### ✅ Changes in This Version

1. **Brand Rebrand**: Changed from "Elira Zvenova" to "Picko Universe" - Featuring Picko the Parrot
2. **Metadata Evolution**: Dynamic, funny, and impressive title/description generation for every post
3. **Parrot-Specific Tags**: Optimized hashtags and tags for the funny animal/parrot niche
4. **Enhanced AI Prompt**: Better context for generating chaotic and adorable parrot content
5. **Robust Fallbacks**: A large set of funny fallback captions for instant publishing

### 📚 Documentation

- **[GOOGLE_DRIVE_SETUP.md](GOOGLE_DRIVE_SETUP.md)** - Complete Google Drive setup guide
- **[README.md](README.md)** - This file (you are here)
- **[WORKFLOW.md](WORKFLOW.md)** - Detailed workflow documentation

## 💡 Tips for Best Results

1. **Upload consistent video quality** to Google Drive for best processing results
2. **Use clear, well-lit videos** for better AI caption generation
3. **Monitor first few uploads** to ensure quality meets your standards
4. **Engage with comments** to boost algorithm performance
5. **Post consistently** for better audience retention

---

**Made with 🦜 for Picko Universe - Where every squawk tells a story**
