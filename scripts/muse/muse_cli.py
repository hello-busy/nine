#!/usr/bin/env python3
"""CLI for the offline Muse assistant (chat-like REPL).
- No network calls; all data stored locally in SQLite.
- Simple deterministic 'generation' using local memories and templates.
Usage:
  python3 scripts/muse/muse_cli.py       # interactive REPL
  python3 scripts/muse/muse_cli.py --file session.txt   # run a script of lines to feed

Commands available in the REPL (start a line with a slash):
  /help                Show this help
  /exit                Exit the REPL
  /remember KEY VALUE  Save a memory (short key/value)
  /recall KEY          Recall a memory by key
  /search QUERY        Search memories by text (substring match)
  /mems                List all memory keys
  /history [N]         Show last N chat messages (default 50)
  /export FILE         Export DB to file (SQLite copy)
  /import FILE         Import DB from file (replaces current DB)
  /clear               Clear conversation history (keeps memories)
  /reset               Reset DB (clears memories and history)

The REPL treats lines not starting with '/' as user messages to the muse, and prints a generated response.
"""

import argparse
import sys
import os
from pathlib import Path
from scripts.muse.muse_backend import MuseBackend
from scripts.muse.muse_utils import generate_response

DEFAULT_DB = Path.home() / '.muse_db.sqlite3'

def repl(db_path, script_file=None):
    backend = MuseBackend(db_path)
    if script_file:
        # feed lines from the file as if typed
        with open(script_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                print(f"> {line}")
                handle_input(line, backend)
        return

    print("Muse CLI — an offline assistant. Type /help for commands.")
    try:
        while True:
            line = input('> ').strip()
            if not line:
                continue
            if line.startswith('/'):  
                if line == '/help':
                    print_help()
                elif line == '/exit':
                    print('Goodbye.')
                    break
                else:
                    handle_command(line, backend)
            else:
                handle_message(line, backend)
    except (KeyboardInterrupt, EOFError):
        print('\nExiting Muse. Bye.')


def print_help():
    print('\nCommands:\n  /help  /exit  /remember KEY VALUE  /recall KEY  /search QUERY')
    print('  /mems  /history [N]  /export FILE  /import FILE  /clear  /reset')


def handle_command(line, backend):
    parts = line.split(maxsplit=2)
    cmd = parts[0]
    if cmd == '/remember':
        if len(parts) < 3:
            print('Usage: /remember KEY VALUE')
            return
        key, value = parts[1], parts[2]
        backend.add_memory(key, value)
        print(f"Remembered: {key}")
    elif cmd == '/recall':
        if len(parts) < 2:
            print('Usage: /recall KEY')
            return
        v = backend.get_memory(parts[1])
        if v is None:
            print('No memory found for that key')
        else:
            print(f"{parts[1]} => {v}")
    elif cmd == '/search':
        if len(parts) < 2:
            print('Usage: /search QUERY')
            return
        results = backend.search_memories(' '.join(parts[1:]))
        for k, v in results:
            print(f"- {k}: {v}")
    elif cmd == '/mems':
        for k in backend.list_memory_keys():
            print(f"- {k}")
    elif cmd == '/history':
        n = 50
        if len(parts) >= 2:
            try:
                n = int(parts[1])
            except Exception:
                pass
        for who, text, ts in backend.get_history(n):
            print(f"[{who}] {text}")
    elif cmd == '/export':
        if len(parts) < 2:
            print('Usage: /export FILE')
            return
        backend.export_db(parts[1])
        print('Exported DB.')
    elif cmd == '/import':
        if len(parts) < 2:
            print('Usage: /import FILE')
            return
        backend.import_db(parts[1])
        print('Imported DB.')
    elif cmd == '/clear':
        backend.clear_history()
        print('Cleared conversation history.')
    elif cmd == '/reset':
        confirm = input('Are you sure? This will erase all memories too. (yes/NO) ')
        if confirm.lower() == 'yes':
            backend.reset()
            print('Database reset.')
        else:
            print('Aborted.')
    else:
        print('Unknown command. Type /help')


def handle_message(text, backend):
    backend.save_message('user', text)
    # gather relevant memories to inform the response
    mems = backend.search_memories(text)
    resp = generate_response(text, mems)
    backend.save_message('muse', resp)
    print(resp)


def handle_input(line, backend):
    if line.startswith('/'):
        handle_command(line, backend)
    else:
        handle_message(line, backend)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--db', default=str(DEFAULT_DB), help='Path to SQLite DB file')
    p.add_argument('--file', help='Script file to feed into the REPL (non-interactive)')
    args = p.parse_args()
    os.makedirs(Path(args.db).parent, exist_ok=True)
    repl(args.db, args.file)

if __name__ == '__main__':
    main()