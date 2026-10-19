# AGA / MC68020 audit — 2026-10-19

This pass corrects the shipping palette path and adds a separate optimized CPU build. It does not certify hardware perfection or claim additional bitplanes, HAM8, wide DMA, or solid rendering.

## Changes

- Mask the reserved DENISEID high byte; accept Lisa by its low `$F8` identification byte.
- Correct AGA sprite palette addressing to `BPLCON4=$0011`.
- Apply 32 low RGB entries after the Copper header and before the visible logo. Lisa high writes also overwrite low nibbles; the previous implementation's pre-header writes could not produce its documented persistent precision.
- Animate the low-bank values over a smooth 128-frame breathing cycle, with independent warm/cool sprite shades. Later Copper high writes intentionally restore replicated low bits for their entries. The middle/floor bands remain 12-bit gradients.
- Add `make aga020`, with scaled vertex indexing and inline fixed-point multiply/shift operations. An initial Exec AttnFlags check rejects older CPUs before libraries, allocation, or takeover.
- Correct generated music to signed PCM and change terminal silence from `$8080` to `$0000`. The validator and audio-DMA checks now enforce zero-centered data and silence.
- Extend the real-code execution harness with 68020 selection, Lisa detection tests including reserved high bits, per-frame low-bank references, LOCT restoration, palette timing, sprite-base assertions, and RGB24 preview rendering with correct Copper high-write replication.
- Unexpected nonzero startup returns now fail the harness directly rather than crashing during empty timing statistics.
- Add four behavioral fault injections and extend static mutation coverage to 41 faults.

## Validation

Both executables assemble with VASM 2.0f and pass Hunk checks. Baseline and AGA/68000 runs each execute 800 frames; the optimized AGA/68020 run also executes 800. Each checks 798 wireframe images against the independent reference, and 121 audio starts over 134 tracker rows. A separate 68000 execution of the 020 executable returns 20 without takeover.

The corrected AGA/68000 path averages 84,009 modeled cycles, worst 91,608. The AGA/68020 model averages 44,226, worst 48,521. These are core-model cycles, not directly comparable elapsed hardware times: CPU clocks, cache effects, DMA contention, and blitter duration are not modeled. The conservative 68000 AGA starfield deadline retains 7,314 modeled cycles of margin.

The static validator catches 41/41 injected faults. Behavioral faults independently corrupt sprite palette addressing, the number of low colours written, scaled vertex indexing, and the CPU capability bit. Asset regeneration is byte-for-byte deterministic; Python compilation, fatal-error lint, and source whitespace checks pass.

Chip data stays at 86,962 bytes (86,964 aligned); the Copper stays at 924 words. The low-bank table expands ordinary data by 2,016 bytes, with no additional bitplane DMA or chip allocation. Executables are approximately 97 KiB.

## Release limits

Real AGA hardware or a cycle-accurate A1200 emulator with a legally supplied ROM is still required to judge DMA contention, cache-sensitive timing, sound quality, and restoration against an actual OS. Existing experimental Python/assembly renderers remain outside the shipping translation unit.

Hardware semantics were checked against the [Commodore Lisa specification](https://www.amigawiki.org/lib/exe/fetch.php?media=de:parts:aa_lisa_specification.pdf), especially COLORxx and BPLCON4, and the [Motorola programmer reference](https://www.nxp.com/docs/en/reference-manual/M68000PRM.pdf) for scaled addressing. The Lisa document explicitly describes high writes updating both nibble banks; selective overrides must follow those writes.
