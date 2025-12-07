"""
OpenAI TTS implementation with word-level timestamp support.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import openai
from moviepy import AudioFileClip


def generate_audio_with_timestamps(
    text: str,
    output_path: Path,
    voice: str = "alloy",
    model: str = "tts-1",
    api_key: Optional[str] = None
) -> Tuple[Path, Dict]:
    """
    Generate TTS audio and word-level timestamps using OpenAI API.
    
    Args:
        text: Input text to convert to speech
        output_path: Path to save audio file (without extension)
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        model: Model to use (tts-1 or tts-1-hd)
        api_key: OpenAI API key (uses env var if not provided)
    
    Returns:
        Tuple of (audio_path, timestamps_dict)
    """
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key required. Set OPENAI_API_KEY env var or pass api_key.")
    
    client = openai.OpenAI(api_key=api_key)
    
    # Generate audio
    audio_path = Path(f"{output_path}.mp3")
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
        response_format="mp3"
    )
    
    # Save audio
    with open(audio_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)
    
    # Get audio duration
    audio_clip = AudioFileClip(str(audio_path))
    duration = audio_clip.duration
    audio_clip.close()
    
    # Generate word-level timestamps using Whisper
    # Note: OpenAI TTS doesn't provide timestamps directly, so we use Whisper for alignment
    timestamps = generate_word_timestamps_with_whisper(
        text, str(audio_path), api_key, duration
    )
    
    # Save timestamps
    timestamps_path = Path(f"{output_path}_timestamps.json")
    with open(timestamps_path, "w") as f:
        json.dump(timestamps, f, indent=2)
    
    return audio_path, timestamps


def generate_word_timestamps_with_whisper(
    text: str,
    audio_path: str,
    api_key: str,
    duration: float
) -> Dict:
    """
    Use Whisper API to get word-level timestamps.
    
    Args:
        text: Original text
        audio_path: Path to audio file
        api_key: OpenAI API key
        duration: Audio duration in seconds
    
    Returns:
        Dictionary with word timestamps
    """
    client = openai.OpenAI(api_key=api_key)
    
    # Transcribe with word-level timestamps
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["word"]
        )
    
    # Extract word timestamps
    words = []
    if hasattr(transcript, 'words') and transcript.words:
        for word_obj in transcript.words:
            words.append({
                "word": word_obj.word,
                "start": word_obj.start,
                "end": word_obj.end
            })
    else:
        # Fallback: estimate timestamps based on text length
        words = estimate_timestamps(text, duration)
    
    return {
        "text": text,
        "duration": duration,
        "words": words
    }


def estimate_timestamps(text: str, duration: float) -> List[Dict]:
    """
    Fallback: estimate word timestamps based on text length.
    
    Args:
        text: Input text
        duration: Total audio duration
    
    Returns:
        List of word timestamp dictionaries
    """
    words = text.split()
    if not words:
        return []
    
    # Simple linear distribution
    time_per_char = duration / len(text)
    words_data = []
    current_time = 0.0
    
    for word in words:
        word_duration = len(word) * time_per_char * 1.2  # Slight padding
        words_data.append({
            "word": word,
            "start": current_time,
            "end": current_time + word_duration
        })
        current_time += word_duration
    
    return words_data

