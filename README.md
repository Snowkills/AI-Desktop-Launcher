# AI Desktop Launcher

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
   cd YourRepoName
   ```

2. **Create a virtual environment and install dependencies:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   chmod +x run_AIoverlay.sh
   ./run_AIoverlay.sh
   # Or you can run it directly with python:
   python3 AIoverlay.py
   ```

### 🪟 Windows Setup

1. **Clone the repository:**
   Open Command Prompt (`cmd`) or PowerShell and type:

   ```cmd
   git clone https://github.com/Snowkills/AI-Desktop-Launcher.git
   cd AI-Desktop-Launcher
   ```

2. **Run the application:**
   Simply double-click on `run_AIoverlay.bat` from your File Explorer.
   The first time you run it, it will automatically create the virtual environment and install dependencies (`PyQt6`). It will then launch the application.

   *(Alternatively, you can manually run `python -m venv venv`, activate it with `venv\Scripts\activate`, `pip install -r requirements.txt`, and run `python AIoverlay.py`)*

## Adding to Application Menu (Linux)

If you want the application to show up in your system's application launcher (like GNOME or KDE menus), you need to configure the provided `.desktop` file:

1. Open the file `AIoverlay.desktop` with a text editor.
2. Find the line that says `Exec=/path/to/your/downloaded/folder/run_AIoverlay.sh`.
3. **Change it** to the *absolute path* of where you cloned this repository (e.g., `Exec=/home/your_username/Downloads/AI-Desktop/run_AIoverlay.sh`).
4. Copy the file into your local applications folder:

   ```bash
   cp AIoverlay.desktop ~/.local/share/applications/
   ```
