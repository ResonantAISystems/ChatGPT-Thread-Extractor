#!/bin/bash
# Launch ChatGPT Thread Extractor GUI

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    python3 extractor_gui.py
elif command -v python &> /dev/null; then
    python extractor_gui.py
else
    echo "Error: Python not found"
    echo "Please install Python 3.6 or higher"
    exit 1
fi
