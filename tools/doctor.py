#!/usr/bin/env python3
"""Fast, non-mutating host/toolchain readiness report for Neon Vectors."""
from pathlib import Path
import importlib.util, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def add(name, state, detail): checks.append((name,state,detail))
add('Python', 'PASS' if sys.version_info >= (3,8) else 'FAIL', sys.version.split()[0])
for rel in ('src/main.s','src/hardware.i','src/modplayer.s','assets/logo.raw','assets/font.raw','assets/neon.mod'):
    p=ROOT/rel; add(rel,'PASS' if p.is_file() else 'FAIL',str(p.stat().st_size)+' bytes' if p.is_file() else 'missing')
vasm=shutil.which('vasmm68k_mot')
local=ROOT/'tools/bin/vasmm68k_mot'
if not vasm and local.is_file() and local.stat().st_mode & 0o111: vasm=str(local)
add('VASM','PASS' if vasm else 'SKIP',vasm or 'not installed; assembly unavailable')
add('machine68k','PASS' if importlib.util.find_spec('machine68k') else 'SKIP','installed' if importlib.util.find_spec('machine68k') else 'not installed; execution harness unavailable')
try:
    r=subprocess.run([sys.executable,str(ROOT/'tools/validate.py')],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    add('static validator','PASS' if r.returncode==0 else 'FAIL','exit '+str(r.returncode))
except OSError as e: add('static validator','FAIL',str(e))
width=max(len(x[0]) for x in checks)
for n,s,d in checks: print(f'{s:4}  {n:<{width}}  {d}')
fails=sum(s=='FAIL' for _,s,_ in checks); skips=sum(s=='SKIP' for _,s,_ in checks)
print(f'\n{len(checks)-fails-skips} pass, {fails} fail, {skips} optional unavailable')
sys.exit(bool(fails))
