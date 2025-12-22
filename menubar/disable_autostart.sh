#!/bin/bash

echo "🛑 Disabling auto-start for Live Transcription Menu Bar App"
echo "============================================================="
echo ""

PLIST_FILE="com.transcribe.menubar.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
DEST_PLIST="$LAUNCH_AGENTS_DIR/$PLIST_FILE"

# Check if LaunchAgent exists
if [ ! -f "$DEST_PLIST" ]; then
    echo "⚠️  Auto-start is not currently enabled"
    echo "LaunchAgent file not found at: $DEST_PLIST"
    exit 0
fi

# Unload the LaunchAgent
echo "🔄 Unloading LaunchAgent..."
launchctl unload "$DEST_PLIST"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent unloaded successfully"
else
    echo "⚠️  LaunchAgent may not have been running"
fi

# Remove the plist file
echo "🗑️  Removing LaunchAgent file..."
rm "$DEST_PLIST"

if [ $? -eq 0 ]; then
    echo "✅ LaunchAgent file removed"
else
    echo "❌ Failed to remove LaunchAgent file"
    exit 1
fi

echo ""
echo "============================================================="
echo "✅ Auto-start disabled!"
echo ""
echo "The menu bar app will no longer start automatically."
echo "You can still run it manually with: ./run_menubar.sh"
echo ""
echo "To re-enable auto-start, run: ./enable_autostart.sh"
echo "============================================================="
