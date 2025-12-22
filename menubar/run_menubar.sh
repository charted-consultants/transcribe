#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DIR="$( cd "$DIR/.." && pwd )"

# Activate virtual environment and run the menu bar app
source "$ROOT_DIR/venv/bin/activate"
python3 "$DIR/menubar_transcribe.py"
