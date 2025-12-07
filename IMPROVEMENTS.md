# Recent Improvements

## 🎯 Improved Audio-Subtitle Synchronization

### Problem
The original timestamp estimation for ElevenLabs TTS was inaccurate, causing subtitles to be out of sync with the audio.

### Solution
1. **Whisper API Integration**: Now uses OpenAI Whisper API to get accurate word-level timestamps for ElevenLabs audio (same as OpenAI TTS)
2. **Improved Fallback Estimation**: Enhanced the estimation algorithm with:
   - Vowel-based timing adjustments (words with more vowels take longer)
   - Better punctuation handling (longer pauses for sentence endings)
   - Word length adjustments (longer words have proportionally less time per character)
   - Duration normalization to prevent drift

### How It Works
- **Primary Method**: Uses Whisper API to transcribe the generated audio and extract word-level timestamps
- **Fallback**: If Whisper fails or OpenAI key unavailable, uses improved estimation algorithm
- **Result**: Much more accurate subtitle synchronization

### Usage
No changes needed! The improvement is automatic. Just generate videos as before:
```bash
python3 main.py --text "Your script" --voice meme-boy
```

## 🎮 Interactive CLI

### New Feature
Added an interactive command-line interface that guides you through video generation step-by-step.

### Usage
```bash
python3 main.py --interactive
# or
python3 main.py -i
```

### What It Does
1. **Prompts for Script Text**: Enter your script (multi-line supported)
2. **Select Background Video**: Choose from available videos or use black background
3. **Choose Voice Profile**: Select from available meme voices
4. **Configure Subtitles**: Choose standard or karaoke style
5. **Set Output Directory**: Use default or specify custom path
6. **Confirm & Generate**: Review settings and start generation

### Example Session
```
🧠 Brain Rot Bot - Interactive Video Generator
============================================================

📝 Enter your script text:
   (Press Enter twice or Ctrl+D when done)

Did you know that bananas are berries?
But strawberries aren't!

✅ Text received (58 characters)

🎬 Select background video:
   0. Use black background (no video)
   1. minecraft_parkour.mp4
   2. subway_surfer.mp4

   Enter choice (0-2): 1
✅ Selected: minecraft_parkour.mp4

🎤 Select voice profile:
   0. Default voice
   1. meme-boy (nova)
   2. sigma-narrator (onyx)
   ...

   Enter choice (0-4): 1
✅ Selected: meme-boy

📺 Select subtitle style:
   1. Standard (SRT format)
   2. Karaoke (ASS format with word highlighting)

   Enter choice (1-2): 2
✅ Selected: Karaoke subtitles

💾 Output Directory:
   Default: renders/2025-12-08
   Use default? (Y/n): y
✅ Output directory: renders/2025-12-08

============================================================
📋 Generation Summary:
============================================================
   Text length: 58 characters
   Background: minecraft_parkour.mp4
   Voice: meme-boy
   Subtitles: karaoke
   Output: renders/2025-12-08
============================================================

   Start generation? (Y/n): y

🚀 Starting video generation...
```

## 📝 Files Changed

1. **tts/elevenlabs_tts.py**
   - Added `generate_word_timestamps_with_whisper()` function
   - Improved `estimate_timestamps()` algorithm
   - Automatic fallback to estimation if Whisper unavailable

2. **main_interactive.py** (NEW)
   - Complete interactive CLI implementation
   - Step-by-step prompts for all options
   - User-friendly interface

3. **main.py**
   - Added `--interactive` / `-i` flag
   - Integrated interactive mode

## 🔧 Technical Details

### Whisper Integration
- Uses OpenAI Whisper API for word-level alignment
- Requires `OPENAI_API_KEY` environment variable
- Falls back gracefully if key unavailable
- Works with both OpenAI TTS and ElevenLabs TTS

### Improved Estimation Algorithm
- Accounts for vowel density
- Better punctuation handling
- Word length adjustments
- Duration normalization to prevent cumulative errors

## 🚀 Next Steps

1. **Test the improvements**:
   ```bash
   python3 main.py --interactive
   ```

2. **Compare sync quality**: Generate a video and check subtitle timing

3. **Add background clips**: Place videos in `assets/background_clips/` for better results

## ⚠️ Notes

- Whisper API requires an OpenAI API key (even when using ElevenLabs TTS)
- If OpenAI key unavailable, the improved estimation algorithm is used
- Interactive mode works with all existing features

