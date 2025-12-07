"""
Configuration management for brain-rot-bot video generator.
"""
import os
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class TTSConfig:
    """Text-to-Speech configuration."""
    provider: str = "elevenlabs"  # "openai" or "elevenlabs" - switched to elevenlabs for testing
    model: str = "tts-1"  # OpenAI: "tts-1" or "tts-1-hd"
    voice: str = "alloy"  # OpenAI voices: alloy, echo, fable, onyx, nova, shimmer
    # Meme voice profiles
    meme_voices: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "meme-boy": {"voice": "nova", "speed": 1.1, "pitch": 1.05},
        "sigma-narrator": {"voice": "onyx", "speed": 0.95, "pitch": 0.98},
        "uwu": {"voice": "shimmer", "speed": 1.15, "pitch": 1.2},
        "deep-epic": {"voice": "echo", "speed": 0.9, "pitch": 0.92},
    })
    elevenlabs_api_key: str = os.getenv("ELEVENLABS_API_KEY", "")
    elevenlabs_voice_id: str = os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Default: Sarah voice


@dataclass
class SubtitleConfig:
    """Subtitle rendering configuration."""
    style: str = "standard"  # "standard" or "karaoke"
    font_size: int = 70
    font_color: str = "white"
    stroke_color: str = "black"
    stroke_width: int = 3
    position: str = "bottom"  # "bottom", "center", "top"
    margin_bottom: int = 150  # pixels from bottom
    animation: bool = True
    karaoke_highlight_color: str = "yellow"


@dataclass
class VideoConfig:
    """Video output configuration."""
    width: int = 1080
    height: int = 1920
    fps: int = 30
    format: str = "mp4"
    codec: str = "libx264"
    bitrate: str = "5M"
    background_folder: str = "assets/background_clips"
    auto_loop: bool = True
    crop_mode: str = "center"  # "center", "smart", "fit"


@dataclass
class PathConfig:
    """Path configuration."""
    project_root: Path = field(default_factory=lambda: Path(__file__).parent)
    scripts_todo: Path = field(default_factory=lambda: Path("scripts/todo"))
    scripts_processed: Path = field(default_factory=lambda: Path("scripts/processed"))
    renders: Path = field(default_factory=lambda: Path("renders"))
    logs: Path = field(default_factory=lambda: Path("logs"))
    assets: Path = field(default_factory=lambda: Path("assets"))
    background_clips: Path = field(default_factory=lambda: Path("assets/background_clips"))
    fonts: Path = field(default_factory=lambda: Path("assets/fonts"))
    overlays: Path = field(default_factory=lambda: Path("assets/overlays"))

    def __post_init__(self):
        """Ensure all directories exist."""
        for path in [self.scripts_todo, self.scripts_processed, self.renders, 
                     self.logs, self.background_clips, self.fonts, self.overlays]:
            path.mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    """Main configuration class."""
    tts: TTSConfig = field(default_factory=TTSConfig)
    subtitles: SubtitleConfig = field(default_factory=SubtitleConfig)
    video: VideoConfig = field(default_factory=VideoConfig)
    paths: PathConfig = field(default_factory=PathConfig)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    automation_mode: bool = False
    log_level: str = "INFO"

    def __post_init__(self):
        """Initialize paths after creation."""
        self.paths.__post_init__()


# Global config instance
config = Config()

