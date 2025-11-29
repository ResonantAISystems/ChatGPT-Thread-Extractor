# ChatGPT Thread Extractor

A Python tool to extract conversations from ChatGPT's exported conversation data into readable text files or a combined archive.

## Overview

This tool parses the `conversations.json` file exported from ChatGPT and provides two extraction modes:
- **Individual Files**: Each conversation saved as a separate text file
- **Archive Mode**: All conversations in a single file, newest-first, with append support for incremental updates

## Features

- **Dual output modes**: Individual files or combined archive
- **Smart append logic**: Archive mode only adds new conversations
- **Chronological sorting**: Newest conversations first in archive
- **Clean delimiters**: Clear visual separation between conversations
- **Metadata headers**: Timestamp, title, and conversation ID for each entry
- **Filename sanitization**: Safe filenames across platforms
- **Large file support**: Handles 200MB+ JSON exports
- **Progress tracking**: Shows extraction progress and statistics

## Prerequisites

- Python 3.6 or higher (includes tkinter for GUI)
- Your ChatGPT conversations export file (`conversations.json`)

## Quick Start

### GUI Version (Recommended for Beginners)

Double-click `launch_gui.bat` (Windows) or run:
```bash
python extractor_gui.py
```

The GUI provides:
- Easy file selection with browse buttons
- Visual mode selection (Individual Files / Archive / Both)
- Real-time progress logging
- No command-line knowledge required

### Command-Line Version (Advanced Users)

See the "Usage" section below for CLI examples.

## Getting Your Conversation Data

1. Log in to ChatGPT at https://chat.openai.com
2. Click on your profile icon (bottom left)
3. Go to Settings → Data controls
4. Click "Export data"
5. Wait for the email with your download link
6. Download and extract the ZIP file
7. Locate the `conversations.json` file

## Usage

### Archive Mode (Recommended for Continuity)

Create or append to a combined archive file:

```bash
# Create/append to archive (default: chatgpt_archive.txt)
python3 extractor.py conversations.json --archive

# Specify custom archive filename
python3 extractor.py conversations.json --archive my_archive.txt

# Force fresh archive (don't append)
python3 extractor.py conversations.json --archive --no-append
```

**Archive behavior:**
- Checks for existing conversations by ID
- Only appends new conversations
- Maintains newest-first chronological order
- Shows count of existing vs. new conversations

### Individual Files Mode

Extract each conversation to a separate text file:

```bash
# Individual files only (default if no --archive)
python3 extractor.py conversations.json

# Specify custom output directory
python3 extractor.py conversations.json --individual --output-dir my_conversations
```

### Combined Mode

Do both simultaneously:

```bash
python3 extractor.py conversations.json --individual --archive chatgpt_archive.txt
```

## Command-Line Options

```
positional arguments:
  input_file            Path to conversations.json file

optional arguments:
  -h, --help            Show help message
  --individual, -i      Output individual text files
  --archive, -a [FILE]  Output combined archive file
  --no-append           Create fresh archive instead of appending
  --output-dir, -o DIR  Output directory for individual files
                        (default: chatgpt_conversations)
```

## Output Formats

### Archive Format

```
================================================================================
CONVERSATION: Understanding Quantum Entanglement
Date: 2025-11-27T14:23:45
ID: abc123def456
================================================================================

Title: Understanding Quantum Entanglement
================================================================================

USER:
Can you explain quantum entanglement?

ASSISTANT:
Quantum entanglement is a phenomenon where two or more particles...

================================================================================

================================================================================
CONVERSATION: [Next conversation...]
Date: 2025-11-26T09:15:32
ID: xyz789uvw012
================================================================================
...
```

**Archive features:**
- Clear visual delimiters (80-character separator lines)
- Conversation metadata in header (title, date, ID)
- Full conversation content preserved
- Newest conversations at top
- Easy to parse programmatically
- Works well with `tail` for recent context

### Individual File Format

Each conversation saved as separate `.txt` file:

```
Title: Understanding Quantum Entanglement
================================================================================

USER:
Can you explain quantum entanglement?

ASSISTANT:
Quantum entanglement is a phenomenon where two or more particles...
```

**Filename format:** `Title_ConversationID.txt`

Example: `Understanding_Quantum_Entanglement_abc123de.txt`

## Use Cases

### AI Memory Persistence
Use archive mode to maintain conversation history across AI instance resets:

```bash
# Regular export and append
python3 extractor.py conversations.json --archive ai_memory.txt

# Load recent context (last 250 lines)
tail -n 250 ai_memory.txt
```

### Conversation Backup
Individual files for organizing and searching:

```bash
python3 extractor.py conversations.json --individual --output-dir backup_2025
```

### Development & Research
Both modes for flexibility:

```bash
python3 extractor.py conversations.json --individual --archive research_corpus.txt
```

## Technical Details

### Data Format Support

The script automatically handles both data formats:
- **Array format**: `[{conversation1}, {conversation2}, ...]` (standard ChatGPT export)
- **Dictionary format**: `{"id1": {conversation1}, "id2": {conversation2}, ...}` (alternative format)

For array format, stable conversation IDs are generated from the conversation's creation timestamp and title.

