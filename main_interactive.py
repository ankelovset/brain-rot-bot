#!/usr/bin/env python3
"""
Interactive CLI for Brain Rot Bot - Automated TikTok/Shorts Video Generator
Provides a user-friendly interface for generating videos.
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import config
from video.render import render_video
from video.background_selector import select_background_clip
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_header():
    """Print welcome header."""
    print("\n" + "=" * 60)
    print("🧠 Brain Rot Bot - Interactive Video Generator")
    print("=" * 60 + "\n")


def get_input_text() -> str:
    """Prompt user for input text."""
    print("📝 Enter your script text:")
    print("   (Press Enter twice or Ctrl+D when done)\n")
    
    lines = []
    try:
        while True:
            line = input()
            if not line.strip() and lines:  # Empty line after content
                break
            if line.strip():
                lines.append(line)
    except EOFError:
        pass
    
    text = "\n".join(lines).strip()
    
    if not text:
        print("❌ No text provided. Exiting.")
        sys.exit(1)
    
    print(f"\n✅ Text received ({len(text)} characters)\n")
    return text


def select_background_video() -> Optional[Path]:
    """Let user select background video."""
    bg_folder = config.paths.background_clips
    
    if not bg_folder.exists():
        bg_folder.mkdir(parents=True, exist_ok=True)
    
    # Find all video files
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(list(bg_folder.glob(f"*{ext}")))
        video_files.extend(list(bg_folder.glob(f"*{ext.upper()}")))
    
    if not video_files:
        print("⚠️  No background videos found in assets/background_clips/")
        print("   The video will use a black background.")
        print("   You can add videos later and they'll be used automatically.\n")
        return None
    
    print("🎬 Select background video:")
    print("   0. Use black background (no video)")
    for i, video_file in enumerate(video_files, 1):
        print(f"   {i}. {video_file.name}")
    
    while True:
        try:
            choice = input(f"\n   Enter choice (0-{len(video_files)}): ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(video_files):
                selected = video_files[choice_num - 1]
                print(f"✅ Selected: {selected.name}\n")
                return selected
            else:
                print(f"❌ Invalid choice. Please enter 0-{len(video_files)}")
        except ValueError:
            print("❌ Please enter a number")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            sys.exit(0)


def select_voice() -> Optional[str]:
    """Let user select voice profile."""
    print("🎤 Select voice profile:")
    
    voices = list(config.tts.meme_voices.keys())
    print("   0. Default voice")
    for i, voice in enumerate(voices, 1):
        voice_info = config.tts.meme_voices[voice]
        print(f"   {i}. {voice} ({voice_info.get('voice', 'N/A')})")
    
    while True:
        try:
            choice = input(f"\n   Enter choice (0-{len(voices)}): ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                return None
            elif 1 <= choice_num <= len(voices):
                selected = voices[choice_num - 1]
                print(f"✅ Selected: {selected}\n")
                return selected
            else:
                print(f"❌ Invalid choice. Please enter 0-{len(voices)}")
        except ValueError:
            print("❌ Please enter a number")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            sys.exit(0)


def select_subtitle_style() -> str:
    """Let user select subtitle style."""
    print("📺 Select subtitle style:")
    print("   1. Standard (SRT format)")
    print("   2. Karaoke (ASS format with word highlighting)")
    
    while True:
        try:
            choice = input("\n   Enter choice (1-2): ").strip()
            if choice == "1":
                print("✅ Selected: Standard subtitles\n")
                return "standard"
            elif choice == "2":
                print("✅ Selected: Karaoke subtitles\n")
                return "karaoke"
            else:
                print("❌ Invalid choice. Please enter 1 or 2")
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            sys.exit(0)


def configure_voice_settings(voice_profile: Optional[str]) -> dict:
    """Let user configure voice settings if they want."""
    print("⚙️  Voice Configuration:")
    print("   Press Enter to use defaults, or enter custom values\n")
    
    settings = {}
    
    if voice_profile and voice_profile in config.tts.meme_voices:
        default = config.tts.meme_voices[voice_profile]
        print(f"   Current settings for '{voice_profile}':")
        print(f"   - Voice: {default.get('voice', 'N/A')}")
        print(f"   - Speed: {default.get('speed', 1.0)}")
        print(f"   - Pitch: {default.get('pitch', 1.0)}\n")
    
    # Note: Actual voice settings are applied in TTS provider
    # This is just for user awareness
    print("   (Voice settings are pre-configured per profile)")
    print("   (Advanced customization available in config.py)\n")
    
    return settings


def select_output_directory() -> Path:
    """Let user select or create output directory."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    default_dir = config.paths.renders / date_str
    
    print("💾 Output Directory:")
    print(f"   Default: {default_dir}")
    
    choice = input("   Use default? (Y/n): ").strip().lower()
    
    if choice in ('', 'y', 'yes'):
        output_dir = default_dir
    else:
        custom_path = input("   Enter custom path: ").strip()
        if custom_path:
            output_dir = Path(custom_path)
        else:
            output_dir = default_dir
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Output directory: {output_dir}\n")
    
    return output_dir


def main():
    """Main interactive CLI."""
    print_header()
    
    try:
        # Step 1: Get input text
        script_text = get_input_text()
        
        # Step 2: Select background video
        background_clip = select_background_video()
        
        # Step 3: Select voice
        voice_profile = select_voice()
        
        # Step 4: Configure voice (informational)
        configure_voice_settings(voice_profile)
        
        # Step 5: Select subtitle style
        subtitle_style = select_subtitle_style()
        
        # Step 6: Select output directory
        output_dir = select_output_directory()
        
        # Step 7: Confirm and generate
        print("\n" + "=" * 60)
        print("📋 Generation Summary:")
        print("=" * 60)
        print(f"   Text length: {len(script_text)} characters")
        print(f"   Background: {background_clip.name if background_clip else 'Black background'}")
        print(f"   Voice: {voice_profile or 'Default'}")
        print(f"   Subtitles: {subtitle_style}")
        print(f"   Output: {output_dir}")
        print("=" * 60)
        
        confirm = input("\n   Start generation? (Y/n): ").strip().lower()
        if confirm not in ('', 'y', 'yes'):
            print("❌ Cancelled.")
            sys.exit(0)
        
        print("\n🚀 Starting video generation...\n")
        
        # Generate video
        video_path, metadata = render_video(
            script_text=script_text,
            output_dir=output_dir,
            voice_profile=voice_profile,
            subtitle_style=subtitle_style,
            background_clip=background_clip,
            config=config
        )
        
        print("\n" + "=" * 60)
        print("✅ Video Generated Successfully!")
        print("=" * 60)
        print(f"   Video: {video_path}")
        print(f"   Audio: {metadata['output_files']['audio']}")
        print(f"   Subtitles: {metadata['output_files']['subtitles']}")
        print(f"   Duration: {metadata['duration']:.2f} seconds")
        print("=" * 60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error generating video: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

