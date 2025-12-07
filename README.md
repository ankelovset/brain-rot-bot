# 🧠 Brain Rot Bot - Automated TikTok/Shorts Video Generator

A fully automated pipeline that generates viral-style TikTok/YouTube Shorts/Instagram Reels from text scripts, complete with:
- **Text-to-Speech (TTS)** audio with word-accurate timestamps
- **Synced subtitles** (SRT or karaoke-style ASS)
- **Vertical format** videos (1080×1920)
- **Minecraft/Subway Surfer** background gameplay loops
- **Multiple meme TTS voices**
- **Full automation** mode for batch processing

## 🎯 Features

- ✅ **Modular Architecture**: Clean, extensible Python modules
- ✅ **Multiple TTS Providers**: OpenAI TTS or ElevenLabs
- ✅ **Word-Accurate Timestamps**: Perfect subtitle synchronization
- ✅ **Karaoke Subtitles**: Optional word-by-word highlighting
- ✅ **Auto Background Selection**: Random gameplay clips with smart cropping
- ✅ **Meme Voice Profiles**: Pre-configured voices (meme-boy, sigma-narrator, uwu, deep-epic)
- ✅ **Automation Mode**: Process multiple scripts from a folder
- ✅ **CLI Interface**: Easy-to-use command-line tool

## 📁 Project Structure

```
brain-rot-bot/
├── main.py                 # CLI entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
│
├── tts/                   # Text-to-Speech modules
│   ├── openai_tts.py
│   ├── elevenlabs_tts.py
│   └── tts_router.py
│
├── subtitles/             # Subtitle generation
│   ├── srt_generator.py
│   ├── ass_karaoke.py
│   └── subtitle_utils.py
│
├── video/                 # Video composition
│   ├── background_selector.py
│   ├── compositor.py
│   ├── render.py
│   └── utils.py
│
├── assets/
│   ├── background_clips/  # Put your gameplay videos here
│   ├── fonts/
│   └── overlays/
│
├── scripts/
│   ├── todo/              # Place .txt scripts here for automation
│   └── processed/
│
├── renders/               # Generated videos
└── logs/                  # Log files
```

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ankelovset/brain-rot-bot.git
   cd brain-rot-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys:**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   # OR for ElevenLabs:
   export ELEVENLABS_API_KEY="your-elevenlabs-api-key"
   ```

4. **Add background clips:**
   - Place your gameplay videos (Minecraft, Subway Surfer, etc.) in `assets/background_clips/`
   - Supported formats: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`

## 💻 Usage

### Basic Usage

**Process a script file:**
```bash
python main.py --script my_script.txt --voice meme-boy
```

**Process inline text:**
```bash
python main.py --text "This is my script text" --voice sigma-narrator --style karaoke
```

**Use a specific background clip:**
```bash
python main.py --script script.txt --background assets/background_clips/minecraft.mp4
```

### Voice Profiles

Available meme voices:
- `meme-boy` - High-energy, fast-paced
- `sigma-narrator` - Deep, authoritative
- `uwu` - Cute, high-pitched
- `deep-epic` - Epic, dramatic

### Subtitle Styles

- `standard` - Standard SRT subtitles (default)
- `karaoke` - ASS format with word-by-word highlighting

### Automation Mode

1. Place `.txt` script files in `scripts/todo/`
2. Run automation mode:
   ```bash
   python main.py --automation
   ```
3. Videos will be generated in `renders/YYYY-MM-DD/`
4. Processed scripts moved to `scripts/processed/`

## ⚙️ Configuration

Edit `config.py` to customize:
- TTS provider and voices
- Subtitle styling (font size, colors, position)
- Video output settings (resolution, FPS, bitrate)
- Background clip selection behavior

## 📝 Script Format

Scripts should be plain text files (`.txt`). The bot will:
1. Convert text to speech
2. Generate word-level timestamps
3. Create synced subtitles
4. Compose with background gameplay
5. Export as vertical video (1080×1920)

Example script:
```
Did you know that if you eat a banana, you're technically eating a berry? 
But a strawberry? That's not even a berry. The world is a lie.
```

## 🎬 Output

Each render produces:
- `render_TIMESTAMP.mp4` - Final video
- `render_TIMESTAMP.mp3` - Audio file
- `render_TIMESTAMP.srt` or `.ass` - Subtitles
- `render_TIMESTAMP_timestamps.json` - Word timestamps
- `render_TIMESTAMP_metadata.json` - Render metadata

## 🔧 Advanced Usage

### Custom Configuration

Modify `config.py` to add custom voice profiles:

```python
meme_voices: Dict[str, Dict[str, Any]] = {
    "custom-voice": {
        "voice": "nova",
        "speed": 1.0,
        "pitch": 1.0
    }
}
```

### Programmatic Usage

```python
from video.render import render_video
from config import config

video_path, metadata = render_video(
    script_text="Your script here",
    output_dir=Path("renders/2024-01-01"),
    voice_profile="meme-boy",
    subtitle_style="karaoke"
)
```

## 🐛 Troubleshooting

**"No word timestamps provided"**
- Ensure your OpenAI API key has access to Whisper API
- Check that the TTS generation completed successfully

**"No background clips found"**
- Add video files to `assets/background_clips/`
- Supported formats: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`

**Video rendering is slow**
- Reduce video bitrate in `config.py`
- Use lower resolution or FPS for testing
- Ensure ffmpeg is properly installed

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a pull request.

## ⚠️ Notes

- Requires ffmpeg for video processing (usually installed with MoviePy)
- OpenAI API usage will incur costs
- Background clips should be high quality for best results
- First run may be slower due to model downloads

---

**Made with ❤️ for generating brain rot content**
