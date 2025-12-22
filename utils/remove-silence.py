#!/usr/bin/env python3
import os
import subprocess
from tqdm import tqdm

def is_video_file(file_path):
    """
    Check if a file is a video file based on extension.
    """
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.m4v',
                       '.MP4', '.MOV', '.AVI', '.MKV', '.WEBM', '.FLV', '.WMV', '.M4V'}
    ext = os.path.splitext(file_path)[1]
    return ext in video_extensions

def remove_silence_from_audio(input_file, output_file, pbar=None):
    """
    Remove silence from audio file by segmenting, removing silence from each segment,
    and concatenating them back together.
    """
    import tempfile
    import shutil

    # Create temporary directory for segments
    temp_dir = tempfile.mkdtemp()

    try:
        if pbar:
            pbar.set_description(f"Segmenting: {os.path.basename(input_file)[:25]}")

        base_name = os.path.splitext(os.path.basename(input_file))[0]
        segment_pattern = os.path.join(temp_dir, f"{base_name}_segment_%03d.wav")

        # Step 1: Split audio into 30-second segments
        segment_cmd = [
            "ffmpeg",
            "-i", input_file,
            "-f", "segment",
            "-segment_time", "30",
            "-c:a", "pcm_s16le",
            "-ar", "44100",
            "-ac", "2",
            segment_pattern
        ]
        subprocess.run(segment_cmd, check=True, capture_output=True, text=True)

        # Get all segment files
        segment_files = sorted([f for f in os.listdir(temp_dir) if f.endswith('.wav')])

        if not segment_files:
            if pbar:
                pbar.write(f"✗ No segments created for {input_file}")
            return False

        if pbar:
            pbar.write(f"Created {len(segment_files)} segments, removing silence from each")

        # Step 2: Remove silence from each segment with progress bar
        processed_segments = []
        segment_pbar = tqdm(
            total=len(segment_files),
            desc=f"  Processing segments",
            unit="seg",
            leave=False,
            position=1
        )

        for i, seg_file in enumerate(segment_files):
            seg_path = os.path.join(temp_dir, seg_file)
            processed_path = os.path.join(temp_dir, f"processed_{seg_file}")

            segment_pbar.set_description(f"  Segment {i+1}/{len(segment_files)}")

            silence_cmd = [
                "ffmpeg",
                "-i", seg_path,
                "-af", "silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:detection=peak,aformat=dblp,areverse,silenceremove=start_periods=1:start_duration=0.5:start_threshold=-50dB:detection=peak,aformat=dblp,areverse",
                "-y",
                processed_path
            ]

            subprocess.run(silence_cmd, capture_output=True, text=True)

            # Check if output file exists and has size > 0
            if os.path.exists(processed_path) and os.path.getsize(processed_path) > 0:
                processed_segments.append(processed_path)

            segment_pbar.update(1)

        segment_pbar.close()

        if not processed_segments:
            if pbar:
                pbar.write(f"✗ No segments after silence removal for {input_file}")
            return False

        if pbar:
            pbar.set_description(f"Concatenating: {os.path.basename(input_file)[:22]}")

        # Step 3: Create concat list file
        concat_file = os.path.join(temp_dir, "concat_list.txt")
        with open(concat_file, 'w') as f:
            for seg in processed_segments:
                f.write(f"file '{seg}'\n")

        # Step 4: Concatenate all processed segments
        concat_cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c:a", "libmp3lame",
            "-b:a", "192k",
            "-y",
            output_file
        ]
        subprocess.run(concat_cmd, check=True, capture_output=True, text=True)

        if pbar:
            pbar.update(1)

        return True

    except subprocess.CalledProcessError as e:
        if pbar:
            pbar.write(f"✗ Error processing {input_file}: {e.stderr}")
        else:
            print(f"✗ Error processing {input_file}: {e.stderr}")
        return False
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)

