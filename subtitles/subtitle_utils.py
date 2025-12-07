"""
Utility functions for subtitle processing.
"""
from pathlib import Path
from typing import Dict
from config import Config

from .srt_generator import generate_srt, group_words_into_lines
from .ass_karaoke import generate_ass_karaoke


def generate_subtitles(
    timestamps: Dict,
    output_path: Path,
    style: str = "standard",
    config: Config = None
) -> Path:
    """
    Generate subtitles in the requested format.
    
    Args:
        timestamps: Word timestamps dictionary
        output_path: Base path for output (without extension)
        style: Subtitle style ("standard" for SRT, "karaoke" for ASS)
        config: Configuration object
    
    Returns:
        Path to generated subtitle file
    """
    if config is None:
        from config import config as global_config
        config = global_config
    
    if style == "karaoke":
        return generate_ass_karaoke(
            timestamps=timestamps,
            output_path=Path(f"{output_path}.ass"),
            font_size=config.subtitles.font_size,
            font_color=config.subtitles.font_color,
            stroke_color=config.subtitles.stroke_color,
            stroke_width=config.subtitles.stroke_width,
            highlight_color=config.subtitles.karaoke_highlight_color,
            position=config.subtitles.position,
            margin_bottom=config.subtitles.margin_bottom
        )
    else:
        return generate_srt(
            timestamps=timestamps,
            output_path=Path(f"{output_path}.srt")
        )
