#!/bin/bash
# Launch AI Desktop
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec "$SCRIPT_DIR/venv/bin/python3" "$SCRIPT_DIR/AIoverlay.py" "$@"
