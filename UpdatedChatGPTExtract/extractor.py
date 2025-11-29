#!/usr/bin/env python3
"""
ChatGPT Thread Extractor - Enhanced Version
Extracts conversations from ChatGPT's conversations.json export
Supports both individual files and combined archive modes
"""

import json
import os
import re
import argparse
import hashlib
from datetime import datetime
from pathlib import Path


def sanitize_filename(title, max_length=100):
    """Convert conversation title to safe filename"""
    # Remove or replace unsafe characters
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace spaces and multiple spaces with single underscore
    safe_title = re.sub(r'\s+', '_', safe_title)
    # Truncate if too long
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length]
    # Remove trailing dots and spaces
    safe_title = safe_title.rstrip('. ')
    return safe_title if safe_title else 'untitled'


def extract_conversation_text(conversation):
    """Extract text content from conversation structure"""
    lines = []
    
    # Add title as header
    title = conversation.get('title', 'Untitled Conversation')
    lines.append(f"Title: {title}\n")
    lines.append("=" * 80 + "\n\n")
    
    # Process messages
    mapping = conversation.get('mapping', {})
    
    # Build message tree and extract in order
    messages = []
    for node_id, node in mapping.items():
        message = node.get('message')
        if message and message.get('content'):
            content = message.get('content', {})
            parts = content.get('parts', [])
            author_role = message.get('author', {}).get('role', 'unknown')
            
            if parts and any(parts):  # Has actual content
                text = '\n'.join(str(part) for part in parts if part)
                if text.strip():
                    messages.append({
                        'role': author_role,
                        'text': text,
                        'create_time': message.get('create_time')
                    })
    
    # Sort by creation time
    messages.sort(key=lambda x: x.get('create_time', 0))
    
    # Format messages
    for msg in messages:
        role = msg['role'].upper()
        if role == 'USER':
            lines.append(f"USER:\n{msg['text']}\n\n")
        elif role == 'ASSISTANT':
            lines.append(f"ASSISTANT:\n{msg['text']}\n\n")
        elif role == 'SYSTEM':
            lines.append(f"SYSTEM:\n{msg['text']}\n\n")
    
    return ''.join(lines)


