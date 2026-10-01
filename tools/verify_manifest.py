#!/usr/bin/env python3
"""Verify MANIFEST.sha256 and reject untracked shipped files."""
from pathlib import Path
import hashlib, sys
R=Path(__file__).resolve().parents[1]
manifest=R/'MANIFEST.sha256'
SKIP_DIRS={'.git','build','__pycache__','vendor','tools/vendor','tools/bin','.venv','venv'}
SKIP_SUFFIXES={'.pyc','.pyo','.o','.obj','.tmp','.bak','.orig','.rej','.DS_Store'}
SKIP_NAMES={'MANIFEST.sha256','.DS_Store','a.out'}
def shipped(p):
    if not p.is_file(): return False
    if set(p.relative_to(R).parts) & SKIP_DIRS: return False
    if p.suffix in SKIP_SUFFIXES or p.name in SKIP_NAMES or p.name.startswith('.'): return False
    return True
errors=[]; expected={}
for n,line in enumerate(manifest.read_text().splitlines(),1):
    if not line.strip(): continue
    try: digest, rel=line.split('  ',1)
    except ValueError: errors.append(f'line {n}: malformed'); continue
    if rel in expected: errors.append(f'line {n}: duplicate {rel}')
    expected[rel]=digest
actual={p.relative_to(R).as_posix():p for p in R.rglob('*') if shipped(p)}
for rel,digest in expected.items():
    p=actual.get(rel)
    if p is None: errors.append(f'missing: {rel}'); continue
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=digest: errors.append(f'hash mismatch: {rel}')
for rel in sorted(set(actual)-set(expected)): errors.append(f'untracked shipped file: {rel}')
if errors:
    print('MANIFEST VERIFY FAILED')
    for e in errors: print(' -',e)
    sys.exit(1)
print(f'MANIFEST OK ({len(expected)} files)')
