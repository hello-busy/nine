#!/usr/bin/env python3
# Simple line-based DSL parser for Muse.
from typing import List, Tuple, Any
import re

class ParseError(Exception):
    pass

def tokenize_line(line: str):
    line = line.strip()
    if not line or line.startswith('#'):
        return None
    # Simple patterns
    m = re.match(r'^SAY\s+"(.*)"$', line)
    if m: return ('SAY', m.group(1))
    m = re.match(r'^ECHO\s+"(.*)"$', line)
    if m: return ('ECHO', m.group(1))
    m = re.match(r'^REMEMBER\s+([A-Za-z0-9_\-]+)\s*=\s*"(.*)"$', line)
    if m: return ('REMEMBER', (m.group(1), m.group(2)))
    m = re.match(r'^RECALL\s+([A-Za-z0-9_\-]+)$', line)
    if m: return ('RECALL', m.group(1))
    m = re.match(r'^SEARCH\s+"(.*)"$', line)
    if m: return ('SEARCH', m.group(1))
    m = re.match(r'^RUN_SKILL\s+([A-Za-z0-9_]+)\s+"(.*)"$', line)
    if m: return ('RUN_SKILL', (m.group(1), m.group(2)))
    m = re.match(r'^WAIT\s+(\d+)$', line)
    if m: return ('WAIT', int(m.group(1)))
    m = re.match(r'^IF\s+EXISTS\s+([A-Za-z0-9_\-]+)$', line)
    if m: return ('IF_EXISTS', m.group(1))
    m = re.match(r'^IF\s+EQ\s+([A-Za-z0-9_\-]+)\s+"(.*)"$', line)
    if m: return ('IF_EQ', (m.group(1), m.group(2)))
    if line == 'ELSE': return ('ELSE', None)
    if line == 'ENDIF': return ('ENDIF', None)
    m = re.match(r'^LOOP\s+(\d+)$', line)
    if m: return ('LOOP', int(m.group(1)))
    if line == 'ENDLOOP': return ('ENDLOOP', None)
    m = re.match(r'^IMPORT\s+"(.*)"$', line)
    if m: return ('IMPORT', m.group(1))
    raise ParseError(f"Unknown or malformed line: {line}")

def parse_lines(lines: List[str]) -> List[Tuple[str, Any]]:
    program = []
    for ln, line in enumerate(lines, start=1):
        try:
            tok = tokenize_line(line)
            if tok:
                program.append(tok)
        except ParseError as e:
            raise ParseError(f"Line {ln}: {e}")
    return program

if __name__ == '__main__':
    import sys
    p = sys.argv[1] if len(sys.argv)>1 else None
    if not p:
        print('Usage: lang.py script.muse')
        sys.exit(2)
    with open(p,'r',encoding='utf-8') as f:
        prog = parse_lines(f.readlines())
    for ins in prog:
        print(ins)
