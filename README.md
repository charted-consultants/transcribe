# FACTORY-OPS

```
  _____ _    ____ _____ ___  ______   __      ___  ____  ____
 |  ___/ \  / ___|_   _/ _ \|  _ \ \ / /___  / _ \|  _ \/ ___|
 | |_ / _ \| |     | || | | | |_) \ V /____|| | | | |_) \___ \
 |  _/ ___ \ |___  | || |_| |  _ < | |      | |_| |  __/ ___) |
 |_|/_/   \_\____| |_| \___/|_| \_\|_|       \___/|_|   |____/

    Operational back-office tools for the modern AI factory
```

## ABOUT

This is not a framework. This is not a wrapper. This is a collection of operational tools built exactly how one person works.

In the new era of AI-powered development, you don't have to compromise. You don't have to adapt to someone else's wrapper or framework. You can build tools that fit your workflow precisely.

These are base tools. Pull them, fork them, tell your Claude or Cursor or Aider to modify them to work exactly how YOU work. Your workflow is unique. Your tools should be too.

## PHILOSOPHY

The age of one-size-fits-all tools is over. With AI coding assistants, highly personalized workflows and tools are not just possible but preferable. You can have exactly what you need, built exactly how you need it.

This repository demonstrates that philosophy. It started as a simple transcription script. It evolved into a full operational toolkit through conversation with AI, adapting to real needs as they emerged.

## WHAT'S INSIDE

### MENUBAR
macOS menu bar application for live transcription with real-time preview.

**Features:**
- Live audio transcription via API
- Real-time preview of transcription text
- Clipboard integration with memory
- Auto-start capability
- Custom microphone icon
- Keyboard shortcuts for control

**Launch methods:**
```bash
~/transcribe-menubar.sh              # Quick terminal launch
~/Transcribe Menubar.app             # Double-click application
./menubar/run_menubar.sh             # Direct script launch
```

**Setup:**
```bash
cd menubar
./install_menubar.sh                 # Install dependencies
./enable_autostart.sh                # Enable auto-start on login
```

### TRANSCRIPTION
Tools for audio transcription and processing.

**Scripts:**
- `live-transcribe.py` - Live microphone transcription
- `live-transcribe-api.py` - API-based transcription
- `post-transcribe.py` - Post-process transcription files

**Data storage:**
- `data/` - Transcription outputs and CSV files
- `logs/` - Application logs

### UTILS
Utility scripts for media processing.

**Available tools:**
- `mp4-to-wav.py` - Convert MP4 to WAV format
- `remove-silence.py` - Remove silence from audio
- `remove-silence-v2.py` - Enhanced silence removal
- `yt-download-audio.py` - Download audio from YouTube
- `yt-download-video.py` - Download video from YouTube

### MEDIA
Storage for audio and video files used in transcription and processing.

## INSTALLATION

### Prerequisites
- Python 3.13 or higher
- macOS (for menu bar app)
- Virtual environment (included)

### Quick start
```bash
# Clone the repository
git clone git@github.com:dakthi/transcribe.git factory-ops
cd factory-ops

# Install menubar app
cd menubar
./install_menubar.sh

# Launch the app
~/transcribe-menubar.sh
```

### Virtual environment
All scripts use a centralized virtual environment located at `venv/` in the root directory. All dependencies are managed through this single environment.

## CONFIGURATION

### Transcription API
The menubar app uses an external transcription API. Configure in `menubar/menubar_transcribe.py`:

```python
API_BASE_URL = "https://transcribe.chartedconsultants.com"
API_MODEL = "turbo"
```

### Audio settings
Adjust recording parameters in `menubar/menubar_transcribe.py`:

```python
RECORD_SECONDS = 5        # Chunk duration
RATE = 16000              # Sample rate
CHANNELS = 1              # Mono audio
```

## USAGE RECOMMENDATIONS

**For best results:**

1. PULL this repository
2. TELL your AI coding assistant (Claude, Cursor, Aider, etc.) to integrate it into YOUR workflow
3. MODIFY the tools to match how YOU work
4. DON'T compromise for generic wrappers when you can have exactly what you need

Your workflow is different from everyone else's. That's not a problem to solve, it's a feature to embrace.

## STRUCTURE

```
factory-ops/
├── venv/                    # Centralized Python environment
├── menubar/                 # Menu bar application
│   ├── menubar_transcribe.py
│   ├── run_menubar.sh
│   ├── install_menubar.sh
│   └── ...
├── transcription/           # Transcription tools
│   ├── data/               # Output files
│   ├── logs/               # Log files
│   └── *.py                # Transcription scripts
├── media/                   # Audio/video storage
├── utils/                   # Utility scripts
└── README.md               # This file
```

## KEYBOARD SHORTCUTS

**Menubar app:**
- `Ctrl+C` - Clear clipboard and reset memory
- Menu bar icon - Click to access controls

**Menu options:**
- Start recording - Begin live transcription
- Stop recording - End transcription session
- Clear clipboard - Reset clipboard memory
- Open transcriptions folder - View saved files
- Quit - Exit application

## EXTENDING

These tools are meant to be extended and personalized. Some ideas:

- Add different transcription providers
- Integrate with your note-taking system
- Add custom keyboard shortcuts
- Build additional menu bar tools
- Connect to your task management workflow
- Add language translation
- Implement custom audio filters

Don't ask permission. Just build what you need.

## REQUIREMENTS

See `requirements.txt` for Python dependencies. The installation script handles all dependencies automatically.

Main dependencies:
- rumps - macOS menu bar framework
- pyaudio - Audio recording
- pandas - Data handling
- pyperclip - Clipboard integration
- requests - API communication
- pynput - Keyboard monitoring

## LICENSE

Use it however you want. Modify it to fit your needs. Share your modifications if you want. Or don't. It's your workflow.

## CREDITS

Built through iterative conversation between a human and Claude, demonstrating how AI coding assistants enable truly personalized tool development.

This is what's possible when you stop compromising.
