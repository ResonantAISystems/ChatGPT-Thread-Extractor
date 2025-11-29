# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository extracts ChatGPT conversation histories from a large JSON export file into individual text files or a combined archive.

## Available Scripts

1. **`extractor_gui.py`** (Recommended for most users): Graphical interface with all features
2. **`extractor.py`** (CLI version): Full-featured command-line script with archive and individual file modes
3. **`extract_conversations.py`** (Legacy): Basic CLI script for individual files only
4. **`launch_gui.bat`** (Windows): Batch file launcher for the GUI

## Data Structure

The `conversations.json` file (217.5MB) contains an array of 250 conversation objects. Each conversation has:
- `title`: Conversation title
- `create_time` / `update_time`: Unix timestamps
- `mapping`: Tree structure of messages with parent-child relationships
- Message nodes containing author roles (user/assistant/system), content, and metadata

## Extracting Conversations

### Basic Usage

Run the extraction script:
```bash
python extract_conversations.py
```

This will:
- Parse `conversations.json`
- Create a `conversations_output/` directory
- Generate individual `.txt` files for each conversation
- Name files as: `YYYY-MM-DD__YYYY-MM-DD_Title.txt` (create date, update date, sanitized title)

### Output Format

Each extracted text file contains:
```
Title: [conversation title]
Created: [timestamp]
Updated: [timestamp]
================================================================================

[USER]
[message content]

--------------------------------------------------------------------------------

[ASSISTANT]
[message content]

--------------------------------------------------------------------------------
```

## Code Architecture

### extract_conversations.py

The extraction script has four main functions:

1. **`traverse_messages(mapping, node_id, visited=None)`**
   - Recursively walks the message tree structure
   - Extracts messages in depth-first order
   - Filters out empty system messages
   - Returns list of message dictionaries with role and text

2. **`format_conversation(conversation)`**
   - Takes a conversation object
   - Formats header with title and timestamps
   - Traverses message tree starting from root nodes
   - Outputs formatted text with role labels and separators

3. **`sanitize_filename(filename)`**
   - Removes invalid filename characters (`<>:"/\|?*`)
   - Strips control characters
   - Truncates to 200 characters for Windows compatibility

4. **`extract_conversations(json_file, output_dir='conversations_output')`**
   - Main entry point
   - Loads the entire JSON file into memory
   - Iterates through conversations
   - Creates output directory and files
   - Displays progress every 100 conversations

### Key Implementation Notes

- The JSON file is loaded entirely into memory (works for files up to ~250MB)
- Message trees are traversed starting from root nodes (nodes with `parent: null`)
- The `mapping` object uses UUIDs as keys to link parent-child message relationships
- Empty system messages and metadata-only content are filtered out
- Files are encoded as UTF-8 to handle special characters

### extractor.py (Main Script)

The enhanced extractor script adds archive mode and improved flexibility:

**Key Features:**
- **Dual output modes**: Individual files AND/OR combined archive
- **Archive append logic**: Detects existing conversations by ID to avoid duplicates
- **Flexible data format**: Handles both array and dictionary JSON formats
- **Generated conversation IDs**: Uses hash of `create_time` + `title` for stable IDs

**Main Functions:**
1. **`write_archive(conversations_data, archive_path, append=True)`**
   - Creates or appends to archive file
   - Parses existing archive to extract conversation IDs
   - Filters out already-archived conversations
   - Sorts by creation time (newest first)

2. **`write_individual_files(conversations_data, output_dir)`**
   - Creates individual text files per conversation
   - Names files: `YYYY-MM-DD__YYYY-MM-DD_Title_ConversationID.txt` (create date, update date, sanitized title, ID is first 8 chars of hash)

3. **`create_archive_entry(conversation, conversation_id)`**
   - Formats conversation with metadata header containing ID
   - Used for deduplication on subsequent runs

**Command-line Usage:**
```bash
# Archive mode (recommended)
python extractor.py conversations.json --archive

# Individual files
python extractor.py conversations.json --individual

# Both modes simultaneously
python extractor.py conversations.json --individual --archive
```

### Modifying the Script

**Change output directory:**
```python
extract_conversations('conversations.json', output_dir='my_custom_dir')
```

**Change filename format:**
Edit the filename construction in `extract_conversations()`:
```python
filename = f"{create_date}__{update_date}_{safe_title}.txt"
```

**Filter specific conversations:**
Add filtering logic in the main loop:
```python
for conversation in conversations:
    if conversation.get('create_time') > some_timestamp:
        # process conversation
```

**Change message format:**
Modify the output formatting in `format_conversation()` to adjust separators, add timestamps per message, etc.
