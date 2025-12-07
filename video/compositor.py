"""
Video compositor: combines background, audio, and subtitles.
"""
from pathlib import Path
from typing import Optional, Dict
from moviepy import (
    VideoFileClip, AudioFileClip, CompositeVideoClip,
    TextClip, ColorClip
)
# Fade effects - MoviePy 2.x handles this differently
from config import Config

from .background_selector import select_background_clip, prepare_background_clip


def create_subtitle_clips(
    timestamps: Dict,
    video_duration: float,
    config: Config,
    style: str = "standard"
) -> list:
    """
    Create subtitle TextClips from timestamps.
    
    Args:
        timestamps: Word timestamps dictionary
        video_duration: Total video duration
        config: Configuration object
        style: Subtitle style
        config: Configuration
    
    Returns:
        List of TextClip objects
    """
    from subtitles.subtitle_utils import group_words_into_lines
    
    words = timestamps.get("words", [])
    if not words:
        return []
    
    # Group words into lines
    lines = group_words_into_lines(words, max_words_per_line=6)
    
    # Calculate position
    video_height = config.video.height
    if config.subtitles.position == "bottom":
        y_pos = video_height - config.subtitles.margin_bottom
    elif config.subtitles.position == "center":
        y_pos = video_height // 2
    else:
        y_pos = config.subtitles.margin_bottom
    
    subtitle_clips = []
    
    for line in lines:
        text = line["text"]
        start_time = line["start"]
        end_time = min(line["end"], video_duration)
        
        # Create text clip (MoviePy 2.x compatible)
        # Use system font - try Arial, fallback to default
        try:
            font_name = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
            import os
            if not os.path.exists(font_name):
                font_name = None  # Use default font
        except:
            font_name = None
        
        txt_clip = TextClip(
            text=text,
            font_size=config.subtitles.font_size,
            color=config.subtitles.font_color,
            font=font_name,
            stroke_color=config.subtitles.stroke_color,
            stroke_width=config.subtitles.stroke_width,
            method='caption',
            size=(config.video.width - 100, None),
            text_align='center'
        ).with_position(('center', y_pos)).with_start(start_time).with_duration(end_time - start_time)
        
        subtitle_clips.append(txt_clip)
    
    return subtitle_clips


def compose_video(
    background_path: Optional[Path],
    audio_path: Path,
    timestamps: Dict,
    output_path: Path,
    config: Optional[Config] = None,
    subtitle_style: str = "standard"
) -> Path:
    """
    Compose final video: background + audio + subtitles.
    
    Args:
        background_path: Path to background clip (None = black background)
        audio_path: Path to TTS audio file
        timestamps: Word timestamps for subtitles
        output_path: Path to save final video
        config: Configuration object
        subtitle_style: Subtitle style ("standard" or "karaoke")
    
    Returns:
        Path to generated video
    """
    if config is None:
        from config import config as global_config
        config = global_config
    
    # Load audio
    audio = AudioFileClip(str(audio_path))
    duration = audio.duration
    
    # Load or create background
    if background_path and background_path.exists():
        background = prepare_background_clip(
            background_path,
            duration,
            config.video.width,
            config.video.height,
            config.video.crop_mode
        )
    else:
        # Black background
        background = ColorClip(
            size=(config.video.width, config.video.height),
            color=(0, 0, 0),
            duration=duration
        )
    
    # Create subtitle clips
    subtitle_clips = create_subtitle_clips(timestamps, duration, config, subtitle_style)
    
    # Composite all elements (MoviePy 2.x uses with_audio)
    clips_to_composite = [background.with_audio(audio)]
    
    if subtitle_clips:
        clips_to_composite.extend(subtitle_clips)
    
    final_video = CompositeVideoClip(clips_to_composite, size=(config.video.width, config.video.height))
    
    # Add fade in/out (MoviePy 2.x compatible)
    try:
        final_video = final_video.with_fadein(0.5).with_fadeout(0.5)
    except AttributeError:
        # If fade methods not available, skip fades
        pass
    
    # Write video
    final_video.write_videofile(
        str(output_path),
        fps=config.video.fps,
        codec=config.video.codec,
        bitrate=config.video.bitrate,
        audio_codec='aac',
        preset='medium',
        threads=4
    )
    
    # Cleanup
    final_video.close()
    audio.close()
    background.close()
    for clip in subtitle_clips:
        clip.close()
    
    return output_path

