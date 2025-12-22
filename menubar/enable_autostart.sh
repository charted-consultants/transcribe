#!/bin/bash

echo "🚀 Setting up auto-start for Live Transcription Menu Bar App"
echo "============================================================="
echo ""

PLIST_FILE="com.transcribe.menubar.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
DEST_PLIST="$LAUNCH_AGENTS_DIR/$PLIST_FILE"

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy the plist file
echo "📋 Installing LaunchAgent..."
cp "$PLIST_FILE" "$DEST_PLIST"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent file installed to: $DEST_PLIST"
else
    echo "❌ Failed to copy LaunchAgent file"
    exit 1
fi

echo ""

# Unload if already loaded (to avoid errors)
launchctl unload "$DEST_PLIST" 2>/dev/null

# Load the LaunchAgent
echo "🔄 Loading LaunchAgent..."
launchctl load "$DEST_PLIST"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent loaded successfully"
else
    echo "❌ Failed to load LaunchAgent"
    exit 1
fi

echo ""
echo "============================================================="
echo "✅ Auto-start enabled!"
echo ""
echo "The menu bar app will now:"
echo "  • Start automatically when you log in"
echo "  • Show the 🎙️ icon in your menu bar"
echo "  • Run in the background until you quit it"
echo ""
echo "You should see the 🎙️ icon appear in your menu bar shortly."
echo ""
echo "To disable auto-start, run: ./disable_autostart.sh"
echo "============================================================="
