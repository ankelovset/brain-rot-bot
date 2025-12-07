#!/usr/bin/env python3
"""
Helper script to download background gameplay videos.
This script helps you download videos from sources you have permission to use.

Usage:
    python scripts/download_backgrounds.py --source youtube --url <video_url>
    python scripts/download_backgrounds.py --source pexels --query "minecraft parkour"
"""
import argparse
import subprocess
import sys
from pathlib import Path
import requests
import json


def check_yt_dlp():
    """Check if yt-dlp is installed."""
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_youtube_video(url: str, output_dir: Path, start_time: int = None, duration: int = 30):
    """
    Download video from YouTube using yt-dlp.
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save video
        start_time: Start time in seconds (optional)
        duration: Duration to extract in seconds
    """
    if not check_yt_dlp():
        print("❌ yt-dlp not found. Install it with: pip install yt-dlp")
        print("   Or: brew install yt-dlp")
        return None
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Build yt-dlp command
    cmd = [
        'yt-dlp',
        '-f', 'best[height<=1080]',  # Get best quality up to 1080p
        '-o', str(output_dir / '%(title)s.%(ext)s'),
        '--no-playlist',
    ]
    
    # Add time range if specified
    if start_time is not None:
        cmd.extend(['--download-sections', f'*{start_time}-{start_time + duration}'])
    else:
        # Limit duration to 30 seconds by default
        cmd.extend(['--postprocessor-args', f'ffmpeg:-t {duration}'])
    
    cmd.append(url)
    
    try:
        print(f"📥 Downloading from YouTube: {url}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Download successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Download failed: {e.stderr}")
        return False


def download_pexels_video(query: str, output_dir: Path, per_page: int = 5):
    """
    Download videos from Pexels (free stock videos).
    Requires Pexels API key.
    
    Args:
        query: Search query
        output_dir: Directory to save videos
        per_page: Number of videos to download
    """
    api_key = input("Enter Pexels API key (get free key at https://www.pexels.com/api/): ").strip()
    if not api_key:
        print("❌ API key required")
        return False
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Search Pexels
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": per_page, "orientation": "portrait"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        videos = data.get('videos', [])
        if not videos:
            print(f"❌ No videos found for query: {query}")
            return False
        
        print(f"📥 Found {len(videos)} videos. Downloading...")
        
        for i, video in enumerate(videos[:per_page]):
            # Get best quality video file
            video_files = video.get('video_files', [])
            if not video_files:
                continue
            
            # Prefer HD quality
            best_video = max(video_files, key=lambda x: x.get('width', 0) * x.get('height', 0))
            video_url = best_video.get('link')
            
            if not video_url:
                continue
            
            # Download video
            filename = f"pexels_{video['id']}.mp4"
            filepath = output_dir / filename
            
            print(f"  Downloading {i+1}/{len(videos[:per_page])}: {video.get('id')}")
            video_response = requests.get(video_url, stream=True)
            video_response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✅ Saved: {filename}")
        
        print("✅ All downloads complete!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download background gameplay videos")
    parser.add_argument(
        "--source",
        choices=["youtube", "pexels"],
        required=True,
        help="Video source"
    )
    parser.add_argument(
        "--url",
        help="YouTube video URL (for youtube source)"
    )
    parser.add_argument(
        "--query",
        help="Search query (for pexels source)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("assets/background_clips"),
        help="Output directory"
    )
    parser.add_argument(
        "--start-time",
        type=int,
        help="Start time in seconds (YouTube only)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Duration in seconds (default: 30)"
    )
    
    args = parser.parse_args()
    
    if args.source == "youtube":
        if not args.url:
            print("❌ --url required for YouTube source")
            sys.exit(1)
        download_youtube_video(args.url, args.output, args.start_time, args.duration)
    elif args.source == "pexels":
        if not args.query:
            print("❌ --query required for Pexels source")
            sys.exit(1)
        download_pexels_video(args.query, args.output)


if __name__ == "__main__":
    main()

