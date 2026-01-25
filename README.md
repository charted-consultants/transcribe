# Transcribe App

macOS/Windows application for live audio transcription with batch processing utilities.

## Features

- **Live transcription** - Real-time audio transcription via API
- **Menu bar app** - Quick access from macOS menu bar
- **Clipboard integration** - Auto-copy transcriptions with memory
- **Batch processing** - Transcribe multiple videos/audio files at once
- **Media utilities** - YouTube download, format conversion, silence removal
- **Keyboard shortcuts** - Quick control and clipboard management

## Components

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
~/transcribe-menubar.sh              # Quick terminal launch (requires symlink setup)
./transcribe-menubar.sh              # Launch from repo directory
~/Transcribe Menubar.app             # Double-click application
./menubar/run_menubar.sh             # Direct script launch
```

**Setup:**

*macOS:*
```bash
# Install dependencies
cd menubar
./install_menubar.sh

# Create launcher symlink for easy access from anywhere
ln -sf "$(pwd)/../transcribe-menubar.sh" ~/transcribe-menubar.sh

# Optional: Enable auto-start on login
./enable_autostart.sh
```

*Windows:*
```powershell
# Install dependencies
cd menubar
pip install -r requirements.txt

# Create launcher shortcut (run as Administrator)
# Option 1: Create symlink
mklink "%USERPROFILE%\transcribe-menubar.bat" "%CD%\..\transcribe-menubar.sh"

# Option 2: Add repo directory to PATH
# Go to System Properties > Environment Variables > User Variables > Path
# Add: C:\path\to\transcribe-app
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
- macOS or Windows (menu bar app optimized for macOS)
- Virtual environment (recommended)

### Quick start

*macOS:*
```bash
# Clone the repository
git clone git@github-dakthi:dakthi/transcribe.git transcribe-app
cd transcribe-app

# Install menubar app and create launcher
cd menubar
./install_menubar.sh
ln -sf "$(pwd)/../transcribe-menubar.sh" ~/transcribe-menubar.sh

# Launch the app
~/transcribe-menubar.sh
```

*Windows:*
```powershell
# Clone the repository
git clone git@github-dakthi:dakthi/transcribe.git transcribe-app
cd transcribe-app

# Install dependencies
cd menubar
pip install -r requirements.txt

# Launch the app
python ..\transcribe-menubar.sh
# Or add the repo to PATH and run from anywhere
```

### Virtual environment
All scripts use a centralized virtual environment located at `venv/` in the root directory. All dependencies are managed through this single environment.

## CONFIGURATION

### Transcription API
The menubar app uses an external transcription API. Configure in `menubar/menubar_transcribe.py`:

```python
API_BASE_URL = "https://transcribe.chartedconsultants.com"
API_MODEL = "turbo"  # The transcription model to use
```

### Audio settings
Adjust recording parameters in `menubar/menubar_transcribe.py`:

```python
RECORD_SECONDS = 5        # Chunk duration
RATE = 16000              # Sample rate
CHANNELS = 1              # Mono audio
```

## STRUCTURE

```
transcribe-app/
├── transcribe-menubar.sh    # Quick launcher script (symlink to ~/)
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
│   ├── batch-transcribe-mp4-videos.py
│   ├── batch-transcribe-videos.py
│   └── ...
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

Extension ideas:

- Add different transcription providers
- Integrate with your note-taking system
- Add custom keyboard shortcuts
- Build additional menu bar tools
- Connect to your task management workflow
- Add language translation
- Implement custom audio filters

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

MIT License - Use freely, modify as needed.

## CREDITS

Built with Claude Code.
