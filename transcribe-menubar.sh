#!/bin/bash

# Quick launcher for Transcribe Menubar App
FACTORY_TECH_DIR="/Users/dakthi/Documents/Factory-Tech"
APP_DIR="$FACTORY_TECH_DIR/tools/transcribe-app"

cd "$APP_DIR"
"$FACTORY_TECH_DIR/.venv/bin/python3" "$APP_DIR/menubar/menubar_transcribe.py"
