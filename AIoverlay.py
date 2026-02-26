#!/usr/bin/env python3
"""
AI Desktop - Floating launcher for Gemini, Claude, ChatGPT, DeepSeek, Qwen.

Uses the REAL Google Chrome in --app mode.
Google login works perfectly because it IS real Chrome.

A floating control bar provides access to each AI model.
"""

import sys
import os
import subprocess
import signal
import time
from pathlib import Path

from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QColor, QCursor, QFont, QPalette, QIcon, QPainter, QBrush, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QMessageBox
)

# ─── Constants ──────────────────────────────────────────────────────────────
APP_NAME = "AI Desktop"
CHROME_DATA_DIR = os.path.join(str(Path.home()), ".ai-desktop-chrome")

# Window size for AI model windows — always enforced
WIN_W = 520
WIN_H = 780

# ─── AI Models ──────────────────────────────────────────────────────────────
# Each entry: (name, url, emoji_icon, accent_color, tooltip)
AI_MODELS = [
    ("Gemini",   "https://gemini.google.com/app",      "✦",  "#8ab4f8", "Apri Google Gemini"),
    ("Claude",   "https://claude.ai/new",               "◈",  "#c192ff", "Apri Anthropic Claude"),
    ("ChatGPT",  "https://chatgpt.com/",                "⬡",  "#19c37d", "Apri OpenAI ChatGPT"),
    ("DeepSeek", "https://chat.deepseek.com/",          "⟡",  "#4d9de0", "Apri DeepSeek"),
    ("Qwen",     "https://chat.qwen.ai/",               "❋",  "#ff7b54", "Apri Qwen (Alibaba)"),
]

# ─── Colors ─────────────────────────────────────────────────────────────────
BG      = "#1a1a1a"
BG2     = "#242424"
TEXT_P  = "#e8eaed"
TEXT_D  = "#9aa0a6"
BORDER  = "#363636"
BTN_H   = "#2e2e2e"
BTN_PR  = "#3a3a3a"
PIN_ON  = "#f9c74f"


def find_chrome():
    """Find Chrome executable."""
    for name in ["google-chrome-stable", "google-chrome", "chromium-browser", "chromium"]:
        try:
            r = subprocess.run(["which", name], capture_output=True, text=True, timeout=3)
            if r.returncode == 0:
                return r.stdout.strip()
        except Exception:
            pass
    return None


