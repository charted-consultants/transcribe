#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FACTORY_TECH_DIR="/Users/dakthi/Documents/Factory-Tech"

# Activate centralized virtual environment and run the menu bar app
source "$FACTORY_TECH_DIR/.venv/bin/activate"
python3 "$DIR/menubar_transcribe.py"
