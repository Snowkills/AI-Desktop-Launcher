#!/bin/bash
# ============================================================
#  build_appimage.sh — Build AI Desktop Launcher AppImage
#  Usage:  bash build_appimage.sh
# ============================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="AIDesktopLauncher"
APP_VERSION="1.0.0"
ARCH="$(uname -m)"           # x86_64 or aarch64
APPDIR="$SCRIPT_DIR/AppDir"
DIST_DIR="$SCRIPT_DIR/dist"

echo "=============================="
echo " AI Desktop Launcher — AppImage builder"
echo " Arch: $ARCH"
echo "=============================="

# ── 1. Install / check dependencies ─────────────────────────────────────────
echo "[1/5] Checking dependencies..."

if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "  → Installing PyQt6..."
    pip3 install --quiet PyQt6
fi

if ! python3 -m PyInstaller --version &>/dev/null; then
    echo "  → Installing PyInstaller..."
    pip3 install --quiet pyinstaller
fi

# ── 2. Download appimagetool if missing ──────────────────────────────────────
TOOL="$SCRIPT_DIR/appimagetool-${ARCH}.AppImage"
if [ ! -f "$TOOL" ]; then
    echo "[2/5] Downloading appimagetool..."
    TOOL_URL="https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-${ARCH}.AppImage"
    curl -sSL -o "$TOOL" "$TOOL_URL"
    chmod +x "$TOOL"
else
    echo "[2/5] appimagetool already present."
fi

# ── 3. Build with PyInstaller ────────────────────────────────────────────────
echo "[3/5] Running PyInstaller..."
cd "$SCRIPT_DIR"
python3 -m PyInstaller --clean AIoverlay.spec

# ── 4. Create AppDir structure ───────────────────────────────────────────────
echo "[4/5] Creating AppDir structure..."
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"
mkdir -p "$APPDIR/usr/share/applications"
mkdir -p "$APPDIR/usr/share/icons/hicolor/256x256/apps"

# Copy the PyInstaller single-file binary
cp "$DIST_DIR/$APP_NAME" "$APPDIR/usr/bin/$APP_NAME"
chmod +x "$APPDIR/usr/bin/$APP_NAME"

# AppRun — entry point required by AppImage
cat > "$APPDIR/AppRun" << 'EOF'
#!/bin/bash
HERE="$(dirname "$(readlink -f "$0")")"
exec "$HERE/usr/bin/AIDesktopLauncher" "$@"
EOF
chmod +x "$APPDIR/AppRun"

# Desktop file (required by appimagetool)
cat > "$APPDIR/AIDesktopLauncher.desktop" << EOF
[Desktop Entry]
Name=AI Desktop Launcher
Comment=Floating launcher for top AI models
Exec=AIDesktopLauncher
Icon=AIDesktopLauncher
Type=Application
Terminal=false
Categories=Utility;Network;
StartupWMClass=AIDesktopLauncher
EOF

# Also copy to usr/share
cp "$APPDIR/AIDesktopLauncher.desktop" "$APPDIR/usr/share/applications/"

# Icon: generate a simple SVG if no icon provided
ICON_TARGET="$APPDIR/AIDesktopLauncher.png"
if [ ! -f "$ICON_TARGET" ]; then
    # Try to copy from repo, else create a placeholder
    if [ -f "$SCRIPT_DIR/icon.png" ]; then
        cp "$SCRIPT_DIR/icon.png" "$ICON_TARGET"
        cp "$SCRIPT_DIR/icon.png" "$APPDIR/usr/share/icons/hicolor/256x256/apps/AIDesktopLauncher.png"
    else
        # Create a minimal placeholder via Python
        python3 - << 'PYEOF'
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
    from PyQt6.QtCore import Qt
    import sys
    app = QApplication(sys.argv)
    pm = QPixmap(256, 256)
    pm.fill(QColor('#1a1a1a'))
    painter = QPainter(pm)
    painter.setPen(QColor('#8ab4f8'))
    font = QFont('Arial', 80, QFont.Weight.Bold)
    painter.setFont(font)
    painter.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, '✦')
    painter.end()
    pm.save('AppDir/AIDesktopLauncher.png')
    pm.save('AppDir/usr/share/icons/hicolor/256x256/apps/AIDesktopLauncher.png')
    print("  → Icon created via PyQt6")
except Exception as e:
    print(f"  → Icon creation skipped: {e}")
    # Touch an empty png so appimagetool doesn't fail
    open('AppDir/AIDesktopLauncher.png', 'wb').write(b'')
    open('AppDir/usr/share/icons/hicolor/256x256/apps/AIDesktopLauncher.png', 'wb').write(b'')
PYEOF
    fi
fi

# ── 5. Package into AppImage ─────────────────────────────────────────────────
echo "[5/5] Packaging AppImage..."
OUTPUT_FILE="${APP_NAME}-${APP_VERSION}-${ARCH}.AppImage"

ARCH="$ARCH" "$TOOL" --no-appstream "$APPDIR" "$OUTPUT_FILE"

echo ""
echo "✅ Done! AppImage created: $OUTPUT_FILE"
echo "   Make it executable and run it:"
echo "   chmod +x $OUTPUT_FILE && ./$OUTPUT_FILE"
