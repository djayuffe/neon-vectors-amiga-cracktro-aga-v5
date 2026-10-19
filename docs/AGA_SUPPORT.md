# AGA and 68020 runtime contract

## AGA palette implementation

The baseline binary remains 68000 compatible. Lisa is detected using the low byte of DENISEID (`$F8`); the reserved high byte is masked. OCS/ECS follows the original rendering path and does not enter AGA register setup.

The display uses four bitplanes at 320×256, with `FMODE=0` and palette bank zero. `BPLCON4=$0011` selects palette base 16 for both even and odd sprite groups. Zero would incorrectly map the sprites into the playfield palette.

Lisa high-colour writes also copy each nibble into the corresponding low-colour register. Therefore programming low nibbles before the Copper header has no lasting effect. After the header and before the visible logo, the CPU writes all 32 low entries using LOCT, then clears LOCT. The bank follows a gentle 32-step, 128-frame neon breathing curve; it is programmed each frame because the Copper resets low values each frame.

The overrides affect logo accent entries until their next Copper write, and all sprite shades throughout the visible frame. Per-row logo face colours and the later middle/floor palette changes retain replicated 12-bit colour values. This is selective RGB24 precision, not an all-band RGB24 gradient renderer. The render model applies high-write replication instead of incorrectly assuming persistent low nibbles.

No extra displayed planes, chip allocation, or Copper instructions are added. The palette animation adds 2 KiB of ordinary data compared with the original 16-word bank. Eight planes, HAM8, wider DMA fetches, and wider sprites remain unimplemented and require different buffers, fetch alignment, Copper schedules, and hardware validation.

## Dedicated 68020 executable

```sh
make aga020
# build/neon_vectors_020
make emutest-020
```

This separate build uses scaled word-index addressing for projected edge endpoints and inlines the exact fixed-point multiply/shift sequence in matrix construction. It preserves fixed-point rounding and the reference image. The initial instructions are 68000 safe and inspect ExecBase.AttnFlags bit 1 before any 68020-only code. Older CPUs return 20 without opening a library or taking over the display. No FPU, MMU, cache manipulation, or self-modifying code is required.

```sh
python3 tools/emu_test.py --reject-020 --frames 10 --snap 5
python3 tools/test_aga_profiles.py
```

The second command proves that corrupting sprite palette mapping, truncating the low palette, breaking scaled indices, and corrupting the CPU capability bit produce specific behavioral failures.

## Evidence and acceptance limits

The emulator executes both CPU variants and checks palette phase every frame, LOCT restoration, blanking-window write timing, reserved DENISEID bits, sprite mapping, rendered geometry, audio DMA events, system restoration, and 68000 rejection. Model cycle figures exclude DMA contention, real blitter duration, CPU clock differences, and caches; they are not hardware performance measurements. A real A1200 or cycle-accurate full-system run remains required for release acceptance.

Primary references: [Commodore Lisa specification](https://www.amigawiki.org/lib/exe/fetch.php?media=de:parts:aa_lisa_specification.pdf), sections BPLCON3/BPLCON4 and COLORxx; [Motorola programmer reference](https://www.nxp.com/docs/en/reference-manual/M68000PRM.pdf), MC68020 addressing modes.
