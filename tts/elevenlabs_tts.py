"""
ElevenLabs TTS implementation with word-level timestamp support.
"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
from moviepy import AudioFileClip


def generate_audio_with_timestamps(
    text: str,
    output_path: Path,
    voice_id: str,
    api_key: Optional[str] = None,
    model_id: str = "eleven_turbo_v2_5"  # Updated: free tier compatible model
) -> Tuple[Path, Dict]:
    """
    Generate TTS audio using ElevenLabs API.
    
    Args:
        text: Input text to convert to speech
        output_path: Path to save audio file (without extension)
        voice_id: ElevenLabs voice ID
        api_key: ElevenLabs API key
        model_id: Model ID to use
    
    Returns:
        Tuple of (audio_path, timestamps_dict)
    """
    api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ElevenLabs API key required. Set ELEVENLABS_API_KEY env var.")
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    # Save audio
    audio_path = Path(f"{output_path}.mp3")
    with open(audio_path, "wb") as f:
        f.write(response.content)
    
    # Get duration
    audio_clip = AudioFileClip(str(audio_path))
    duration = audio_clip.duration
    audio_clip.close()
    
    # Use Whisper API for accurate word-level timestamps (same as OpenAI)
    # This provides much better synchronization than estimation
    timestamps = generate_word_timestamps_with_whisper(
        text, str(audio_path), duration
    )
    
    timestamps_dict = {
        "text": text,
        "duration": duration,
        "words": timestamps
    }
    
    # Save timestamps
    timestamps_path = Path(f"{output_path}_timestamps.json")
    with open(timestamps_path, "w") as f:
        json.dump(timestamps_dict, f, indent=2)
    
    return audio_path, timestamps_dict


def generate_word_timestamps_with_whisper(
    text: str,
    audio_path: str,
    duration: float
) -> List[Dict]:
    """
    Use Whisper API to get accurate word-level timestamps for ElevenLabs audio.
    This provides much better synchronization than estimation.
    
    Args:
        text: Original text
        audio_path: Path to audio file
        duration: Audio duration in seconds
    
    Returns:
        List of word timestamp dictionaries
    """
    import openai
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Fallback to estimation if OpenAI key not available
        return estimate_timestamps(text, duration)
    
    try:
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
            # Fallback to estimation
            words = estimate_timestamps(text, duration)
        
        return words
    except Exception as e:
        # If Whisper fails, fall back to estimation
        print(f"⚠️  Whisper alignment failed, using estimation: {e}")
        return estimate_timestamps(text, duration)


def estimate_timestamps(text: str, duration: float) -> List[Dict]:
    """
    Estimate word timestamps based on text length.
    
    Args:
        text: Input text
        duration: Total audio duration
    
    Returns:
        List of word timestamp dictionaries
    """
    words = text.split()
    if not words:
        return []
    
    # More sophisticated estimation
    time_per_char = duration / len(text)
    words_data = []
    current_time = 0.0
    
    # Improved estimation with better word timing
    # Account for speech rate variations
    vowels = 'aeiouAEIOU'
    
    for i, word in enumerate(words):
        # Base duration calculation
        char_count = len(word)
        vowel_count = sum(1 for c in word if c in vowels)
        
        # Words with more vowels tend to be spoken longer
        base_duration = char_count * time_per_char * (1.0 + vowel_count * 0.1)
        
        # Adjust for punctuation pauses
        if word.endswith(('.', '!', '?')):
            base_duration *= 1.5  # Longer pause for sentence endings
        elif word.endswith((',', ';', ':')):
            base_duration *= 1.25  # Medium pause
        elif word.endswith(("'", '"')):
            base_duration *= 1.1  # Small pause
        
        # Adjust for word length (longer words take proportionally less time per char)
        if char_count > 8:
            base_duration *= 0.9
        
        # Add small gap between words
        word_gap = 0.05 if i > 0 else 0.0
        
        words_data.append({
            "word": word,
            "start": current_time + word_gap,
            "end": current_time + word_gap + base_duration
        })
        current_time += word_gap + base_duration
    
    # Normalize to match total duration (in case of drift)
    if words_data and current_time > 0:
        scale_factor = duration / current_time
        for word_data in words_data:
            word_data["start"] *= scale_factor
            word_data["end"] *= scale_factor
    
    return words_data

