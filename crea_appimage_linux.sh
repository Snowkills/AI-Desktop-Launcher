#!/bin/bash
# Script per creare l'AppImage su Linux per AI-Desktop-Launcher

set -e

echo "======================================"
echo "    Creazione AppImage (Linux)        "
echo "======================================"

# Verifica dei prerequisiti
if ! command -v python3 &> /dev/null; then
    echo "Errore: python3 non trovato!"
    exit 1
fi
if ! command -v pyinstaller &> /dev/null; then
    echo "Errore: pyinstaller non trovato! Installalo con: pip install pyinstaller PyQt6"
    exit 1
fi
if ! command -v wget &> /dev/null; then
    echo "Errore: wget non trovato!"
    exit 1
fi

echo "1) Creazione dell'eseguibile singolo (binario) con PyInstaller..."
pyinstaller --clean AI-Desktop-Launcher.spec
mv dist/AI-Desktop-Launcher ./AI-Desktop-Launcher-bin

echo "2) Strutturazione della cartella AppDir..."
mkdir -p AppDir/usr/bin
cp AI-Desktop-Launcher-bin AppDir/usr/bin/AI-Desktop-Launcher
chmod +x AppDir/usr/bin/AI-Desktop-Launcher

# Creazione del file .desktop all'interno dell'AppDir
cat << 'EOF' > AppDir/AI-Desktop-Launcher.desktop
[Desktop Entry]
Type=Application
Name=AI-Desktop-Launcher
Exec=AI-Desktop-Launcher
Icon=AI-Desktop-Launcher
Categories=Utility;
EOF

# Creazione AppRun (richiesto da AppImageTool)
ln -s usr/bin/AI-Desktop-Launcher AppDir/AppRun

# Creazione di un'icona vuota fittizia per AppDir
touch AppDir/AI-Desktop-Launcher.png

# Download di appimagetool se non presente
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    echo "3) Download di appimagetool..."
    wget -q https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

echo "4) Creazione finale dell'AppImage..."
./appimagetool-x86_64.AppImage AppDir AI-Desktop-Launcher-x86_64.AppImage

echo "======================================"
echo "Completato! File generato: AI-Desktop-Launcher-x86_64.AppImage"
echo "Puoi avviarlo con: ./AI-Desktop-Launcher-x86_64.AppImage"
echo "======================================"

# Pulizia temporanea
rm AI-Desktop-Launcher-bin
rm -rf AppDir
rm -rf build
