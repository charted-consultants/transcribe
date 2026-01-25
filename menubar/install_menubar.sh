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

# Use centralized Factory-Tech virtual environment
FACTORY_TECH_DIR="/Users/dakthi/Documents/Factory-Tech"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TRANSCRIBE_APP_DIR="$( cd "$DIR/.." && pwd )"

# Check if centralized venv exists
if [ ! -d "$FACTORY_TECH_DIR/.venv" ]; then
    echo "❌ Centralized virtual environment not found at $FACTORY_TECH_DIR/.venv"
    echo "Creating centralized venv..."
    cd "$FACTORY_TECH_DIR"
    python3 -m venv .venv
    echo "✅ Centralized virtual environment created"
fi

echo ""

# Activate virtual environment and install packages
echo "📦 Installing dependencies from requirements.txt..."
source "$FACTORY_TECH_DIR/.venv/bin/activate"

# Install from requirements.txt
cd "$TRANSCRIBE_APP_DIR"
pip install --upgrade pip
pip install -r requirements.txt

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