class AILauncherBar(QWidget):
    """Floating launcher bar with buttons for each AI model."""

    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self._pinned = False

        self._setup_ui()
        self._position_panel()

        # Auto-launch Gemini on startup
        self._open_model(AI_MODELS[0])

    # ── UI Setup ────────────────────────────────────────────────────────────

    def _setup_ui(self):
        self._update_window_flags(pinned=False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Fixed height, width will be set after building layout
        self.setFixedHeight(52)

        self.setStyleSheet(f"""
            QWidget#bar {{
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2a2a2a, stop:1 {BG}
                );
                border: 1px solid {BORDER};
                border-radius: 26px;
            }}
        """)

        # Use a named inner widget so border-radius applies correctly
        self._bar = QWidget(self)
        self._bar.setObjectName("bar")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(self._bar)

        layout = QHBoxLayout(self._bar)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(4)

        # ── AI model buttons ────────────────────────────────────────────
        for model in AI_MODELS:
            btn = self._model_btn(model)
            layout.addWidget(btn)

        # ── Separator ───────────────────────────────────────────────────
        sep = QLabel("│")
        sep.setStyleSheet(f"color: {BORDER}; border: none; font-size: 16px; margin: 0 4px;")
        layout.addWidget(sep)

        # ── Pin button ──────────────────────────────────────────────────
        self.btn_pin = self._icon_btn("📌", "Primo piano: OFF")
        self.btn_pin.clicked.connect(self._toggle_pin)
        layout.addWidget(self.btn_pin)

        # ── Close button ─────────────────────────────────────────────────
        self.btn_close = self._icon_btn("✕", "Chiudi tutto")
        self.btn_close.setStyleSheet(self.btn_close.styleSheet() +
                                     f" QPushButton {{ color: #ff6b6b; }}"
                                     f" QPushButton:hover {{ color: #ff4444; }}")
        self.btn_close.clicked.connect(self._close_all)
        layout.addWidget(self.btn_close)

        self.adjustSize()
        self.setFixedWidth(self._bar.sizeHint().width() + 28)
        self._bar.setGeometry(0, 0, self.width(), self.height())

    def _model_btn(self, model):
        """Create a vertical button for an AI model (icon + label)."""
        name, url, icon, color, tip = model

        btn = QPushButton()
        btn.setToolTip(tip)
        btn.setFixedSize(52, 40)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # Two-line content: emoji + label
        btn.setText(f"{icon}\n{name}")
        btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 10px;
                color: {color};
                font-size: 9px;
                font-weight: 700;
                font-family: 'Inter','Segoe UI','Roboto',sans-serif;
                padding: 2px 4px;
                line-height: 1.3;
            }}
            QPushButton:hover {{
                background: {BTN_H};
            }}
            QPushButton:pressed {{
                background: {BTN_PR};
            }}
        """)

        btn.clicked.connect(lambda checked, m=model: self._open_model(m))
        return btn

    def _icon_btn(self, icon, tip):
        """Small icon-only utility button."""
        b = QPushButton(icon)
        b.setToolTip(tip)
        b.setFixedSize(32, 32)
        b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        b.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
                border-radius: 8px;
                color: {TEXT_D};
                font-size: 14px;
                padding: 0;
            }}
            QPushButton:hover {{
                background: {BTN_H};
                color: {TEXT_P};
            }}
            QPushButton:pressed {{
                background: {BTN_PR};
            }}
        """)
        return b

    # ── Window management ────────────────────────────────────────────────────

    def _update_window_flags(self, pinned):
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    def _position_panel(self):
        screen = QApplication.primaryScreen()
        if screen:
            g = screen.availableGeometry()
            self.move((g.width() - self.width()) // 2 + g.x(), g.y() + 10)

    def resizeEvent(self, ev):
        super().resizeEvent(ev)
        if hasattr(self, '_bar'):
            self._bar.setGeometry(0, 0, self.width(), self.height())

    # ── AI model launcher ────────────────────────────────────────────────────

    def _open_model(self, model):
        """Open a Chrome --app window for the given AI model at a fixed size."""
        name, url, icon, color, tip = model
        chrome = find_chrome()
        if not chrome:
            QMessageBox.critical(self, "Errore",
                                 "Google Chrome non trovato!\nInstalla Chrome.")
            return

        os.makedirs(CHROME_DATA_DIR, exist_ok=True)

        cmd = [
            chrome,
            f"--app={url}",
            f"--user-data-dir={CHROME_DATA_DIR}",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-background-networking",
            f"--window-size={WIN_W},{WIN_H}",
            # Force the window to not be maximized regardless of saved state
            "--window-position=100,80",
            "--start-in-screenshot-mode",   # prevents restoring maximized state
            f"--class=ai-desktop-{name.lower()}",
        ]

        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid
        )
        print(f"[AI Desktop] Opened {name} — {url}")

    # ── Pin toggle ───────────────────────────────────────────────────────────

    def _toggle_pin(self):
        self._pinned = not self._pinned
        pos = self.pos()
        self._update_window_flags(self._pinned)
        self.move(pos)
        self.show()

        if self._pinned:
            self.btn_pin.setStyleSheet(
                self.btn_pin.styleSheet() +
                f" QPushButton {{ color: {PIN_ON}; }}"
            )
            self.btn_pin.setToolTip("Primo piano: ON")
        else:
            self.btn_pin.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; border: none; border-radius: 8px;
                    color: {TEXT_D}; font-size: 14px; padding: 0;
                }}
                QPushButton:hover {{ background: {BTN_H}; color: {TEXT_P}; }}
                QPushButton:pressed {{ background: {BTN_PR}; }}
            """)
            self.btn_pin.setToolTip("Primo piano: OFF")

    # ── Close ────────────────────────────────────────────────────────────────

    def _close_all(self):
        QApplication.quit()

    # ── Drag ─────────────────────────────────────────────────────────────────

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = ev.globalPosition().toPoint() - self.frameGeometry().topLeft()
            ev.accept()

    def mouseMoveEvent(self, ev):
        if self._drag_pos is not None:
            self.move(ev.globalPosition().toPoint() - self._drag_pos)
            ev.accept()

    def mouseReleaseEvent(self, ev):
        self._drag_pos = None
        ev.accept()

    def closeEvent(self, ev):
        self._close_all()
        ev.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(True)

    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(BG))
    p.setColor(QPalette.ColorRole.WindowText, QColor(TEXT_P))
    app.setPalette(p)

    f = QFont("Inter", 10)
    f.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(f)

    bar = AILauncherBar()
    bar.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
