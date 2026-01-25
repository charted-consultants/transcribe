# Live Transcription Menu Bar App - Setup Guide

This guide will help you set up the live transcription tool as a macOS menu bar app for easy access.

## Features

- **Menu Bar Icon**: Access transcription from your macOS menu bar (🎙️)
- **One-Click Start/Stop**: Start and stop recording with a single click
- **Status Indicator**: Icon changes to 🔴 when recording
- **Quick Actions**:
  - Start/Stop Recording
  - Clear Clipboard
  - Open Transcriptions Folder
  - Quit App
- **Keyboard Shortcut**: Cmd+Shift+C to clear clipboard and reset memory
- **Notifications**: macOS notifications for recording status

## Installation

### Easy Installation (Recommended)

Run the automated installation script:

```bash
cd /Users/dakthi/Documents/Factory-Tech/tools/transcribe-app/menubar
./install_menubar.sh
```

This will:
- Create a virtual environment (to avoid PEP 668 issues)
- Install all required packages (`rumps`, `pyaudio`, `pandas`, etc.)
- Set up everything you need

### Manual Installation

If you prefer to install manually:

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install packages:
```bash
pip install rumps pyaudio pandas pyperclip requests pynput
```

3. Make scripts executable:
```bash
chmod +x menubar_transcribe.py
chmod +x run_menubar.sh
```

## Running the App

After installation, simply run:

```bash
./run_menubar.sh
```

You should now see a 🎙️ microphone icon appear in your macOS menu bar!

**Note**: Always use `./run_menubar.sh` to start the app - this ensures the virtual environment is activated properly.

## How to Use

1. **Click the 🎙️ icon** in your menu bar to see options
2. **Select "Start Recording"** to begin live transcription
   - The icon will change to 🔴 to show recording is active
   - Transcriptions will be automatically copied to your clipboard
   - Transcriptions are saved to CSV in real-time
3. **Select "Stop Recording"** when done
   - The icon returns to 🎙️
   - Your transcription is saved
4. **Use "Clear Clipboard"** to reset the clipboard and memory without stopping
5. **Use "Open Transcriptions Folder"** to quickly access your saved transcriptions

## Keyboard Shortcuts

- **Cmd+Shift+C**: Clear clipboard and reset memory (while app is running)
- **Click Menu > Quit**: Close the app

## Auto-Start on Login (Optional)

To have the menu bar app start automatically when you log in:

### Option 1: Using System Preferences
1. Open **System Preferences** > **Users & Groups** > **Login Items**
2. Click the **+** button
3. Navigate to and select `run_menubar.sh` (NOT the .py file)
4. The app will now start automatically when you log in

### Option 2: Create a LaunchAgent (Advanced)

Create a file at `~/Library/LaunchAgents/com.transcribe.menubar.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.transcribe.menubar</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/dakthi/Documents/Factory-Tech/tools/transcribe-app/menubar/run_menubar.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.transcribe.menubar.plist
```

## Configuration

You can customize the app by editing these settings in `menubar_transcribe.py`:

- `API_BASE_URL`: Your transcription API endpoint
- `API_MODEL`: The model to use (default: "turbo")
- `RECORD_SECONDS`: Length of each audio chunk (default: 5 seconds)
- `CLIPBOARD_ENABLED`: Enable/disable automatic clipboard updates
- `SHOULD_SAVE_AUDIO`: Save audio files in addition to transcriptions

## Troubleshooting

### PEP 668 Error (externally-managed-environment)
If you see an error like:
```
error: externally-managed-environment
note: See PEP 668 for the detailed specification.
```

This is macOS protecting your system Python. Solution:
- Use the provided `install_menubar.sh` script (it creates a virtual environment)
- Or manually create a venv as shown in "Manual Installation" above
- **Do NOT use** `--break-system-packages` - it can break your system Python

### Module Not Found Error
If you get `ModuleNotFoundError: No module named 'rumps'`:
- Make sure you're using `./run_menubar.sh` to launch (NOT `python3 menubar_transcribe.py`)
- The launcher script activates the virtual environment automatically
- If you ran `install_menubar.sh`, this should be handled for you

### Icon doesn't appear in menu bar
- Make sure you used `./run_menubar.sh` to start the app
- Check the log file in `transcriptions/transcription_menubar.log`
- Try running `source venv/bin/activate` then `python3 menubar_transcribe.py`

### Permission errors for microphone
- Go to **System Preferences** > **Security & Privacy** > **Privacy** > **Microphone**
- Make sure Terminal (or your Python app) has microphone access

### App crashes or won't start
- Check the log file: `transcriptions/transcription_menubar.log`
- Make sure all dependencies are installed: run `./install_menubar.sh` again
- Try running the original script first to verify everything works

## Files and Folders

- `menubar_transcribe.py` - The menu bar app
- `transcriptions/` - Folder containing all transcriptions and logs
- `transcriptions/transcription.csv` - All transcriptions in CSV format
- `transcriptions/transcription_menubar.log` - App logs for debugging

## Comparison with Original Script

| Feature | Original (`live-transcribe-api.py`) | Menu Bar App |
|---------|-------------------------------------|--------------|
| Access | Run from terminal | Click menu bar icon |
| Start/Stop | Ctrl+C to stop | Click to start/stop |
| Status | Terminal output | Menu bar icon (🎙️/🔴) |
| Notifications | Terminal only | macOS notifications |
| Background | Requires terminal open | Runs in background |

Both versions have the same transcription capabilities - the menu bar version just makes it much easier to access!
