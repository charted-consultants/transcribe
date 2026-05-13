#!/bin/bash

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FACTORY_TECH_DIR="/Users/dakthi/Documents/Factory-Tech"

# Activate centralized virtual environment and run the menu bar app
source "$FACTORY_TECH_DIR/.venv/bin/activate"
# Load secrets from local env file (not committed)
[ -f "$DIR/.env" ] && export $(grep -v '^#' "$DIR/.env" | xargs)
python3 "$DIR/menubar_transcribe.py"
