#!/usr/bin/env python3
"""
Brain Rot Bot - Automated TikTok/Shorts Video Generator
Main CLI entry point with automation support.
"""
import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from config import config
from video.render import render_video


# Setup logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.paths.logs / f"brain_rot_bot_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def process_script_file(script_path: Path) -> str:
    """
    Read script text from file.
    
    Args:
        script_path: Path to script file
    
    Returns:
        Script text content
    """
    if not script_path.exists():
        raise FileNotFoundError(f"Script file not found: {script_path}")
    
    with open(script_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def process_single_script(
    script_text: str,
    output_dir: Optional[Path] = None,
    voice_profile: Optional[str] = None,
    subtitle_style: str = "standard",
    background_clip: Optional[Path] = None
) -> Path:
    """
    Process a single script and generate video.
    
    Args:
        script_text: Input script text
        output_dir: Output directory (default: renders/YYYY-MM-DD)
        voice_profile: Meme voice profile
        subtitle_style: "standard" or "karaoke"
        background_clip: Specific background clip
    
    Returns:
        Path to generated video
    """
    if output_dir is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = config.paths.renders / date_str
    
    logger.info(f"Processing script (length: {len(script_text)} chars)")
    logger.info(f"Voice profile: {voice_profile or 'default'}")
    logger.info(f"Subtitle style: {subtitle_style}")
    
    video_path, metadata = render_video(
        script_text=script_text,
        output_dir=output_dir,
        voice_profile=voice_profile,
        subtitle_style=subtitle_style,
        background_clip=background_clip,
        config=config
    )
    
    logger.info(f"Video generated: {video_path}")
    return video_path


def automation_mode():
    """
    Automation mode: process all scripts from scripts/todo/ directory.
    """
    logger.info("Starting automation mode...")
    
    todo_dir = config.paths.scripts_todo
    processed_dir = config.paths.scripts_processed
    
    # Find all .txt files in todo directory
    script_files = list(todo_dir.glob("*.txt"))
    
    if not script_files:
        logger.info("No scripts found in todo directory")
        return
    
    logger.info(f"Found {len(script_files)} script(s) to process")
    
    for script_file in script_files:
        try:
            logger.info(f"Processing: {script_file.name}")
            
            # Read script
            script_text = process_script_file(script_file)
            
            # Generate video
            video_path = process_single_script(
                script_text=script_text,
                voice_profile=None,  # Can be configured per-file or random
                subtitle_style="standard"
            )
            
            # Move script to processed
            processed_path = processed_dir / script_file.name
            script_file.rename(processed_path)
            logger.info(f"Moved {script_file.name} to processed")
            
        except Exception as e:
            logger.error(f"Error processing {script_file.name}: {e}", exc_info=True)
            # Move to processed anyway to avoid reprocessing
            try:
                script_file.rename(processed_dir / f"{script_file.name}.error")
            except:
                pass
    
    logger.info("Automation mode complete")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Brain Rot Bot - Automated TikTok/Shorts Video Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process a script file
  python main.py --script my_script.txt --voice meme-boy
  
  # Process text directly
  python main.py --text "This is my script" --voice sigma-narrator --style karaoke
  
  # Automation mode (process all scripts in scripts/todo/)
  python main.py --automation
  
  # Custom background clip
  python main.py --script script.txt --background assets/background_clips/minecraft.mp4
        """
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group(required=False)
    input_group.add_argument(
        "--script",
        type=Path,
        help="Path to script text file"
    )
    input_group.add_argument(
        "--text",
        type=str,
        help="Script text directly (inline)"
    )
    input_group.add_argument(
        "--automation",
        action="store_true",
        help="Run in automation mode (process all scripts in scripts/todo/)"
    )
    input_group.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Run in interactive mode (guided prompts)"
    )
    
    # Voice and style options
    parser.add_argument(
        "--voice",
        type=str,
        choices=list(config.tts.meme_voices.keys()) + ["default"],
        default="default",
        help="Meme voice profile to use"
    )
    parser.add_argument(
        "--style",
        type=str,
        choices=["standard", "karaoke"],
        default="standard",
        help="Subtitle style: standard (SRT) or karaoke (ASS)"
    )
    
    # Background option
    parser.add_argument(
        "--background",
        type=Path,
        help="Specific background clip to use (default: random)"
    )
    
    # Output option
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory (default: renders/YYYY-MM-DD)"
    )
    
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        from main_interactive import main as interactive_main
        interactive_main()
        return
    
    # Automation mode
    if args.automation:
        automation_mode()
        return
    
    # Get script text
    if args.script:
        script_text = process_script_file(args.script)
    elif args.text:
        script_text = args.text
    else:
        parser.error("Must provide --script, --text, or --automation")
    
    # Process voice profile
    voice_profile = None if args.voice == "default" else args.voice
    
    # Process script
    try:
        video_path = process_single_script(
            script_text=script_text,
            output_dir=args.output,
            voice_profile=voice_profile,
            subtitle_style=args.style,
            background_clip=args.background
        )
        print(f"\n✅ Video generated successfully: {video_path}")
    except Exception as e:
        logger.error(f"Error generating video: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