def parse_existing_archive(archive_path):
    """Parse existing archive file to extract conversation IDs already present"""
    if not os.path.exists(archive_path):
        return set()
    
    existing_ids = set()
    try:
        with open(archive_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for ID lines in the format "ID: [conversation_id]"
            id_matches = re.findall(r'^ID: (.+)$', content, re.MULTILINE)
            existing_ids = set(id_matches)
    except Exception as e:
        print(f"Warning: Could not parse existing archive: {e}")
    
    return existing_ids


def create_archive_entry(conversation, conversation_id):
    """Create a formatted archive entry for a conversation"""
    title = conversation.get('title', 'Untitled Conversation')
    create_time = conversation.get('create_time', 0)
    
    # Format timestamp
    if create_time:
        dt = datetime.fromtimestamp(create_time)
        timestamp = dt.isoformat()
    else:
        timestamp = 'Unknown'
    
    # Build entry
    lines = []
    lines.append("=" * 80)
    lines.append(f"CONVERSATION: {title}")
    lines.append(f"Date: {timestamp}")
    lines.append(f"ID: {conversation_id}")
    lines.append("=" * 80)
    lines.append("")
    
    # Add conversation content
    content = extract_conversation_text(conversation)
    lines.append(content)
    
    lines.append("=" * 80)
    lines.append("")
    
    return '\n'.join(lines)


def write_archive(conversations_data, archive_path, append=True):
    """Write conversations to archive file"""
    # Parse existing IDs if appending
    existing_ids = set()
    if append:
        existing_ids = parse_existing_archive(archive_path)
        print(f"Found {len(existing_ids)} existing conversations in archive")
    
    # Collect all conversations with metadata
    all_conversations = []
    
    for conv_id, conversation in conversations_data.items():
        create_time = conversation.get('create_time', 0)
        all_conversations.append({
            'id': conv_id,
            'data': conversation,
            'create_time': create_time
        })
    
    # Sort by creation time, newest first
    all_conversations.sort(key=lambda x: x['create_time'], reverse=True)
    
    # Filter to only new conversations if appending
    if append:
        new_conversations = [c for c in all_conversations if c['id'] not in existing_ids]
        print(f"Found {len(new_conversations)} new conversations to add")
        
        if not new_conversations:
            print("No new conversations to add to archive")
            return
        
        # Append new conversations to archive
        with open(archive_path, 'a', encoding='utf-8') as f:
            for conv in new_conversations:
                entry = create_archive_entry(conv['data'], conv['id'])
                f.write(entry)
                f.write('\n')
        
        print(f"Appended {len(new_conversations)} conversations to {archive_path}")
    else:
        # Write fresh archive
        with open(archive_path, 'w', encoding='utf-8') as f:
            for conv in all_conversations:
                entry = create_archive_entry(conv['data'], conv['id'])
                f.write(entry)
                f.write('\n')
        
        print(f"Wrote {len(all_conversations)} conversations to {archive_path}")


def write_individual_files(conversations_data, output_dir):
    """Write each conversation to individual text file"""
    os.makedirs(output_dir, exist_ok=True)

    count = 0
    for conversation_id, conversation in conversations_data.items():
        title = conversation.get('title', 'Untitled Conversation')
        safe_title = sanitize_filename(title)

        # Get timestamps
        create_time = conversation.get('create_time', 0)
        update_time = conversation.get('update_time', 0)

        # Format dates
        if create_time:
            create_date = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d')
        else:
            create_date = 'unknown'

        if update_time:
            update_date = datetime.fromtimestamp(update_time).strftime('%Y-%m-%d')
        else:
            update_date = 'unknown'

        # Create filename with date stamps: create_date__update_date_title_id.txt
        filename = f"{create_date}__{update_date}_{safe_title}_{conversation_id[:8]}.txt"
        filepath = os.path.join(output_dir, filename)

        # Extract and write content
        content = extract_conversation_text(conversation)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
        except Exception as e:
            print(f"Error writing {filename}: {e}")

    print(f"Extracted {count} conversations to {output_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description='Extract ChatGPT conversations from conversations.json export',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract to individual files (default)
  %(prog)s conversations.json
  
  # Create/append to archive file
  %(prog)s conversations.json --archive chatgpt_archive.txt
  
  # Do both
  %(prog)s conversations.json --individual --archive chatgpt_archive.txt
  
  # Force fresh archive (don't append)
  %(prog)s conversations.json --archive chatgpt_archive.txt --no-append
        """
    )
    
    parser.add_argument('input_file', help='Path to conversations.json file')
    parser.add_argument('--individual', '-i', action='store_true',
                        help='Output individual text files (default if no --archive)')
    parser.add_argument('--archive', '-a', nargs='?', const='chatgpt_archive.txt',
                        help='Output combined archive file (optionally specify filename)')
    parser.add_argument('--no-append', action='store_true',
                        help='Create fresh archive instead of appending')
    parser.add_argument('--output-dir', '-o', default='chatgpt_conversations',
                        help='Output directory for individual files (default: chatgpt_conversations)')
    
    args = parser.parse_args()
    
    # Default to individual files if neither mode specified
    if not args.individual and not args.archive:
        args.individual = True
    
    # Load conversations.json
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {args.input_file}")
        return 1
    except json.JSONDecodeError:
        print(f"Error: {args.input_file} is not valid JSON")
        return 1

    # Handle both list (array) and dict formats
    if isinstance(data, list):
        # Convert list to dict with generated conversation IDs
        # Use create_time + title hash for stable IDs across exports
        conversations = {}
        for conv in data:
            # Generate stable ID from create_time and title
            title = conv.get('title', 'untitled')
            create_time = conv.get('create_time', 0)
            id_string = f"{create_time}_{title}"
            conv_id = hashlib.sha256(id_string.encode()).hexdigest()[:16]
            conversations[conv_id] = conv
    else:
        conversations = data

    if not conversations:
        print("No conversations found in input file")
        return 1

    print(f"Loaded {len(conversations)} conversations from {args.input_file}")
    
    # Process based on mode
    if args.individual:
        write_individual_files(conversations, args.output_dir)
    
    if args.archive:
        write_archive(conversations, args.archive, append=not args.no_append)
    
    return 0


if __name__ == '__main__':
    exit(main())
