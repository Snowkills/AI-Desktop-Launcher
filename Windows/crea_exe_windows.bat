@echo off
echo ======================================
echo    Creazione EXE (Windows)
echo ======================================

:: Verifica dei prerequisiti
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Errore: Python non trovato.
    exit /b 1
)

pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Errore: PyInstaller non trovato! Installalo con: pip install pyinstaller PyQt6
    exit /b 1
)

echo 1) Creazione dell'eseguibile con PyInstaller...
pyinstaller --clean AI-Desktop-Launcher.spec

echo 2) Spostamento dell'eseguibile nella cartella principale...
move dist\AI-Desktop-Launcher.exe AI-Desktop-Launcher.exe

echo 3) Pulizia dei file temporanei...
rmdir /S /Q build
rmdir /S /Q dist

echo ======================================
echo Completato! File generato: AI-Desktop-Launcher.exe
echo Puoi avviarlo facendo doppio clic su di esso.
echo ======================================
pause
