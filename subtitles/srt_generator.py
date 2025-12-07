"""
SRT subtitle file generator from word timestamps.
"""
from pathlib import Path
from typing import Dict, List


def generate_srt(timestamps: Dict, output_path: Path) -> Path:
    """
    Generate SRT subtitle file from word timestamps.
    
    Args:
        timestamps: Dictionary with 'words' list containing word timestamps
        output_path: Path to save SRT file
    
    Returns:
        Path to generated SRT file
    """
    words = timestamps.get("words", [])
    if not words:
        raise ValueError("No word timestamps provided")
    
    # Group words into subtitle lines (max 5-7 words per line)
    subtitle_lines = group_words_into_lines(words, max_words_per_line=6)
    
    srt_content = []
    for idx, line in enumerate(subtitle_lines, 1):
        start_time = format_srt_time(line["start"])
        end_time = format_srt_time(line["end"])
        text = line["text"]
        
        srt_content.append(f"{idx}\n")
        srt_content.append(f"{start_time} --> {end_time}\n")
        srt_content.append(f"{text}\n")
        srt_content.append("\n")
    
    # Write SRT file
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(srt_content)
    
    return output_path


def group_words_into_lines(words: List[Dict], max_words_per_line: int = 6) -> List[Dict]:
    """
    Group words into subtitle lines.
    
    Args:
        words: List of word dictionaries with 'word', 'start', 'end'
        max_words_per_line: Maximum words per subtitle line
    
    Returns:
        List of line dictionaries with 'text', 'start', 'end'
    """
    lines = []
    current_line_words = []
    current_start = None
    
    for word_obj in words:
        word = word_obj.get("word", "")
        start = word_obj.get("start", 0.0)
        end = word_obj.get("end", 0.0)
        
        if current_start is None:
            current_start = start
        
        current_line_words.append(word)
        
        # Create line when max words reached or on punctuation
        should_break = (
            len(current_line_words) >= max_words_per_line or
            word.endswith(('.', '!', '?')) or
            word.endswith(',') and len(current_line_words) >= 3
        )
        
        if should_break:
            line_text = " ".join(current_line_words)
            lines.append({
                "text": line_text,
                "start": current_start,
                "end": end
            })
            current_line_words = []
            current_start = None
    
    # Add remaining words
    if current_line_words:
        last_word = words[-1]
        line_text = " ".join(current_line_words)
        lines.append({
            "text": line_text,
            "start": current_start or last_word.get("start", 0.0),
            "end": last_word.get("end", 0.0)
        })
    
    return lines


def format_srt_time(seconds: float) -> str:
    """
    Format seconds to SRT time format (HH:MM:SS,mmm).
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