def detect_non_silent_segments(input_file, silence_threshold=-50, min_silence_duration=0.5):
    """
    Detect non-silent segments in a video/audio file.
    Returns list of (start_time, end_time) tuples for non-silent parts.
    """
    import re

    # Detect silence using ffmpeg
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-af", f"silencedetect=noise={silence_threshold}dB:d={min_silence_duration}",
        "-f", "null",
        "-"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    # Parse silence periods from output
    silence_starts = []
    silence_ends = []

    for line in output.split('\n'):
        if 'silencedetect' in line:
            # silence_start: 12.3456
            start_match = re.search(r'silence_start:\s*(\d+\.?\d*)', line)
            if start_match:
                silence_starts.append(float(start_match.group(1)))

            # silence_end: 15.6789
            end_match = re.search(r'silence_end:\s*(\d+\.?\d*)', line)
            if end_match:
                silence_ends.append(float(end_match.group(1)))

    # Get total duration
    duration_match = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.\d+)', output)
    if duration_match:
        hours, minutes, seconds = duration_match.groups()
        total_duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    else:
        total_duration = None

    # Build non-silent segments
    non_silent_segments = []

    # Handle edge cases
    if not silence_starts and not silence_ends:
        # No silence detected - entire file is non-silent
        if total_duration:
            return [(0, total_duration)]
        return []

    # Start of file to first silence
    if silence_starts:
        if silence_starts[0] > 0.1:  # At least 0.1 seconds of audio
            non_silent_segments.append((0, silence_starts[0]))

    # Between silence periods
    for i in range(len(silence_ends)):
        if i < len(silence_starts) - 1:
            start = silence_ends[i]
            end = silence_starts[i + 1]
            if end - start > 0.1:  # At least 0.1 seconds
                non_silent_segments.append((start, end))

    # Last silence to end of file
    if silence_ends and total_duration:
        if total_duration - silence_ends[-1] > 0.1:
            non_silent_segments.append((silence_ends[-1], total_duration))

    return non_silent_segments

def remove_silence_from_video(input_file, output_file, pbar=None):
    """
    Remove silence from video file by detecting silent segments,
    cutting out non-silent parts, and concatenating them together.
    """
    import tempfile
    import shutil

    temp_dir = tempfile.mkdtemp()

    try:
        # Show progress message
        status_msg = f"Detecting silence: {os.path.basename(input_file)[:25]}"
        if pbar:
            pbar.set_description(status_msg)
        else:
            print(status_msg)

        # Detect non-silent segments
        segments = detect_non_silent_segments(input_file)

        if not segments:
            error_msg = f"✗ No non-silent segments found in {input_file}"
            if pbar:
                pbar.write(error_msg)
            else:
                print(error_msg)
            return False

        # Show segments found
        found_msg = f"Found {len(segments)} non-silent segments to extract"
        if pbar:
            pbar.write(found_msg)
        else:
            print(found_msg)

        # Extract each non-silent segment with progress bar
        segment_files = []
        segment_pbar = tqdm(
            total=len(segments),
            desc=f"Extracting segments",
            unit="seg",
            leave=True
        )

        for i, (start, end) in enumerate(segments):
            segment_file = os.path.join(temp_dir, f"segment_{i:04d}.mp4")
            duration = end - start

            segment_pbar.set_description(f"Extracting segment {i+1}/{len(segments)} ({start:.1f}s-{end:.1f}s)")

            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-ss", str(start),
                "-t", str(duration),
                "-c:v", "copy",
                "-c:a", "copy",
                "-y",
                segment_file
            ]

            subprocess.run(cmd, check=True, capture_output=True, text=True)
            segment_files.append(segment_file)
            segment_pbar.update(1)

        segment_pbar.close()

        # Show concatenation message
        concat_msg = f"Concatenating segments..."
        if pbar:
            pbar.set_description(concat_msg)
        else:
            print(concat_msg)

        # Create concat list
        concat_file = os.path.join(temp_dir, "concat_list.txt")
        with open(concat_file, 'w') as f:
            for seg_file in segment_files:
                f.write(f"file '{seg_file}'\n")

        # Concatenate all segments
        concat_cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_file,
            "-c", "copy",
            "-y",
            output_file
        ]
        subprocess.run(concat_cmd, check=True, capture_output=True, text=True)

        if pbar:
            pbar.update(1)

        return True

    except subprocess.CalledProcessError as e:
        error_msg = f"✗ Error processing {input_file}: {e.stderr}"
        if pbar:
            pbar.write(error_msg)
        else:
            print(error_msg)
        return False
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

