#!/usr/bin/env python3
# Executor for the Muse DSL. Runs scripts against a MuseBackend and skill_router.
import time
import argparse
from pathlib import Path
from scripts.muse.muse_backend import MuseBackend
from scripts.muse.skill_router import get_response
from scripts.muse.dsl.lang import parse_lines

class Executor:
    def __init__(self, backend: MuseBackend):
        self.backend = backend
        self.ip = 0

    def run_program(self, program):
        self._run_block(program, 0, len(program))

    def _run_block(self, program, start, end):
        i = start
        stack = []
        while i < end:
            op, arg = program[i]
            if op == 'SAY':
                mems = self.backend.search_memories(arg)
                resp = get_response(arg, mems, {})
                print('MUSE:', resp)
                self.backend.save_message('muse', resp)
            elif op == 'ECHO':
                print(arg)
            elif op == 'REMEMBER':
                k,v = arg
                self.backend.add_memory(k, v)
                print(f'[remembered] {k} = {v}')
            elif op == 'RECALL':
                v = self.backend.get_memory(arg)
                print(f'[recall] {arg} => {v}')
            elif op == 'SEARCH':
                res = self.backend.search_memories(arg)
                for k,v in res:
                    print(f'- {k}: {v}')
            elif op == 'RUN_SKILL':
                skill, inp = arg
                mems = self.backend.search_memories(inp)
                # map skill name to specific module via router by calling get_response
                resp = get_response(inp, mems, {'force_skill':skill})
                print(f'[skill:{skill}]', resp)
                self.backend.save_message('muse', resp)
            elif op == 'WAIT':
                time.sleep(arg)
            elif op == 'IMPORT':
                path = Path(arg)
                if not path.exists():
                    print(f'IMPORT failed: {path} not found')
                else:
                    lines = path.read_text(encoding='utf-8').splitlines()
                    subprog = parse_lines(lines)
                    self._run_block(subprog, 0, len(subprog))
            elif op == 'IF_EXISTS':
                key = arg
                val = self.backend.get_memory(key)
                # find matching ELSE/ENDIF
                j = i+1
                depth = 0
                true_block = []
                false_block = []
                collecting = 'true'
                while j < end:
                    o,a = program[j]
                    if o in ('IF_EXISTS','IF_EQ'):
                        depth +=1
                        if collecting == 'true': true_block.append((o,a))
                        else: false_block.append((o,a))
                    elif o == 'ELSE' and depth==0:
                        collecting = 'false'
                    elif o == 'ENDIF' and depth==0:
                        break
                    elif o == 'ENDIF':
                        depth -=1
                        if collecting == 'true': true_block.append((o,a))
                        else: false_block.append((o,a))
                    else:
                        if collecting == 'true': true_block.append((o,a))
                        else: false_block.append((o,a))
                    j+=1
                if val is not None:
                    self._run_block(true_block,0,len(true_block))
                else:
                    self._run_block(false_block,0,len(false_block))
                i = j
            elif op == 'IF_EQ':
                key, check = arg
                val = self.backend.get_memory(key)
                # reuse same block finding logic
                j = i+1
                depth = 0
                true_block = []
                false_block = []
                collecting = 'true'
                while j < end:
                    o,a = program[j]
                    if o in ('IF_EXISTS','IF_EQ'):
                        depth +=1
                        if collecting == 'true': true_block.append((o,a))
                        else: false_block.append((o,a))
                    elif o == 'ELSE' and depth==0:
                        collecting = 'false'
                    elif o == 'ENDIF' and depth==0:
                        break
                    elif o == 'ENDIF':
                        depth -=1
                        if collecting == 'true': true_block.append((o,a))
                        else: false_block.append((o,a))
                    else:
                        if collecting == 'true': true_block.append((o,a))
                        else: false_block.append((o,a))
                    j+=1
                if val == check:
                    self._run_block(true_block,0,len(true_block))
                else:
                    self._run_block(false_block,0,len(false_block))
                i = j
            elif op == 'LOOP':
                count = arg
                # find matching ENDLOOP
                j = i+1
                depth = 0
                loop_block = []
                while j < end:
                    o,a = program[j]
                    if o == 'LOOP':
                        depth +=1
                        loop_block.append((o,a))
                    elif o == 'ENDLOOP' and depth==0:
                        break
                    elif o == 'ENDLOOP':
                        depth -=1
                        loop_block.append((o,a))
                    else:
                        loop_block.append((o,a))
                    j+=1
                for _ in range(count):
                    self._run_block(loop_block,0,len(loop_block))
                i = j
            else:
                print(f'Unknown op: {op}')
            i+=1

def main():
    p = argparse.ArgumentParser()
    p.add_argument('script', help='DSL script file to execute')
    p.add_argument('--db', default=str(Path.home()/'/.muse_db.sqlite3'))
    args = p.parse_args()
    backend = MuseBackend(args.db)
    text = Path(args.script).read_text(encoding='utf-8')
    prog = parse_lines(text.splitlines())
    exe = Executor(backend)
    exe.run_program(prog)

if __name__ == '__main__':
    main()
