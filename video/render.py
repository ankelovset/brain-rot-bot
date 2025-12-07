"""
Main video rendering pipeline.
"""
from pathlib import Path
from typing import Optional, Dict, Tuple
from datetime import datetime
import json
import logging

from config import Config
from tts.tts_router import generate_tts
from subtitles.subtitle_utils import generate_subtitles
from .background_selector import select_background_clip
from .compositor import compose_video


logger = logging.getLogger(__name__)


def render_video(
    script_text: str,
    output_dir: Path,
    voice_profile: Optional[str] = None,
    subtitle_style: str = "standard",
    background_clip: Optional[Path] = None,
    config: Optional[Config] = None
) -> Tuple[Path, Dict]:
    """
    Full pipeline: TTS → Subtitles → Video composition.
    
    Args:
        script_text: Input text script
        output_dir: Directory to save output files
        voice_profile: Meme voice profile name
        subtitle_style: "standard" or "karaoke"
        background_clip: Specific background clip (None = random)
        config: Configuration object
    
    Returns:
        Tuple of (video_path, metadata_dict)
    """
    if config is None:
        from config import config as global_config
        config = global_config
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"render_{timestamp}"
    
    logger.info(f"Starting render: {base_name}")
    
    # Step 1: Generate TTS audio with timestamps
    logger.info("Generating TTS audio...")
    audio_path, timestamps = generate_tts(
        text=script_text,
        output_path=output_dir / base_name,
        voice_profile=voice_profile,
        config=config
    )
    
    # Step 2: Generate subtitles
    logger.info("Generating subtitles...")
    subtitle_path = generate_subtitles(
        timestamps=timestamps,
        output_path=output_dir / base_name,
        style=subtitle_style,
        config=config
    )
    
    # Step 3: Select background (if not provided)
    if background_clip is None:
        bg_clip_path = select_background_clip(
            config.paths.background_clips,
            timestamps.get("duration", 30.0)
        )
    else:
        bg_clip_path = background_clip
    
    # Step 4: Compose final video
    logger.info("Composing video...")
    video_path = compose_video(
        background_path=bg_clip_path,
        audio_path=audio_path,
        timestamps=timestamps,
        output_path=output_dir / f"{base_name}.mp4",
        config=config,
        subtitle_style=subtitle_style
    )
    
    # Create metadata
    metadata = {
        "script": script_text,
        "voice_profile": voice_profile,
        "subtitle_style": subtitle_style,
        "background_clip": str(bg_clip_path) if bg_clip_path else None,
        "duration": timestamps.get("duration", 0),
        "output_files": {
            "audio": str(audio_path),
            "subtitles": str(subtitle_path),
            "video": str(video_path)
        },
        "timestamp": timestamp
    }
    
    # Save metadata
    metadata_path = output_dir / f"{base_name}_metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata, f, indent=2)
    
    logger.info(f"Render complete: {video_path}")
    
    return video_path, metadata

