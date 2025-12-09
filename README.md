# ChatGPT Thread Extractor

**A Python tool to extract and organize conversations from ChatGPT's exported data into readable formats for AI continuity and research.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## Overview

This tool parses ChatGPT's exported `conversations.json` file and provides flexible extraction options for conversation management, AI memory persistence, and research applications. Supports both individual file extraction and combined archive creation with smart duplicate detection.

**Current Status:** Production ready  
**Key Features:** GUI interface, archive mode with append logic, batch processing

---

## Key Features

**Extraction Modes**
- Individual files: Each conversation as separate text file
- Archive mode: Combined file with chronological ordering
- Smart append: Only adds new conversations to existing archives
- Dual output: Both modes simultaneously

**Data Management**
- Automatic duplicate detection via conversation IDs
- Chronological sorting (newest conversations first)
- Large file support (handles 200MB+ exports)
- Cross-platform filename sanitization

**User Interface**
- GUI application for easy use
- Command-line interface for automation
- Real-time progress tracking
- Comprehensive error handling

---

## Quick Start

### GUI Version (Recommended)

**Windows:** Double-click `launch_gui.bat`  
**Mac/Linux:** Run `./launch_gui.sh` or `python3 extractor_gui.py`

1. Select your `conversations.json` file
2. Choose extraction mode (Individual/Archive/Both)
3. Configure output options
4. Click "Extract Conversations"

### Command Line

```bash
# Archive mode (recommended for AI continuity)
python3 extractor.py conversations.json --archive

# Individual files
python3 extractor.py conversations.json --individual

# Both modes
python3 extractor.py conversations.json --individual --archive
```

---

## Getting Your Data

1. Log in to ChatGPT at https://chat.openai.com
2. Profile → Settings → Data controls → Export data
3. Download the ZIP file from the email link
4. Extract and locate `conversations.json`

---

## Configuration

**Archive Mode Options**
- Default filename: `chatgpt_archive.txt`
- Append mode: Only adds new conversations
- Fresh archive: `--no-append` flag overwrites existing
- Custom filename: `--archive custom_name.txt`

**Individual Files Options**
- Output directory: `--output-dir` (default: `chatgpt_conversations`)
- Filename format: `Title_ConversationID.txt`
- Automatic sanitization for cross-platform compatibility

**Advanced Options**
- Progress tracking for large exports
- UTF-8 encoding for international characters
- Stable conversation ID generation for deduplication

---

## Use Cases

**AI Memory Persistence**
Maintain conversation history across AI instance resets using archive mode with regular exports and appends.

**Conversation Backup**
Organize conversations as individual files for easy searching and categorization.

**Research Applications**
Extract conversation datasets for analysis, training, or research with both individual and archive formats.

**Development Workflows**
Integrate with automated systems using command-line interface for batch processing.

---

## Technical Details

**Supported Formats:** Array and dictionary JSON structures  
**Performance:** Optimized for large exports (200MB+ tested)  
**Dependencies:** Python 3.6+ with tkinter for GUI  
**Encoding:** UTF-8 with international character support  

**Archive Format:**
- Clear visual delimiters between conversations
- Metadata headers with timestamps and IDs
- Newest conversations first ordering
- Programmatically parseable structure

For detailed usage examples and customization options, see the [technical documentation](docs/).

---

## Project Structure

```
ChatGPT-Thread-Extractor/
├── extractor_gui.py          # GUI application
├── extractor.py              # CLI with archive support
├── launch_gui.bat/.sh        # Platform launchers
└── README.md                 # This file
```

---

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

---

**Part of the RAIS (Resonant AI Systems) community toolkit**  
For more information: https://resonantaisystems.com/

---

*Essential tool for AI conversation management, research, and continuity applications.*