#!/usr/bin/env python3
"""
Batch transcribe MP4 video files:
1. Convert MP4 to MP3 using ffmpeg
2. Transcribe MP3 using transcribe.chartedconsultants.com API
3. Save results incrementally
"""

import os
import sys
import json
import requests
import subprocess
from pathlib import Path
import time

API_BASE_URL = "https://transcribe.chartedconsultants.com"
API_MODEL = "turbo"

def convert_mp4_to_mp3(mp4_path, mp3_path):
    """Convert MP4 video to MP3 audio using ffmpeg"""
    try:
        result = subprocess.run([
            'ffmpeg',
            '-i', str(mp4_path),
            '-vn',  # No video
            '-acodec', 'libmp3lame',
            '-q:a', '2',  # Quality
            '-y',  # Overwrite
            str(mp3_path)
        ], capture_output=True, text=True, timeout=300)

        if result.returncode == 0:
            return True
        else:
            print(f"  ✗ ffmpeg error: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ✗ Conversion error: {e}")
        return False

def transcribe_audio(audio_path, language="vi"):
    """Transcribe audio file using API"""
    try:
        with open(audio_path, 'rb') as f:
            files = {'file': (audio_path.name, f, 'audio/mpeg')}
            params = {'language': language, 'model': API_MODEL}

            response = requests.post(
                f"{API_BASE_URL}/transcribe",
                files=files,
                params=params,
                timeout=600
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                print(f"  ✗ API error {response.status_code}: {response.text[:200]}")
                return None
    except Exception as e:
        print(f"  ✗ Transcription error: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch-transcribe-mp4-videos.py <videos_directory> [output_directory] [posts_json]")
        sys.exit(1)

    videos_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else videos_dir.parent / "transcriptions"
    posts_json = Path(sys.argv[3]) if len(sys.argv) > 3 else None

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load posts data if provided
    posts_by_id = {}
    if posts_json and posts_json.exists():
        print(f"Loading post metadata from {posts_json}")
        with open(posts_json, 'r', encoding='utf-8') as f:
            posts = json.load(f)
            posts_by_id = {p['postId']: p for p in posts}

    # Get all complete MP4 files (not .part files)
    video_files = sorted([f for f in videos_dir.glob("*.mp4") if not f.name.endswith('.part')])

    print(f"\nFound {len(video_files)} MP4 videos to transcribe")
    print(f"Output directory: {output_dir}")
    print(f"API: {API_BASE_URL}")
    print(f"Model: {API_MODEL}\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, video_path in enumerate(video_files, 1):
        post_id = video_path.stem.split('.')[0]

        # Check if already transcribed
        output_file = output_dir / f"{post_id}.md"
        if output_file.exists():
            print(f"[{i}/{len(video_files)}] ⊘ Skipping {video_path.name} - already transcribed")
            skip_count += 1
            continue

        print(f"\n[{i}/{len(video_files)}] Processing {video_path.name}")
        print(f"  Video size: {video_path.stat().st_size / 1024 / 1024:.1f} MB")

        # Convert MP4 to MP3
        mp3_path = videos_dir / f"{post_id}.mp3"
        if not mp3_path.exists():
            print(f"  Converting to MP3...")
            if not convert_mp4_to_mp3(video_path, mp3_path):
                fail_count += 1
                continue
        else:
            print(f"  MP3 already exists")

        print(f"  Audio size: {mp3_path.stat().st_size / 1024:.1f} KB")
        print(f"  Transcribing...")

        # Transcribe
        transcription = transcribe_audio(mp3_path, language="vi")

        if transcription:
            # Get post metadata
            post_data = posts_by_id.get(post_id, {})

            # Save transcription with metadata
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Video: {post_id}\n\n")

                if post_data.get('url'):
                    f.write(f"**URL:** {post_data['url']}\n\n")

                if post_data.get('time'):
                    f.write(f"**Date:** {post_data['time']}\n\n")

                if post_data.get('text'):
                    f.write(f"**Caption:** {post_data['text']}\n\n")

                views = post_data.get('viewsCount', 0)
                likes = post_data.get('likes', 0)
                comments = post_data.get('comments', 0)
                if views or likes or comments:
                    f.write(f"**Engagement:** {views} views • {likes} likes • {comments} comments\n\n")

                f.write(f"---\n\n")
                f.write(f"## Transcription\n\n")
                f.write(transcription)
                f.write("\n")

            print(f"  ✓ Saved to {output_file.name} ({len(transcription)} chars)")
            success_count += 1

            # Clean up MP3
            if mp3_path.exists():
                mp3_path.unlink()
                print(f"  Cleaned up MP3")
        else:
            print(f"  ✗ Failed to transcribe")
            fail_count += 1

        # Rate limiting
        if i < len(video_files):
            time.sleep(2)

    print(f"\n" + "="*60)
    print(f"TRANSCRIPTION COMPLETE")
    print(f"="*60)
    print(f"✓ Success: {success_count}")
    print(f"⊘ Skipped: {skip_count}")
    print(f"✗ Failed:  {fail_count}")
    print(f"\nTranscriptions saved to: {output_dir}")

if __name__ == "__main__":
    main()
