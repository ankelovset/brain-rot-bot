# 🚀 Quick Start Guide

Get up and running with Brain Rot Bot in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set API Key

```bash
export OPENAI_API_KEY="your-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-key-here
```

## 3. Add Background Clips

Place gameplay videos in `assets/background_clips/`:
- Minecraft parkour
- Subway Surfer
- Geometry Dash
- Any vertical gameplay footage

## 4. Create Your First Video

```bash
# Using the example script
python main.py --script scripts/todo/example_script.txt --voice meme-boy

# Or with inline text
python main.py --text "Your script here" --voice sigma-narrator
```

## 5. Check Output

Your video will be in `renders/YYYY-MM-DD/render_TIMESTAMP.mp4`

## Next Steps

- Add more scripts to `scripts/todo/` for batch processing
- Try different voices: `meme-boy`, `sigma-narrator`, `uwu`, `deep-epic`
- Enable karaoke subtitles: `--style karaoke`
- Run automation mode: `python main.py --automation`

## Troubleshooting

**"No module named 'moviepy'"**
→ Run `pip install -r requirements.txt`

**"OpenAI API key required"**
→ Set `OPENAI_API_KEY` environment variable

**"No background clips found"**
→ Add video files to `assets/background_clips/`

**Video rendering is slow**
→ This is normal for first render. Subsequent renders are faster.

---

Happy brain rotting! 🧠

