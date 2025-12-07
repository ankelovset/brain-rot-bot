"""
ASS subtitle generator with karaoke-style word-by-word highlighting.
"""
from pathlib import Path
from typing import Dict, List


def generate_ass_karaoke(
    timestamps: Dict,
    output_path: Path,
    font_size: int = 70,
    font_color: str = "white",
    stroke_color: str = "black",
    stroke_width: int = 3,
    highlight_color: str = "yellow",
    position: str = "bottom",
    margin_bottom: int = 150
) -> Path:
    """
    Generate ASS subtitle file with karaoke word-by-word animation.
    
    Args:
        timestamps: Dictionary with 'words' list
        output_path: Path to save ASS file
        font_size: Font size in pixels
        font_color: Base font color
        stroke_color: Stroke/outline color
        stroke_width: Stroke width
        highlight_color: Color for highlighted (spoken) words
        position: Subtitle position ("bottom", "center", "top")
        margin_bottom: Margin from bottom in pixels
    
    Returns:
        Path to generated ASS file
    """
    words = timestamps.get("words", [])
    if not words:
        raise ValueError("No word timestamps provided")
    
    # Calculate position
    video_height = 1920
    if position == "bottom":
        y_pos = video_height - margin_bottom
    elif position == "center":
        y_pos = video_height // 2
    else:
        y_pos = margin_bottom
    
    # ASS header
    ass_content = [
        "[Script Info]\n",
        "Title: Brain Rot Bot Subtitles\n",
        "ScriptType: v4.00+\n",
        "\n",
        "[V4+ Styles]\n",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n",
        f"Style: Default,Arial,{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,{stroke_width},0,5,10,10,{video_height - y_pos},1\n",
        "\n",
        "[Events]\n",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    ]
    
    # Group words into lines for display
    lines = group_words_into_lines(words, max_words_per_line=6)
    
    for line in lines:
        line_words = [w for w in words if line["start"] <= w.get("start", 0) <= line["end"]]
        
        # Create karaoke effect: highlight words as they're spoken
        karaoke_text = create_karaoke_line(line_words, line, font_color, highlight_color)
        
        start_time = format_ass_time(line["start"])
        end_time = format_ass_time(line["end"])
        
        ass_content.append(
            f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{karaoke_text}\n"
        )
    
    # Write ASS file
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(ass_content)
    
    return output_path


def create_karaoke_line(
    words: List[Dict],
    line: Dict,
    base_color: str,
    highlight_color: str
) -> str:
    """
    Create ASS karaoke line with word-by-word highlighting.
    
    Args:
        words: List of word dictionaries
        line: Line dictionary with start/end times
        base_color: Base color for unspoken words
        highlight_color: Color for currently spoken word
    
    Returns:
        ASS formatted text with karaoke tags
    """
    if not words:
        return line.get("text", "")
    
    karaoke_parts = []
    line_start = line["start"]
    
    for i, word_obj in enumerate(words):
        word = word_obj.get("word", "")
        word_start = word_obj.get("start", 0.0)
        word_end = word_obj.get("end", 0.0)
        
        # Calculate karaoke timing relative to line start
        karaoke_start = int((word_start - line_start) * 100)  # centiseconds
        karaoke_end = int((word_end - line_start) * 100)
        
        # ASS karaoke tag: {\k<duration>} highlights word for duration
        duration = karaoke_end - karaoke_start
        
        if i == 0:
            # First word: set base color, then highlight
            karaoke_parts.append(f"{{\\c&H{color_to_ass(base_color)}&}}{{\\k{duration}}}{word}")
        else:
            # Subsequent words: highlight then return to base
            karaoke_parts.append(f"{{\\c&H{color_to_ass(highlight_color)}&}}{{\\k{duration}}}{{\\c&H{color_to_ass(base_color)}&}} {word}")
    
    return "".join(karaoke_parts)


def group_words_into_lines(words: List[Dict], max_words_per_line: int = 6) -> List[Dict]:
    """
    Group words into subtitle lines (same as SRT generator).
    
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
        
        current_line_words.append(word_obj)
        
        should_break = (
            len(current_line_words) >= max_words_per_line or
            word.endswith(('.', '!', '?')) or
            (word.endswith(',') and len(current_line_words) >= 3)
        )
        
        if should_break:
            last_word = current_line_words[-1]
            lines.append({
                "text": " ".join(w.get("word", "") for w in current_line_words),
                "start": current_start,
                "end": last_word.get("end", end)
            })
            current_line_words = []
            current_start = None
    
    if current_line_words:
        last_word = words[-1]
        lines.append({
            "text": " ".join(w.get("word", "") for w in current_line_words),
            "start": current_start or last_word.get("start", 0.0),
            "end": last_word.get("end", 0.0)
        })
    
    return lines


def format_ass_time(seconds: float) -> str:
    """
    Format seconds to ASS time format (H:MM:SS.cc).
    
    Args:
        seconds: Time in seconds
    
    Returns:
        Formatted time string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    centiseconds = int((seconds % 1) * 100)
    
    return f"{hours}:{minutes:02d}:{secs:02d}.{centiseconds:02d}"


def color_to_ass(color: str) -> str:
    """
    Convert color name/hex to ASS color format (BGR hex).
    
    Args:
        color: Color name or hex code
    
    Returns:
        ASS color string (BGR format)
    """
    color_map = {
        "white": "FFFFFF",
        "black": "000000",
        "yellow": "00FFFF",
        "red": "0000FF",
        "green": "00FF00",
        "blue": "FF0000",
    }
    
    if color.lower() in color_map:
        return color_map[color.lower()]
    
    # Assume hex format (remove # if present)
    hex_color = color.lstrip("#")
    if len(hex_color) == 6:
        # Convert RGB to BGR for ASS
        r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
        return f"{b}{g}{r}"
    
    return "FFFFFF"  # Default to white

