#!/usr/bin/env python3
"""
Batch transcribe video files using transcribe.chartedconsultants.com API
"""

import os
import sys
import json
import requests
from pathlib import Path
import time

API_BASE_URL = "https://transcribe.chartedconsultants.com"
API_MODEL = "turbo"

def transcribe_file(file_path, language="vi"):
    """Transcribe a single video file"""

    print(f"Uploading {file_path.name}...")

    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f, 'video/mp4')}
            params = {
                'language': language,
                'model': API_MODEL
            }

            response = requests.post(
                f"{API_BASE_URL}/transcribe",
                files=files,
                params=params,
                timeout=600  # 10 minute timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                print(f"Error: API returned status {response.status_code}")
                print(response.text[:500])
                return None

    except Exception as e:
        print(f"Error transcribing {file_path.name}: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python batch-transcribe-videos.py <videos_directory> [output_directory] [posts_json]")
        print("\nExample:")
        print("  python batch-transcribe-videos.py /path/to/videos")
        print("  python batch-transcribe-videos.py /path/to/videos /path/to/output")
        print("  python batch-transcribe-videos.py /path/to/videos /path/to/output /path/to/posts.json")
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

    # Get all complete video files (not .part files)
    video_files = sorted([f for f in videos_dir.glob("*.mp4") if not f.name.endswith('.part')])

    print(f"\nFound {len(video_files)} videos to transcribe")
    print(f"Output directory: {output_dir}")
    print(f"API: {API_BASE_URL}")
    print(f"Model: {API_MODEL}\n")

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i, video_path in enumerate(video_files, 1):
        # Extract post ID from filename
        post_id = video_path.stem.split('.')[0]

        # Check if already transcribed
        output_file = output_dir / f"{post_id}.md"
        if output_file.exists():
            print(f"[{i}/{len(video_files)}] ⊘ Skipping {video_path.name} - already transcribed")
            skip_count += 1
            continue

        print(f"\n[{i}/{len(video_files)}] Transcribing {video_path.name}")
        print(f"  File size: {video_path.stat().st_size / 1024 / 1024:.1f} MB")

        # Get post metadata
        post_data = posts_by_id.get(post_id, {})

        # Transcribe
        transcription = transcribe_file(video_path, language="vi")

        if transcription:
            # Save transcription with metadata
            metadata = {
                'post_id': post_id,
                'video_file': video_path.name,
                'post_text': post_data.get('text', ''),
                'post_url': post_data.get('url', ''),
                'timestamp': post_data.get('time', ''),
                'views': post_data.get('viewsCount', 0),
                'likes': post_data.get('likes', 0),
                'comments': post_data.get('comments', 0),
            }

            # Write markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Video: {post_id}\n\n")

                if metadata['post_url']:
                    f.write(f"**URL:** {metadata['post_url']}\n\n")

                if metadata['timestamp']:
                    f.write(f"**Date:** {metadata['timestamp']}\n\n")

                if metadata['post_text']:
                    f.write(f"**Caption:** {metadata['post_text']}\n\n")

                if metadata['views'] or metadata['likes'] or metadata['comments']:
                    f.write(f"**Engagement:** {metadata['views']} views • {metadata['likes']} likes • {metadata['comments']} comments\n\n")

                f.write(f"---\n\n")
                f.write(f"## Transcription\n\n")
                f.write(transcription)
                f.write("\n")

            print(f"  ✓ Saved to {output_file.name}")
            success_count += 1
        else:
            print(f"  ✗ Failed to transcribe")
            fail_count += 1

        # Rate limiting - wait between requests
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
