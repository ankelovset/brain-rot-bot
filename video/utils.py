"""
Utility functions for video processing.
"""
from pathlib import Path
from typing import List


def get_supported_video_formats() -> List[str]:
    """Get list of supported video file extensions."""
    return ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.MP4', '.MOV', '.AVI', '.MKV', '.WEBM']


def validate_video_file(path: Path) -> bool:
    """Check if file is a valid video file."""
    return path.exists() and path.suffix.lower() in get_supported_video_formats()

