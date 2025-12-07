"""
TTS router that selects the appropriate TTS provider.
"""
import os
from pathlib import Path
from typing import Dict, Tuple, Optional
from config import Config, TTSConfig

from .openai_tts import generate_audio_with_timestamps as openai_generate
from .elevenlabs_tts import generate_audio_with_timestamps as elevenlabs_generate


def generate_tts(
    text: str,
    output_path: Path,
    voice_profile: Optional[str] = None,
    config: Optional[Config] = None
) -> Tuple[Path, Dict]:
    """
    Generate TTS audio with timestamps using configured provider.
    
    Args:
        text: Input text to convert
        output_path: Path to save output (without extension)
        voice_profile: Meme voice profile name (e.g., "meme-boy", "sigma-narrator")
        config: Configuration object (uses global config if not provided)
    
    Returns:
        Tuple of (audio_path, timestamps_dict)
    """
    if config is None:
        from config import config as global_config
        config = global_config
    
    # Get voice settings
    if voice_profile and voice_profile in config.tts.meme_voices:
        voice_settings = config.tts.meme_voices[voice_profile]
        voice = voice_settings["voice"]
    else:
        voice = config.tts.voice
    
    # Generate based on provider
    if config.tts.provider == "openai":
        return openai_generate(
            text=text,
            output_path=output_path,
            voice=voice,
            model=config.tts.model,
            api_key=config.openai_api_key
        )
    elif config.tts.provider == "elevenlabs":
        # Get API key from config or environment
        api_key = config.tts.elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")
        voice_id = config.tts.elevenlabs_voice_id or os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")
        
        return elevenlabs_generate(
            text=text,
            output_path=output_path,
            voice_id=voice_id,
            api_key=api_key
        )
    else:
        raise ValueError(f"Unknown TTS provider: {config.tts.provider}")

