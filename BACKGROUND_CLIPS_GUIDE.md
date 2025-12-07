# Background Clips Guide

This guide helps you find and download free gameplay videos for your brain-rot-bot.

## 🎮 Recommended Sources

### 1. **Pexels** (Recommended - Free & Legal)
- **URL**: https://www.pexels.com/videos/
- **Why**: Free stock videos, no attribution required
- **Search terms**: 
  - "minecraft parkour"
  - "subway surfer"
  - "gameplay vertical"
  - "mobile game"
- **How to use**:
  1. Get free API key: https://www.pexels.com/api/
  2. Run: `python scripts/download_backgrounds.py --source pexels --query "minecraft parkour"`

### 2. **Pixabay** (Free Stock Videos)
- **URL**: https://pixabay.com/videos/
- **Why**: Free videos, simple license
- **Search**: "minecraft", "subway surfer", "parkour"
- **Note**: Manual download required

### 3. **YouTube** (Your Own Content or Creative Commons)
- **Why**: Large selection
- **Important**: Only download videos you own or have permission to use
- **How to use**:
  ```bash
  # Install yt-dlp first
  pip install yt-dlp
  # Or: brew install yt-dlp
  
  # Download specific video
  python scripts/download_backgrounds.py --source youtube --url "https://youtube.com/watch?v=..." --duration 30
  ```

### 4. **Record Your Own**
- Use screen recording tools:
  - **macOS**: QuickTime Player (built-in)
  - **Windows**: OBS Studio (free)
  - **Mobile**: Built-in screen recording
- Record vertical format (9:16) for best results

## 📥 Quick Setup

### Option 1: Use the Download Script

```bash
# Install yt-dlp for YouTube downloads
pip install yt-dlp

# Download from Pexels (requires free API key)
python scripts/download_backgrounds.py --source pexels --query "minecraft parkour"

# Download from YouTube (your own videos)
python scripts/download_backgrounds.py --source youtube --url "YOUR_VIDEO_URL" --duration 30
```

### Option 2: Manual Download

1. **Find videos** on Pexels or Pixabay
2. **Download** in vertical format (1080x1920 or similar)
3. **Place** in `assets/background_clips/`
4. **Supported formats**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`

## 🎯 Video Requirements

- **Format**: Vertical (9:16 aspect ratio)
- **Resolution**: 1080x1920 (ideal) or similar
- **Duration**: 10-60 seconds (will be looped automatically)
- **Content**: Gameplay footage (Minecraft, Subway Surfer, etc.)
- **Quality**: Clear, not too busy (subtitles will overlay)

## 🔍 Search Tips

### For Minecraft Parkour:
- Search: "minecraft parkour", "minecraft gameplay", "minecraft speedrun"
- Look for: First-person parkour, smooth movement

### For Subway Surfer:
- Search: "subway surfer gameplay", "subway surfer mobile"
- Look for: Side-scrolling gameplay, colorful visuals

### For Other Games:
- Geometry Dash
- Temple Run
- Any vertical mobile game footage

## ⚖️ Legal Notes

- ✅ **OK**: Your own gameplay recordings
- ✅ **OK**: Free stock videos (Pexels, Pixabay)
- ✅ **OK**: Creative Commons licensed videos
- ❌ **NOT OK**: Copyrighted gameplay without permission
- ❌ **NOT OK**: Downloading from YouTube without permission

## 🚀 Quick Start

1. **Get Pexels API key** (free): https://www.pexels.com/api/
2. **Run download script**:
   ```bash
   python scripts/download_backgrounds.py --source pexels --query "minecraft parkour"
   ```
3. **Videos will be saved** to `assets/background_clips/`
4. **Test it**:
   ```bash
   python main.py --text "Test video" --voice meme-boy
   ```

## 📝 Example Commands

```bash
# Download 5 Minecraft parkour videos from Pexels
python scripts/download_backgrounds.py --source pexels --query "minecraft parkour"

# Download specific YouTube video (30 second clip)
python scripts/download_backgrounds.py --source youtube --url "https://youtube.com/watch?v=..." --start-time 10 --duration 30

# Download Subway Surfer videos
python scripts/download_backgrounds.py --source pexels --query "subway surfer gameplay"
```

---

**Note**: The bot will automatically select a random clip from `assets/background_clips/` if multiple videos are available. If no clips are found, it will use a black background.

