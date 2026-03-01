# AI-Desktop-Launcher

A minimal, floating desktop launcher for the top 5 Artificial Intelligence models (Gemini, Claude, ChatGPT, DeepSeek, Qwen).
It runs as a native application using Google Chrome in `--app` mode, which means it keeps all your active sessions and logins (like Google or OpenAI) without requiring you to log in every time.

## Features

* **Floating Control Bar:** Sleek, minimal interface that sits nicely at the top of your screen.
* **5 AI Models Supported:** One-click pure app-window launch for Gemini, Anthropic Claude, OpenAI ChatGPT, DeepSeek, and Qwen.
* **Always on Top (Pin):** You can pin the launch bar so it stays above other windows.

## Requirements

* **Google Chrome** (or Chromium) installed on your system.
* Python 3
* PyQt6

## Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/YourUsername/YourRepoName.git
   cd AI-Desktop-Launcher
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   chmod +x run_AI-Desktop-Launcher.sh
   ./run_AI-Desktop-Launcher.sh
   # Or you can run it directly with python:
   python3 AI-Desktop-Launcher.py
   ```

### 🪟 Windows Setup

1. **Clone the repository:**
   Open Command Prompt (`cmd`) or PowerShell and type:

   ```cmd
   git clone https://github.com/Snowkills/AI-Desktop-Launcher.git
   cd AI-Desktop-Launcher
   ```

2. **Run the application:**
   Simply double-click on `run_AI-Desktop-Launcher.bat` from your File Explorer.
   The first time you run it, it will automatically create the virtual environment and install dependencies (`PyQt6`). It will then launch the application.

   *(Alternatively, you can manually run `python -m venv venv`, activate it with `venv\Scripts\activate`, `pip install -r requirements.txt`, and run `python AI-Desktop-Launcher.py`)*

## Adding to Application Menu (Linux)

If you want the application to show up in your system's application launcher (like GNOME or KDE menus), you need to configure the provided `.desktop` file:

1. Open the file `AI-Desktop-Launcher.desktop` with a text editor.
2. Find the line that says `Exec=/path/to/your/downloaded/folder/run_AI-Desktop-Launcher.sh`.
3. **Change it** to the *absolute path* of where you cloned this repository (e.g., `Exec=/home/your_username/Downloads/AI-Desktop/run_AI-Desktop-Launcher.sh`).
4. Copy the file into your local applications folder:

   ```bash
   cp AI-Desktop-Launcher.desktop ~/.local/share/applications/
   ```

## 📦 Pre-build Binaries & Self-Building (No Python Required)

Since GitHub repositories have a strict file size limit for direct uploads (25MB) which prevents us from uploading bulky compiled standalone files directly to the code, we use **GitHub Actions** and **local build scripts** to handle the large standalone executables (`.exe` and `.AppImage`).

### Option 1: Download Pre-built Releases (Recommended)

You do not need to compile the program yourself or install Python. Every time a new version is tagged, our GitHub Actions automatically build the `.exe` for Windows and the `.AppImage` for Linux.

* **Go to the [Releases page](../../releases)** of this repository.
* Download the `AI-Desktop-Launcher-x.x.x-windows.exe` for Windows or the `AI-Desktop-Launcher-x.x.x-linux.AppImage` for Linux.
* Simply double-click to run! (On Linux, make it executable first with `chmod +x`).

### Option 2: Self-Produce the Executables (Build Locally)

If you prefer to compile the standalone executables on your own machine, we provide easy-to-use scripts.

**For Linux (Creates an `.AppImage`):**

1. Make sure you have `python3`, `pip`, and `wget` installed.
2. Run the Linux build script:

   ```bash
   chmod +x crea_appimage_linux.sh
   ./crea_appimage_linux.sh
   ```

3. An `AI-Desktop-Launcher-x86_64.AppImage` will be generated in the root folder.

**For Windows (Creates an `.exe`):**

1. Make sure you have Python installed and added to your system PATH.
2. Double-click on `crea_exe_windows.bat` or run it via command prompt:

   ```cmd
   crea_exe_windows.bat
   ```

3. A standalone file `AI-Desktop-Launcher.exe` will be generated in the same folder.

### Option 3: Automatic Generation via AI (Claude / Antigravity)

**Note:** If you don't want to run the scripts locally or don't have the development environment to compile, you can provide the files in this repository (the `.py`, `.bat`, `.sh`, `.spec` and `requirements.txt` files) or the URL to this repo directly to an Artificial Intelligence like **Claude** or **Antigravity**.

Simply ask the AI:

* For Linux: *"Generate an AppImage executable starting from these files"*
* For Windows: *"Use these files to generate the .exe executable of this program for Windows"*

The assistant will automatically handle the compilation environment and provide you with the ready-to-use executable file!
