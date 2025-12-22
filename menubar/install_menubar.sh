#!/bin/bash

echo "🎙️  Live Transcription Menu Bar App - Installation"
echo "=================================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Get the root directory (parent of menubar folder)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$DIR/.." && pwd )"

# Create virtual environment in root
echo "📦 Creating virtual environment..."
if [ -d "$ROOT_DIR/venv" ]; then
    echo "⚠️  Virtual environment already exists, using existing one"
else
    cd "$ROOT_DIR"
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

echo ""

# Activate virtual environment and install packages
echo "📦 Installing dependencies in virtual environment..."
source "$ROOT_DIR/venv/bin/activate"

# Install all required packages
pip install --upgrade pip
pip install rumps pyaudio pandas pyperclip requests pynput

if [ $? -eq 0 ]; then
    echo "✅ All packages installed successfully"
else
    echo "❌ Installation failed. Please check the error messages above."
    deactivate
    exit 1
fi

deactivate
echo ""

# Make the scripts executable
echo "🔧 Making scripts executable..."
chmod +x menubar_transcribe.py
chmod +x run_menubar.sh
echo "✅ Done"
echo ""

echo "=================================================="
echo "✅ Installation Complete!"
echo ""
echo "To start the menu bar app, run:"
echo "   ./run_menubar.sh"
echo ""
echo "You should see a 🎙️ icon appear in your menu bar!"
echo ""
echo "For more information, see MENUBAR_SETUP.md"
echo "=================================================="
