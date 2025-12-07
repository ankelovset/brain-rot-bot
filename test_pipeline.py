#!/usr/bin/env python3
"""
Test script for the brain-rot-bot pipeline.
Run this to verify all components are working.
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from tts.tts_router import generate_tts
from subtitles.subtitle_utils import generate_subtitles
from video.background_selector import select_background_clip


def test_config():
    """Test configuration loading."""
    print("✅ Config loaded successfully")
    print(f"   TTS Provider: {config.tts.provider}")
    print(f"   Video Size: {config.video.width}x{config.video.height}")
    return True


def test_tts():
    """Test TTS generation (requires API key)."""
    print("\n🧪 Testing TTS generation...")
    try:
        test_text = "This is a test of the text to speech system."
        output_path = Path("test_output")
        
        audio_path, timestamps = generate_tts(
            text=test_text,
            output_path=output_path,
            voice_profile="meme-boy"
        )
        
        print(f"✅ TTS generated: {audio_path}")
        print(f"   Duration: {timestamps.get('duration', 0):.2f}s")
        print(f"   Words: {len(timestamps.get('words', []))}")
        return True
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        print("   Make sure OPENAI_API_KEY is set in environment")
        return False


def test_subtitles():
    """Test subtitle generation."""
    print("\n🧪 Testing subtitle generation...")
    try:
        # Mock timestamps
        timestamps = {
            "text": "This is a test",
            "duration": 2.5,
            "words": [
                {"word": "This", "start": 0.0, "end": 0.5},
                {"word": "is", "start": 0.5, "end": 1.0},
                {"word": "a", "start": 1.0, "end": 1.5},
                {"word": "test", "start": 1.5, "end": 2.5}
            ]
        }
        
        srt_path = generate_subtitles(
            timestamps=timestamps,
            output_path=Path("test_subtitles"),
            style="standard"
        )
        
        print(f"✅ Subtitles generated: {srt_path}")
        return True
    except Exception as e:
        print(f"❌ Subtitle test failed: {e}")
        return False


def test_background_selection():
    """Test background clip selection."""
    print("\n🧪 Testing background selection...")
    try:
        bg_clip = select_background_clip(
            config.paths.background_clips,
            duration=10.0
        )
        
        if bg_clip:
            print(f"✅ Background clip found: {bg_clip.name}")
        else:
            print("⚠️  No background clips found (add videos to assets/background_clips/)")
        return True
    except Exception as e:
        print(f"❌ Background selection test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧠 Brain Rot Bot - Pipeline Test\n")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Subtitle Generation", test_subtitles),
        ("Background Selection", test_background_selection),
        ("TTS Generation", test_tts),  # Last because it requires API key
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")


if __name__ == "__main__":
    main()

