# NEON VECTORS v5 — AGA compatibility/enhancement pass

- One executable supports OCS, ECS and AGA.
- Runtime Lisa detection through DENISEID=$00F8.
- OCS/ECS path never executes AGA-only register writes.
- AGA uses FMODE=0 to preserve the proven 16-bit fetch/DMA timing.
- AGA low RGB nibbles are programmed through BPLCON3.LOCT, giving 8:8:8 precision while the existing Copper continues to animate high RGB nibbles.
- BPLCON3 is restored to high-nibble mode before Copper colour writes.
- BPLCON4 remains zero for compatible sprite/bitplane palette mapping.
- Added docs/AGA_SUPPORT.md.
- Added five AGA-specific mutation tests; full mutation result is 38/38 caught.
- Static validation and deterministic asset reproduction pass.
- Fresh assembled-Hunk and machine68k execution remain dependent on external tools unavailable in this environment.
