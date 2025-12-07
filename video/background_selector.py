"""
Background video clip selector and processor.
"""
import random
from pathlib import Path
from typing import Optional, List
from moviepy import VideoFileClip, CompositeVideoClip
from config import Config


def select_background_clip(background_folder: Path, duration: float) -> Optional[Path]:
    """
    Select a random background clip from the folder.
    
    Args:
        background_folder: Path to folder containing background clips
        duration: Required duration in seconds
    
    Returns:
        Path to selected clip, or None if no clips found
    """
    if not background_folder.exists():
        return None
    
    # Find all video files
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(list(background_folder.glob(f"*{ext}")))
        video_files.extend(list(background_folder.glob(f"*{ext.upper()}")))
    
    if not video_files:
        return None
    
    # Select random clip
    return random.choice(video_files)


def prepare_background_clip(
    clip_path: Path,
    duration: float,
    target_width: int = 1080,
    target_height: int = 1920,
    crop_mode: str = "center"
) -> VideoFileClip:
    """
    Load and prepare background clip: loop, crop, and scale to target dimensions.
    
    Args:
        clip_path: Path to background video
        duration: Target duration (will loop if needed)
        target_width: Target video width
        target_height: Target video height
        crop_mode: Crop mode ("center", "smart", "fit")
    
    Returns:
        Prepared VideoFileClip
    """
    clip = VideoFileClip(str(clip_path))
    
    # Loop clip to match duration (MoviePy 2.x compatible)
    if clip.duration < duration:
        loops_needed = int(duration / clip.duration) + 1
        # MoviePy 2.x: manually loop by concatenating
        from moviepy import concatenate_videoclips
        clips_list = [clip] * loops_needed
        clip = concatenate_videoclips(clips_list)
    
    # Trim to exact duration (MoviePy 2.x uses subclipped instead of subclip)
    clip = clip.subclipped(0, duration)
    
    # Crop and scale to vertical format
    clip = crop_and_scale_vertical(clip, target_width, target_height, crop_mode)
    
    return clip


def crop_and_scale_vertical(
    clip: VideoFileClip,
    target_width: int,
    target_height: int,
    crop_mode: str = "center"
) -> VideoFileClip:
    """
    Crop and scale video to vertical format (9:16).
    
    Args:
        clip: Input video clip
        target_width: Target width (1080)
        target_height: Target height (1920)
        crop_mode: Crop mode
    
    Returns:
        Cropped and scaled clip
    """
    clip_width, clip_height = clip.size
    target_aspect = target_width / target_height  # 9:16 = 0.5625
    
    if crop_mode == "center":
        # Center crop: maintain aspect, crop from center
        if clip_width / clip_height > target_aspect:
            # Clip is wider than target - crop width
            new_width = int(clip_height * target_aspect)
            x_center = clip_width / 2
            x1 = int(x_center - new_width / 2)
            x2 = int(x_center + new_width / 2)
            clip = clip.cropped(x1=x1, y1=0, x2=x2, y2=clip_height)
        else:
            # Clip is taller than target - crop height
            new_height = int(clip_width / target_aspect)
            y_center = clip_height / 2
            y1 = int(y_center - new_height / 2)
            y2 = int(y_center + new_height / 2)
            clip = clip.cropped(x1=0, y1=y1, x2=clip_width, y2=y2)
    
    elif crop_mode == "fit":
        # Fit: scale to fit, may have letterboxing
        scale_w = target_width / clip_width
        scale_h = target_height / clip_height
        scale = min(scale_w, scale_h)
        
        new_w = int(clip_width * scale)
        new_h = int(clip_height * scale)
        
        clip = clip.resized(new_size=(new_w, new_h))
        
        # Center on black background if needed
        if new_w != target_width or new_h != target_height:
            x_center = (target_width - new_w) // 2
            y_center = (target_height - new_h) // 2
            clip = clip.with_position((x_center, y_center))
            # Create black background
            from moviepy import ColorClip
            bg = ColorClip(size=(target_width, target_height), color=(0, 0, 0), duration=clip.duration)
            clip = CompositeVideoClip([bg, clip])
    
    else:  # smart or default to center
        return crop_and_scale_vertical(clip, target_width, target_height, "center")
    
    # Final resize to exact target dimensions
    clip = clip.resized(new_size=(target_width, target_height))
    
    return clip

