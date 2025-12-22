import os
import re
import subprocess
import time

FFMPEG_EXE = os.path.expanduser("D:\\transcribe-main\\ffmpeg\\bin\\ffmpeg.exe")
MASTER_FOLDER = os.path.expanduser(
    "C:\\Users\\Thi\\OneDrive - VL London LTD\\Documents\\SilenceRemoval"
)


def detect_silence(input_file, silence_db=-50, min_silence_duration=0.5):
    """Detect silent portions in a video file using ffmpeg."""
    cmd = [
        FFMPEG_EXE,
        "-i",
        input_file,
        "-af",
        f"silencedetect=n={silence_db}dB:d={min_silence_duration}",
        "-f",
        "null",
        "-",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    stderr = result.stderr

    starts = re.findall(r"silence_start:\s*([\d\.]+)", stderr)
    ends = re.findall(r"silence_end:\s*([\d\.]+)", stderr)
    durs = re.findall(r"silence_duration:\s*([\d\.]+)", stderr)

    return [
        {
            "start": float(starts[i]) if i < len(starts) else None,
            "end": float(ends[i]),
            "duration": float(durs[i]) if i < len(durs) else None,
        }
        for i in range(len(ends))
    ]


def remove_silence(input_file, silence_info):
    """Remove silent portions from video file and create new output file."""
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_nosilence{ext}"

    if os.path.exists(output_file):
        print(f"⏭ Already processed: {output_file}")
        return output_file

    if not silence_info:
        print(f"⚠️ No silence found in {input_file}. Skipping.")
        return input_file

    silence_starts = [s["start"] for s in silence_info if s["start"] is not None]
    silence_ends = [s["end"] for s in silence_info]

    fc = ""
    last_end = 0
    count = 0

    for start, end in zip(silence_starts, silence_ends):
        if last_end < start:
            fc += f"[0:v]trim=start={last_end}:end={start},setpts=PTS-STARTPTS[v{count}];"
            fc += f"[0:a]atrim=start={last_end}:end={start},asetpts=PTS-STARTPTS[a{count}];"
            count += 1
        last_end = end

    fc += f"[0:v]trim=start={last_end},setpts=PTS-STARTPTS[v{count}];"
    fc += f"[0:a]atrim=start={last_end},asetpts=PTS-STARTPTS[a{count}];"

    fc += "".join(f"[v{i}]" for i in range(count + 1))
    fc += f"concat=n={count+1}:v=1:a=0[outv];"
    fc += "".join(f"[a{i}]" for i in range(count + 1))
    fc += f"concat=n={count+1}:v=0:a=1[outa]"

    cmd = [
        FFMPEG_EXE,
        "-hwaccel",
        "cuda",
        "-i",
        input_file,
        "-filter_complex",
        fc,
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        "-c:v",
        "h264_nvenc",
        "-preset",
        "p7",
        "-rc",
        "vbr",
        "-cq",
        "18",
        "-b:v",
        "0",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        output_file,
    ]

    subprocess.run(cmd, check=True)
    return output_file


def process_video(input_file):
    """Process a single video file to remove silence."""
    if "_nosilence" in input_file:
        return  # Skip already processed

    print(f"🔍 Processing: {input_file}")
    silence = detect_silence(input_file)
    result_file = remove_silence(input_file, silence)
    print(f"✅ Done: {result_file}")


def monitor_folder():
    """Continuously monitor folder for video files and process them."""
    print(f"👀 Watching folder: {MASTER_FOLDER}")

    while True:
        try:
            for f in os.listdir(MASTER_FOLDER):
                full = os.path.join(MASTER_FOLDER, f)
                if f.lower().endswith((".mp4", ".mov", ".mkv")) and os.path.isfile(
                    full
                ):
                    process_video(full)
        except Exception as e:
            print(f"⚠️ Error: {e}")

        time.sleep(10)


if __name__ == "__main__":
    monitor_folder()
