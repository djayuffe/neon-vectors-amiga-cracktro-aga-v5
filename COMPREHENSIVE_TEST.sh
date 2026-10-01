#!/bin/sh
# Honest host-side release test. Optional toolchain/emulator checks are SKIP,
# never silently counted as PASS.
set -u
PASS=0; FAIL=0; SKIP=0
ok(){ printf 'PASS  %s\n' "$1"; PASS=$((PASS+1)); }
bad(){ printf 'FAIL  %s\n' "$1"; FAIL=$((FAIL+1)); }
skip(){ printf 'SKIP  %s\n' "$1"; SKIP=$((SKIP+1)); }
run(){ name=$1; shift; if "$@"; then ok "$name"; else bad "$name"; fi; }

printf '%s\n' 'NEON VECTORS — comprehensive host validation'
run 'static source/assets validation' python3 tools/validate.py
run 'deterministic asset reproduction' python3 tools/verify_repro.py
run 'release manifest integrity' python3 tools/verify_manifest.py

ASM=$(command -v vasmm68k_mot 2>/dev/null || true)
[ -n "$ASM" ] || { [ -x tools/bin/vasmm68k_mot ] && ASM=tools/bin/vasmm68k_mot || true; }
if [ -n "$ASM" ]; then
  if make clean all VASM="$ASM"; then ok 'assemble + Amiga Hunk validation'; else bad 'assemble + Amiga Hunk validation'; fi
else
  skip 'assemble + Hunk validation (vasmm68k_mot unavailable)'
fi

if python3 -c 'import machine68k' >/dev/null 2>&1; then
  if make emutest; then ok '68000 execution harness'; else bad '68000 execution harness'; fi
else
  skip '68000 execution harness (machine68k unavailable)'
fi

printf '\nSummary: %d passed, %d failed, %d skipped\n' "$PASS" "$FAIL" "$SKIP"
[ "$FAIL" -eq 0 ]
