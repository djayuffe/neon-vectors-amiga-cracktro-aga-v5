#!/usr/bin/env python3
"""Behavioral fault checks for the AGA/68020 paths (requires VASM and machine68k)."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASES = [
    ('sprite palette base', 'move.w  #$0011,BPLCON4(a6)', 'clr.w   BPLCON4(a6)', 'sprite'),
    ('low sprite palette omitted', 'moveq   #31,d7', 'moveq   #15,d7', 'palette'),
    ('scaled vertex index', '0(a3,d4.w*4),d0', '0(a3,d4.w*2),d0', 'wireframe'),
    ('020 capability bit', 'btst    #1,297(a6)', 'btst    #0,297(a6)', 'return code'),
]


def main():
    assembler = os.environ.get('VASM') or shutil.which('vasmm68k_mot') or str(ROOT/'tools/bin/vasmm68k_mot')
    if not Path(assembler).is_file():
        raise SystemExit('Set VASM to the assembler path')
    with tempfile.TemporaryDirectory(prefix='neon_aga_faults_') as td:
        target = Path(td)
        for name in ('src', 'tools', 'assets'):
            shutil.copytree(ROOT/name, target/name, ignore=shutil.ignore_patterns('__pycache__','bin','vendor'))
        source = target/'src/main.s'
        original = source.read_text()
        cmd = [sys.executable, str(target/'tools/emu_test.py'), '--aga', '--cpu', '68020', '--frames', '100', '--snap', '80']
        env = dict(os.environ, VASM=str(Path(assembler).resolve()))
        def run():
            return subprocess.run(cmd, cwd=target, env=env, capture_output=True, text=True, timeout=120)
        baseline = run()
        if baseline.returncode:
            raise SystemExit('Baseline failed:\n'+baseline.stdout+baseline.stderr)
        print('AGA/68020 baseline passed')
        for name, old, new, diagnostic in CASES:
            if old not in original:
                raise SystemExit('Missing mutation anchor: '+name)
            source.write_text(original.replace(old,new,1))
            result=run()
            output=result.stdout+result.stderr
            if not result.returncode or 'Traceback' in output or not any('FAIL:' in line and diagnostic in line for line in output.splitlines()):
                raise SystemExit('Fault was not specifically caught: '+name+'\n'+output)
            print('Caught:',name)
    print('4/4 AGA/68020 behavioral faults caught')


if __name__=='__main__':
    main()
