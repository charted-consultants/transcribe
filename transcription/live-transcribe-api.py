import os
import time
import queue
import threading
import logging
import wave
import pyaudio
import pandas as pd
import pyperclip
import requests
import io
from pynput import keyboard as pynput_keyboard

# ------------------ CONFIGURATION ------------------
SHOULD_SAVE_AUDIO = False
CLIPBOARD_ENABLED = True
MASTER_FOLDER = os.path.join(os.path.dirname(__file__), "transcriptions")
CSV_FILE = os.path.join(MASTER_FOLDER, "transcription.csv")

# API Configuration
API_BASE_URL = "https://transcribe.chartedconsultants.com"
API_MODEL = "turbo"  # Options: turbo, or other models supported by the API

RECORD_SECONDS = 5
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

os.makedirs(MASTER_FOLDER, exist_ok=True)

logging.basicConfig(
    filename="transcription_api.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

# 🧠 Event to signal clipboard + memory reset
reset_event = threading.Event()

def ensure_csv_exists():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Filename", "Transcription"])
        df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

def save_wav_file(filename, frames):
    path = os.path.join(MASTER_FOLDER, filename)
    wf = wave.open(path, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def record_audio(q):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    logging.info("Recording started...")
    try:
        while True:
            frames = []
            for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
            q.put(frames)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

def listen_for_reset_clipboard():
    COMBO = {pynput_keyboard.Key.ctrl, pynput_keyboard.KeyCode(char='c')}
    current_keys = set()

    def on_press(key):
        current_keys.add(key)
        if all(k in current_keys for k in COMBO):
            pyperclip.copy("")
            reset_event.set()
            print("🧹 Manual clipboard + memory reset triggered (Cmd+Shift+C).")
            current_keys.clear()

    def on_release(key):
        if key in current_keys:
            current_keys.remove(key)

    listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

def transcribe_chunk_via_api(audio_data):
    """
    Send audio chunk to the API for transcription
    Returns the transcribed text or None on error
    """
    try:
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(audio_data)

        wav_buffer.seek(0)

        # Send to API
        files = {
            'file': ('chunk.wav', wav_buffer, 'audio/wav')
        }
        params = {
            'model': API_MODEL
        }

        response = requests.post(
            f"{API_BASE_URL}/transcribe",
            files=files,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            # Extract text from response (adjust based on actual API response structure)
            if isinstance(result, dict):
                # Try common response field names
                return result.get('text') or result.get('transcription') or result.get('transcript') or str(result)
            return str(result)
        else:
            logging.error(f"API returned status {response.status_code}: {response.text}")
            return None

    except Exception as e:
        logging.error(f"API transcription error: {e}")
        return None

def transcribe_live():
    ensure_csv_exists()
    audio_queue = queue.Queue()
    all_frames = []
    full_transcription = ""
    clipboard_memory = ""
    timestamp = time.strftime("%y%m%d_%H%M%S")
    raw_filename = f"{timestamp}.wav"

    threading.Thread(target=record_audio, args=(audio_queue,), daemon=True).start()
    threading.Thread(target=listen_for_reset_clipboard, daemon=True).start()

    print(f"\n🎙️ Recording in 5-second chunks using API: {API_BASE_URL}")
    print(f"🤖 Model: {API_MODEL}")
    print("📋 Press Cmd+Shift+C to clear the clipboard + reset memory.")
    print("⌨️ Press Ctrl+C to stop...\n")

    try:
        while True:
            frames = audio_queue.get()
            all_frames.extend(frames)

            # 🧠 Reset clipboard memory if triggered
            if reset_event.is_set():
                clipboard_memory = ""
                reset_event.clear()

            # Transcribe chunk via API
            audio_data = b"".join(frames)
            chunk_text = transcribe_chunk_via_api(audio_data)

            if chunk_text:
                print(f"{chunk_text}")
                logging.info(f"{chunk_text}")

                # Append and update cumulative transcription in CSV
                full_transcription += " " + chunk_text
                df = pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else pd.DataFrame(columns=["Filename", "Transcription"])

                if raw_filename in df["Filename"].values:
                    df.loc[df["Filename"] == raw_filename, "Transcription"] = full_transcription.strip()
                else:
                    new_row = pd.DataFrame([{"Filename": raw_filename, "Transcription": full_transcription.strip()}])
                    df = pd.concat([df, new_row], ignore_index=True)

                df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

                # 📋 Clipboard handling
                if CLIPBOARD_ENABLED:
                    clipboard_memory += " " + chunk_text
                    pyperclip.copy(clipboard_memory.strip())

    except KeyboardInterrupt:
        print("\n🔁 Finalising...")

        if len(all_frames) == 0:
            print("ℹ️ No speech was recorded.")
            return

        if SHOULD_SAVE_AUDIO:
            save_wav_file(raw_filename, all_frames)
            print(f"✅ Audio saved as: {raw_filename}")
        else:
            print("✅ Transcription was saved during live processing. Audio not saved.")

        if CLIPBOARD_ENABLED:
            pyperclip.copy("")
            print("🧹 Clipboard cleared.")

def main():
    transcribe_live()

if __name__ == "__main__":
    main()
