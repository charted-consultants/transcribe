#!/usr/bin/env python3
"""
MacOS Menu Bar App for Live Transcription
"""
import rumps
import threading
import os
import time
import queue
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
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
MASTER_FOLDER = os.path.join(ROOT_DIR, "transcription", "data", "transcriptions")
CSV_FILE = os.path.join(ROOT_DIR, "transcription", "data", "transcription.csv")

# API Configuration
API_BASE_URL = "https://transcribe.chartedconsultants.com"
API_MODEL = "turbo"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

RECORD_SECONDS = 5
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

os.makedirs(MASTER_FOLDER, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(MASTER_FOLDER, "transcription_menubar.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="w",
)

# Event to signal clipboard + memory reset
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
            if isinstance(result, dict):
                return result.get('text') or result.get('transcription') or result.get('transcript') or str(result)
            return str(result)
        else:
            logging.warning(f"Primary API returned {response.status_code}, falling back to OpenAI Whisper")

    except Exception as e:
        logging.warning(f"Primary API unreachable, falling back to OpenAI Whisper: {e}")

    # Fallback: OpenAI Whisper
    try:
        wav_buffer.seek(0)
        fallback_response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": ("chunk.wav", wav_buffer, "audio/wav")},
            data={"model": "whisper-1", "language": "en"},
            timeout=30,
        )
        if fallback_response.status_code == 200:
            return fallback_response.json().get("text")
        logging.error(f"OpenAI Whisper fallback failed: {fallback_response.status_code}: {fallback_response.text}")
    except Exception as e:
        logging.error(f"OpenAI Whisper fallback error: {e}")

    return None


