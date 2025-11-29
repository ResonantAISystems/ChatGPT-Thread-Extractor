#!/usr/bin/env python3
"""
ChatGPT Thread Extractor - GUI Version
Simple graphical interface for extracting ChatGPT conversations
"""

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from tkinter import ttk
import os
import sys
import threading
from pathlib import Path

# Import the extractor functions
import json
import re
import hashlib
from datetime import datetime


def sanitize_filename(title, max_length=100):
    """Convert conversation title to safe filename"""
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_title = re.sub(r'\s+', '_', safe_title)
    if len(safe_title) > max_length:
        safe_title = safe_title[:max_length]
    safe_title = safe_title.rstrip('. ')
    return safe_title if safe_title else 'untitled'


def extract_conversation_text(conversation):
    """Extract text content from conversation structure"""
    lines = []

    title = conversation.get('title', 'Untitled Conversation')
    lines.append(f"Title: {title}\n")
    lines.append("=" * 80 + "\n\n")

    mapping = conversation.get('mapping', {})

    messages = []
    for node_id, node in mapping.items():
        message = node.get('message')
        if message and message.get('content'):
            content = message.get('content', {})
            parts = content.get('parts', [])
            author_role = message.get('author', {}).get('role', 'unknown')

            if parts and any(parts):
                text = '\n'.join(str(part) for part in parts if part)
                if text.strip():
                    messages.append({
                        'role': author_role,
                        'text': text,
                        'create_time': message.get('create_time')
                    })

    messages.sort(key=lambda x: x.get('create_time', 0))

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
    """Parse existing archive file to extract conversation IDs"""
    if not os.path.exists(archive_path):
        return set()

    existing_ids = set()
    try:
        with open(archive_path, 'r', encoding='utf-8') as f:
            content = f.read()
            id_matches = re.findall(r'^ID: (.+)$', content, re.MULTILINE)
            existing_ids = set(id_matches)
    except Exception:
        pass

    return existing_ids


def create_archive_entry(conversation, conversation_id):
    """Create a formatted archive entry for a conversation"""
    title = conversation.get('title', 'Untitled Conversation')
    create_time = conversation.get('create_time', 0)

    if create_time:
        dt = datetime.fromtimestamp(create_time)
        timestamp = dt.isoformat()
    else:
        timestamp = 'Unknown'

    lines = []
    lines.append("=" * 80)
    lines.append(f"CONVERSATION: {title}")
    lines.append(f"Date: {timestamp}")
    lines.append(f"ID: {conversation_id}")
    lines.append("=" * 80)
    lines.append("")

    content = extract_conversation_text(conversation)
    lines.append(content)

    lines.append("=" * 80)
    lines.append("")

    return '\n'.join(lines)


def write_archive(conversations_data, archive_path, append=True, log_callback=None):
    """Write conversations to archive file"""
    existing_ids = set()
    if append:
        existing_ids = parse_existing_archive(archive_path)
        if log_callback:
            log_callback(f"Found {len(existing_ids)} existing conversations in archive\n")

    all_conversations = []

    for conv_id, conversation in conversations_data.items():
        create_time = conversation.get('create_time', 0)
        all_conversations.append({
            'id': conv_id,
            'data': conversation,
            'create_time': create_time
        })

    all_conversations.sort(key=lambda x: x['create_time'], reverse=True)

    if append:
        new_conversations = [c for c in all_conversations if c['id'] not in existing_ids]
        if log_callback:
            log_callback(f"Found {len(new_conversations)} new conversations to add\n")

        if not new_conversations:
            if log_callback:
                log_callback("No new conversations to add to archive\n")
            return 0

        with open(archive_path, 'a', encoding='utf-8') as f:
            for conv in new_conversations:
                entry = create_archive_entry(conv['data'], conv['id'])
                f.write(entry)
                f.write('\n')

        if log_callback:
            log_callback(f"Appended {len(new_conversations)} conversations to {archive_path}\n")
        return len(new_conversations)
    else:
        with open(archive_path, 'w', encoding='utf-8') as f:
            for conv in all_conversations:
                entry = create_archive_entry(conv['data'], conv['id'])
                f.write(entry)
                f.write('\n')

        if log_callback:
            log_callback(f"Wrote {len(all_conversations)} conversations to {archive_path}\n")
        return len(all_conversations)


def write_individual_files(conversations_data, output_dir, log_callback=None):
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

        content = extract_conversation_text(conversation)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
        except Exception as e:
            if log_callback:
                log_callback(f"Error writing {filename}: {e}\n")

    if log_callback:
        log_callback(f"Extracted {count} conversations to {output_dir}/\n")
    return count


class ExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatGPT Thread Extractor")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # Variables
        self.input_file = tk.StringVar()
        self.output_mode = tk.StringVar(value="individual")
        self.output_dir = tk.StringVar(value="chatgpt_conversations")
        self.archive_file = tk.StringVar(value="chatgpt_archive.txt")
        self.no_append = tk.BooleanVar(value=False)

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="ChatGPT Thread Extractor",
                                font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        # Input file section
        row = 1
        ttk.Label(main_frame, text="Input File:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.input_file, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        ttk.Button(main_frame, text="Browse...", command=self.browse_input).grid(
            row=row, column=2, pady=5)

        # Output mode section
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        row += 1
        ttk.Label(main_frame, text="Output Mode:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=5)

        row += 1
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=5)

        ttk.Radiobutton(mode_frame, text="Individual Files",
                       variable=self.output_mode, value="individual",
                       command=self.update_ui_state).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Archive File",
                       variable=self.output_mode, value="archive",
                       command=self.update_ui_state).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(mode_frame, text="Both",
                       variable=self.output_mode, value="both",
                       command=self.update_ui_state).pack(side=tk.LEFT, padx=5)

        # Individual files options
        row += 1
        self.dir_label = ttk.Label(main_frame, text="Output Directory:")
        self.dir_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.dir_entry = ttk.Entry(main_frame, textvariable=self.output_dir, width=50)
        self.dir_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.dir_button = ttk.Button(main_frame, text="Browse...", command=self.browse_output_dir)
        self.dir_button.grid(row=row, column=2, pady=5)

        # Archive file options
        row += 1
        self.archive_label = ttk.Label(main_frame, text="Archive File:")
        self.archive_label.grid(row=row, column=0, sticky=tk.W, pady=5)
        self.archive_entry = ttk.Entry(main_frame, textvariable=self.archive_file, width=50)
        self.archive_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        self.archive_button = ttk.Button(main_frame, text="Browse...", command=self.browse_archive)
        self.archive_button.grid(row=row, column=2, pady=5)

        row += 1
        self.append_check = ttk.Checkbutton(main_frame, text="Create fresh archive (don't append to existing)",
                                           variable=self.no_append)
        self.append_check.grid(row=row, column=1, sticky=tk.W, pady=5)

        # Extract button
        row += 1
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)

        row += 1
        self.extract_button = ttk.Button(main_frame, text="Extract Conversations",
                                        command=self.start_extraction)
        self.extract_button.grid(row=row, column=0, columnspan=3, pady=10)

        # Progress/log section
        row += 1
        ttk.Label(main_frame, text="Output Log:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(10, 5))

        row += 1
        self.log_text = scrolledtext.ScrolledText(main_frame, height=12, width=70,
                                                  state='disabled', wrap=tk.WORD)
        self.log_text.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(row, weight=1)

        # Initial UI state
        self.update_ui_state()

    def update_ui_state(self):
        """Enable/disable fields based on selected mode"""
        mode = self.output_mode.get()

        # Individual files fields
        if mode in ["individual", "both"]:
            self.dir_label.config(state='normal')
            self.dir_entry.config(state='normal')
            self.dir_button.config(state='normal')
        else:
            self.dir_label.config(state='disabled')
            self.dir_entry.config(state='disabled')
            self.dir_button.config(state='disabled')

        # Archive fields
        if mode in ["archive", "both"]:
            self.archive_label.config(state='normal')
            self.archive_entry.config(state='normal')
            self.archive_button.config(state='normal')
            self.append_check.config(state='normal')
        else:
            self.archive_label.config(state='disabled')
            self.archive_entry.config(state='disabled')
            self.archive_button.config(state='disabled')
            self.append_check.config(state='disabled')

    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select conversations.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)

    def browse_output_dir(self):
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.output_dir.set(dirname)

    def browse_archive(self):
        filename = filedialog.asksaveasfilename(
            title="Archive File",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.archive_file.set(filename)

    def log(self, message):
        """Add message to log window"""
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update_idletasks()

    def clear_log(self):
        """Clear the log window"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')

    def start_extraction(self):
        """Start extraction in a separate thread"""
        # Validate input
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input file")
            return

        if not os.path.exists(self.input_file.get()):
            messagebox.showerror("Error", f"File not found: {self.input_file.get()}")
            return

        # Disable extract button during processing
        self.extract_button.config(state='disabled')
        self.clear_log()

        # Run extraction in thread to keep UI responsive
        thread = threading.Thread(target=self.extract, daemon=True)
        thread.start()

    def extract(self):
        """Perform the extraction"""
        try:
            self.log(f"Loading {self.input_file.get()}...\n")

            # Load JSON
            with open(self.input_file.get(), 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both list and dict formats
            if isinstance(data, list):
                conversations = {}
                for conv in data:
                    title = conv.get('title', 'untitled')
                    create_time = conv.get('create_time', 0)
                    id_string = f"{create_time}_{title}"
                    conv_id = hashlib.sha256(id_string.encode()).hexdigest()[:16]
                    conversations[conv_id] = conv
            else:
                conversations = data

            if not conversations:
                self.log("ERROR: No conversations found in file\n")
                messagebox.showerror("Error", "No conversations found in input file")
                return

            self.log(f"Loaded {len(conversations)} conversations\n\n")

            mode = self.output_mode.get()

            # Extract based on mode
            if mode in ["individual", "both"]:
                self.log("--- Individual Files Mode ---\n")
                count = write_individual_files(conversations, self.output_dir.get(), self.log)
                self.log("\n")

            if mode in ["archive", "both"]:
                self.log("--- Archive Mode ---\n")
                count = write_archive(conversations, self.archive_file.get(),
                                    not self.no_append.get(), self.log)
                self.log("\n")

            self.log("=" * 60 + "\n")
            self.log("EXTRACTION COMPLETE!\n")
            self.log("=" * 60 + "\n")

            messagebox.showinfo("Success", "Extraction completed successfully!")

        except json.JSONDecodeError:
            self.log(f"\nERROR: Invalid JSON file\n")
            messagebox.showerror("Error", "The selected file is not valid JSON")
        except Exception as e:
            self.log(f"\nERROR: {str(e)}\n")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            # Re-enable extract button
            self.root.after(0, lambda: self.extract_button.config(state='normal'))


def main():
    root = tk.Tk()
    app = ExtractorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