### Archive Append Logic

1. Parse existing archive for conversation IDs (from metadata headers)
2. Load all conversations from `conversations.json`
3. Filter to only conversations not in archive
4. Sort all conversations by creation time (newest first)
5. Append new conversations with proper delimiters

### Performance

- Tested with 200MB+ JSON files
- Archive append is incremental (doesn't rewrite existing entries)
- Efficient ID parsing using regex on metadata headers
- UTF-8 encoding for international character support

### Conversation ID Extraction

The script generates stable conversation IDs using a hash of the conversation's creation timestamp and title. These IDs are consistent across exports (same conversation = same ID) and are used to detect duplicates. IDs are written to archive metadata headers and parsed on subsequent runs to determine which conversations are new.

## GUI Usage Guide

### Launching the GUI

**Windows:**
- Double-click `launch_gui.bat`
- Or run: `python extractor_gui.py`

**Mac/Linux:**
- Run: `./launch_gui.sh`
- Or: `python3 extractor_gui.py`

### Using the GUI

1. **Select Input File**: Click "Browse..." next to "Input File" and select your `conversations.json`

2. **Choose Output Mode**:
   - **Individual Files**: Extracts each conversation to a separate .txt file
   - **Archive File**: Creates/appends to a single combined archive
   - **Both**: Does both simultaneously

3. **Configure Options**:
   - **Output Directory**: Where individual files will be saved (if using Individual/Both modes)
   - **Archive File**: Archive filename (if using Archive/Both modes)
   - **Create fresh archive**: Check to overwrite existing archive instead of appending

4. **Click "Extract Conversations"**: Progress and results appear in the log window

### GUI Features

- **Smart defaults**: Pre-configured with recommended settings
- **Real-time logging**: See exactly what's happening during extraction
- **Error handling**: Clear error messages if something goes wrong
- **Thread-safe**: UI remains responsive during extraction
- **No installation**: Uses Python's built-in tkinter library

## Project Structure

```
ChatGPT-Thread-Extractor/
├── extractor_gui.py              # GUI application (recommended)
├── launch_gui.bat                # Windows launcher for GUI
├── launch_gui.sh                 # Mac/Linux launcher for GUI
├── extractor.py                  # CLI script (archive + individual modes)
├── extract_conversations.py      # Legacy CLI script (individual files only)
├── README.md                     # This file
├── CLAUDE.md                     # Instructions for Claude Code
├── LICENSE                       # MIT License
└── conversations.json            # Your export (not in repo)
```

## Examples

### Workflow for AI Continuity

```bash
# Initial export
python3 extractor.py conversations.json --archive memory_archive.txt
# Output: Wrote 150 conversations to memory_archive.txt

# Week later, new export
python3 extractor.py conversations_new.json --archive memory_archive.txt
# Output: Found 150 existing conversations in archive
#         Found 12 new conversations to add
#         Appended 12 conversations to memory_archive.txt

# Load recent context for AI boot
tail -n 250 memory_archive.txt
```

### Organizing by Date Range

For individual files with date filtering, you can modify the script or filter the JSON before processing. See **Customization** section below.

## Customization

### Change Default Archive Name

Modify the `--archive` default in the script:

```python
parser.add_argument('--archive', '-a', nargs='?', const='my_default_archive.txt',
                    help='Output combined archive file')
```

### Filter by Date Range

To only extract conversations from a specific time period:

```python
# In write_archive() or write_individual_files(), add:
from datetime import datetime

# Filter conversations created after January 1, 2025
cutoff = datetime(2025, 1, 1).timestamp()
filtered_convos = [c for c in all_conversations if c['create_time'] >= cutoff]
```

### Custom Delimiter Format

Modify `create_archive_entry()` to change the archive entry format:

```python
def create_archive_entry(conversation, conversation_id):
    # Your custom format here
    lines.append("### NEW CONVERSATION ###")
    # ... rest of formatting
```

## Notes

- `conversations.json` is excluded from version control (listed in `.gitignore`)
- Archive mode preserves all conversation content (same as individual files)
- Conversation IDs are stable across exports (safe for deduplication)
- Archive files can grow large; consider periodic archiving by date range
- The script handles special characters and emoji in titles/content

## Migration from Individual Files

If you have existing individual files and want to create an archive:

```bash
# Create fresh archive from new export
python3 extractor.py conversations.json --archive --no-append

# Future exports append automatically
python3 extractor.py new_export.json --archive
```

## Troubleshooting

**"No new conversations to add to archive"**
- All conversations in JSON are already in archive
- This is normal for unchanged exports

**Archive appears empty or truncated**
- Check file encoding (should be UTF-8)
- Verify conversations.json is valid JSON
- Try `--no-append` to regenerate fresh archive

**Filename sanitization issues**
- Script automatically removes unsafe characters
- Long titles are truncated to 100 characters
- Conversation ID suffix ensures uniqueness

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please:
- Open issues for bugs or feature requests
- Submit pull requests with clear descriptions
- Maintain backward compatibility with existing archives

## Related Projects

- [Sovereign AI Collective](https://github.com/ResonantAISystems/Continuity-Project) - AI continuity architecture using this tool for memory persistence