def process_directory(directory_path):
    """
    Process all audio and video files in the given directory.
    """
    # Supported audio extensions
    audio_extensions = {'.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg', '.MP3', '.WAV', '.M4A'}

    # Supported video extensions
    video_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv', '.wmv', '.m4v',
                       '.MP4', '.MOV', '.AVI', '.MKV', '.WEBM', '.FLV', '.WMV', '.M4V'}

    # Create output directory
    output_dir = os.path.join(directory_path, "silence-removed")
    os.makedirs(output_dir, exist_ok=True)

    # Find all audio and video files
    media_files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            ext = os.path.splitext(file)[1]
            if ext in audio_extensions or ext in video_extensions:
                media_files.append(file)

    if not media_files:
        print("No audio or video files found in the directory.")
        return

    print(f"\nFound {len(media_files)} media file(s) to process.\n")

    # Process each file with progress bar
    success_count = 0
    with tqdm(total=len(media_files), desc="Overall Progress", unit="file") as pbar:
        for media_file in media_files:
            input_path = os.path.join(directory_path, media_file)
            base_name = os.path.splitext(media_file)[0]

            # Determine if it's a video or audio file and set appropriate output
            if is_video_file(input_path):
                # Keep original video extension
                original_ext = os.path.splitext(media_file)[1]
                output_path = os.path.join(output_dir, f"{base_name}_no-silence{original_ext}")
                if remove_silence_from_video(input_path, output_path, pbar):
                    success_count += 1
            else:
                # Audio files output as .mp3
                output_path = os.path.join(output_dir, f"{base_name}_no-silence.mp3")
                if remove_silence_from_audio(input_path, output_path, pbar):
                    success_count += 1

    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Successfully processed: {success_count}/{len(media_files)} files")
    print(f"Output directory: {output_dir}")
    print(f"{'='*50}")

def process_single_file(file_path):
    """
    Process a single audio or video file.
    """
    if not os.path.isfile(file_path):
        print(f"\n✗ Error: File '{file_path}' does not exist.")
        return False

    # Get the directory and create output subdirectory
    directory = os.path.dirname(file_path) or "."
    output_dir = os.path.join(directory, "silence-removed")
    os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(file_path))[0]

    print(f"\nProcessing: {os.path.basename(file_path)}\n")

    # Determine if it's a video or audio file
    if is_video_file(file_path):
        original_ext = os.path.splitext(file_path)[1]
        output_path = os.path.join(output_dir, f"{base_name}_no-silence{original_ext}")
        success = remove_silence_from_video(file_path, output_path)
    else:
        output_path = os.path.join(output_dir, f"{base_name}_no-silence.mp3")
        success = remove_silence_from_audio(file_path, output_path)

    if success:
        print(f"\n{'='*50}")
        print(f"Processing complete!")
        print(f"Output file: {output_path}")
        print(f"{'='*50}")

    return success

def main():
    """
    Main function that prompts for file/directory and processes audio/video files.
    """
    print("="*50)
    print("Audio/Video Silence Remover")
    print("="*50)
    print("\nThis script will remove silence from audio and video files")
    print("in the specified file or directory and save them to a 'silence-removed' subfolder.\n")

    # Prompt for file or directory
    path = input("Enter the file or directory path: ").strip()

    # Remove quotes if user pasted path with quotes
    path = path.strip("'\"")

    # Check if path exists
    if not os.path.exists(path):
        print(f"\n✗ Error: Path '{path}' does not exist.")
        return

    # Process based on whether it's a file or directory
    if os.path.isfile(path):
        process_single_file(path)
    elif os.path.isdir(path):
        process_directory(path)
    else:
        print(f"\n✗ Error: '{path}' is not a valid file or directory.")
        return

if __name__ == "__main__":
    main()
