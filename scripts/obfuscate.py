#!/usr/bin/env python3
"""scripts/obfuscate.py
Deterministic obfuscation pass for boot.asm: fills 'decoy_table' with pseudo-random bytes
seeded by --seed to keep builds reproducible. Makes a backup of boot.asm as boot.asm.bak
and writes a new boot.asm with the modified decoy_table.

Usage: scripts/obfuscate.py --seed 1234 boot.asm
"""

import argparse
import random
import re
import sys

TEMPLATE = 'decoy_table: {}\n'

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--seed', type=int, default=0)
    p.add_argument('file', help='Path to boot.asm')
    return p.parse_args()

def make_bytes(seed, length=32):
    rnd = random.Random(seed)
    return bytes(rnd.getrandbits(8) for _ in range(length))

def format_db_bytes(b):
    return 'db ' + ','.join(f'0x{byte:02X}' for byte in b)

def main():
    args = parse_args()
    path = args.file
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except Exception as e:
        print(f'Error reading {path}: {e}', file=sys.stderr)
        sys.exit(2)

    # backup
    with open(path + '.bak', 'w', encoding='utf-8') as f:
        f.write(src)

    # find decoy_table declaration (either "decoy_table: times N db 0x90" or existing db list)
    m = re.search(r"decoy_table:\s*[:\w\s,0x]*\n", src)
    if not m:
        # fallback: try to locate 'decoy_table' in a different way
        m = re.search(r"decoy_table:[^\n]*\n", src)
    if not m:
        print('Could not find decoy_table label in boot.asm', file=sys.stderr)
        sys.exit(3)

    new_bytes = make_bytes(args.seed, 32)
    new_db = format_db_bytes(new_bytes)
    replacement = f"decoy_table: {new_db}   ; obfuscated with seed={args.seed}\n"

    new_src = src[:m.start()] + replacement + src[m.end():]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_src)

    print(f'obfuscation: wrote {path} (seed={args.seed}), backup at {path}.bak')

if __name__ == '__main__':
    main()