class TranscriptionApp(rumps.App):
    def __init__(self):
        super(TranscriptionApp, self).__init__("🎙️", quit_button=None)

        # Create preview menu item (non-clickable, just for display)
        self.preview_item = rumps.MenuItem("Preview: (not recording)", callback=None)
        self.preview_text = "(not recording)"  # Thread-safe storage for preview text

        self.menu = [
            self.preview_item,
            None,  # Separator
            rumps.MenuItem("Start Recording", callback=self.start_recording),
            rumps.MenuItem("Stop Recording", callback=self.stop_recording),
            None,  # Separator
            rumps.MenuItem("Clear Clipboard", callback=self.clear_clipboard),
            rumps.MenuItem("Open Transcriptions Folder", callback=self.open_folder),
            None,  # Separator
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]

        self.recording = False
        self.recording_thread = None
        self.audio_queue = None
        self.stop_recording_flag = threading.Event()

        # Disable stop button initially
        self.menu["Stop Recording"].set_callback(None)

        # Set up keyboard listener for reset
        self.setup_keyboard_listener()

        # Start timer to update preview on main thread
        self.update_timer = rumps.Timer(self.update_preview_ui, 0.5)
        self.update_timer.start()

    def update_preview(self, text):
        """Store preview text (called from background thread)"""
        # Truncate to one line (max ~60 chars for readability)
        max_length = 60
        if len(text) > max_length:
            display_text = "..." + text[-max_length:]
        else:
            display_text = text if text else "(waiting...)"

        self.preview_text = display_text

    def update_preview_ui(self, _):
        """Update the UI on main thread (called by timer)"""
        self.preview_item.title = f"Preview: {self.preview_text}"

    def setup_keyboard_listener(self):
        """Set up global keyboard listener for Cmd+Shift+C to reset clipboard"""
        COMBO = {pynput_keyboard.Key.ctrl, pynput_keyboard.KeyCode(char='c')}
        current_keys = set()

        def on_press(key):
            current_keys.add(key)
            if all(k in current_keys for k in COMBO):
                pyperclip.copy("")
                reset_event.set()
                rumps.notification("Live Transcription", "Clipboard Reset", "Clipboard and memory cleared")
                current_keys.clear()

        def on_release(key):
            if key in current_keys:
                current_keys.remove(key)

        listener = pynput_keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    def start_recording(self, _):
        """Start the live transcription"""
        if self.recording:
            rumps.alert("Already Recording", "Transcription is already in progress")
            return

        self.recording = True
        self.title = "🔴"  # Red dot to indicate recording
        self.stop_recording_flag.clear()

        # Update preview
        self.update_preview("(starting...)")

        # Update menu
        self.menu["Start Recording"].set_callback(None)
        self.menu["Stop Recording"].set_callback(self.stop_recording)

        # Start recording in background thread
        self.recording_thread = threading.Thread(target=self.run_transcription, daemon=True)
        self.recording_thread.start()

        rumps.notification("Live Transcription", "Recording Started", "Transcription is now running")

    def stop_recording(self, _):
        """Stop the live transcription"""
        if not self.recording:
            return

        self.recording = False
        self.title = "🎙️"
        self.stop_recording_flag.set()

        # Update preview
        self.update_preview("(not recording)")

        # Update menu
        self.menu["Start Recording"].set_callback(self.start_recording)
        self.menu["Stop Recording"].set_callback(None)

        if CLIPBOARD_ENABLED:
            pyperclip.copy("")

        rumps.notification("Live Transcription", "Recording Stopped", "Transcription saved")

    def clear_clipboard(self, _):
        """Clear clipboard and reset memory"""
        pyperclip.copy("")
        reset_event.set()
        if self.recording:
            self.update_preview("(cleared, waiting...)")
        rumps.notification("Live Transcription", "Clipboard Cleared", "Memory reset")

    def open_folder(self, _):
        """Open the transcriptions folder in Finder"""
        os.system(f'open "{MASTER_FOLDER}"')

    def quit_app(self, _):
        """Quit the application"""
        if self.recording:
            self.stop_recording(None)
        rumps.quit_application()

    def run_transcription(self):
        """Main transcription loop running in background thread"""
        ensure_csv_exists()
        audio_queue = queue.Queue()
        all_frames = []
        full_transcription = ""
        clipboard_memory = ""
        timestamp = time.strftime("%y%m%d_%H%M%S")
        raw_filename = f"{timestamp}.wav"

        # Start audio recording thread
        audio_thread = threading.Thread(
            target=self.record_audio,
            args=(audio_queue,),
            daemon=True
        )
        audio_thread.start()

        logging.info(f"Recording started at {timestamp}")

        try:
            while not self.stop_recording_flag.is_set():
                try:
                    frames = audio_queue.get(timeout=1)
                except queue.Empty:
                    continue

                all_frames.extend(frames)

                # Reset clipboard memory if triggered
                if reset_event.is_set():
                    clipboard_memory = ""
                    reset_event.clear()
                    self.update_preview("(cleared, waiting...)")

                # Transcribe chunk via API
                audio_data = b"".join(frames)
                chunk_text = transcribe_chunk_via_api(audio_data)

                if chunk_text:
                    logging.info(f"Transcribed: {chunk_text}")

                    # Append and update cumulative transcription in CSV
                    full_transcription += " " + chunk_text
                    df = pd.read_csv(CSV_FILE) if os.path.exists(CSV_FILE) else pd.DataFrame(columns=["Filename", "Transcription"])

                    if raw_filename in df["Filename"].values:
                        df.loc[df["Filename"] == raw_filename, "Transcription"] = full_transcription.strip()
                    else:
                        new_row = pd.DataFrame([{"Filename": raw_filename, "Transcription": full_transcription.strip()}])
                        df = pd.concat([df, new_row], ignore_index=True)

                    df.to_csv(CSV_FILE, index=False, encoding="utf-8-sig")

                    # Clipboard handling
                    if CLIPBOARD_ENABLED:
                        clipboard_memory += " " + chunk_text
                        pyperclip.copy(clipboard_memory.strip())

                    # Update preview with latest transcription
                    self.update_preview(full_transcription.strip())

        except Exception as e:
            logging.error(f"Error in transcription loop: {e}")
            rumps.alert("Transcription Error", str(e))

        finally:
            logging.info("Recording stopped")

            if SHOULD_SAVE_AUDIO and len(all_frames) > 0:
                save_wav_file(raw_filename, all_frames)
                logging.info(f"Audio saved as: {raw_filename}")

    def record_audio(self, q):
        """Record audio and put chunks into queue"""
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        logging.info("Audio stream opened")

        try:
            while not self.stop_recording_flag.is_set():
                frames = []
                for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    if self.stop_recording_flag.is_set():
                        break
                    try:
                        data = stream.read(CHUNK, exception_on_overflow=False)
                        frames.append(data)
                    except Exception as e:
                        logging.error(f"Error reading audio: {e}")
                        break

                if frames:
                    q.put(frames)

        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            logging.info("Audio stream closed")


if __name__ == "__main__":
    app = TranscriptionApp()
    app.run()
