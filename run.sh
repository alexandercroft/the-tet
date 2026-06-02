#!/bin/bash
set -e
cd "$(dirname "$0")"

# --- system tools ---
missing=""
command -v python3 >/dev/null 2>&1 || missing="$missing python3"
command -v ffmpeg  >/dev/null 2>&1 || missing="$missing ffmpeg"
if [ -n "$missing" ]; then
  echo "Missing required tools:$missing"
  command -v brew >/dev/null 2>&1 && echo "Install with:  brew install$missing" \
    || echo "Please install:$missing"
  exit 1
fi

# --- python env + deps ---
if [ ! -d venv ]; then
  echo "Setting up virtual environment..."
  python3 -m venv venv
  source venv/bin/activate
  pip install -q --upgrade pip
  pip install -q -r requirements.txt
  echo "Installing Chromium for Threads..."
  python -m playwright install chromium
else
  source venv/bin/activate
fi

PORT="${PORT:-8900}"
export PORT
echo ""
echo "  The TET is running at http://127.0.0.1:$PORT"
echo ""
python app.py
