@echo off
echo [AI-Desktop-Launcher] Avvio in corso...
cd /d "%~dp0"

IF NOT EXIST "venv\Scripts\python.exe" (
    echo Creazione ambiente virtuale in corso...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installazione dipendenze...
    pip install -r requirements.txt
) ELSE (
    call venv\Scripts\activate.bat
)

start "" venv\Scripts\pythonw.exe AI-Desktop-Launcher.py
