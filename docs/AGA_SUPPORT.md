# NEON VECTORS AGA v5

NEON VECTORS v5 is the AGA edition. It uses one binary with a guarded OCS/ECS compatibility path,
but AGA/Lisa hardware is the intended public target for this release.

## Runtime contract

- Read `DENISEID` and accept `$00F8` as Lisa/AGA.
- Never execute AGA-only register writes when `aga_enabled == 0`.
- Keep `FMODE=0`: 16-bit fetches and the original 320x256x4 DMA budget.
- Keep palette bank 0.
- Set `BPLCON3.LOCT` only while writing the low RGB nibbles.
- Clear `BPLCON3` immediately afterwards so the OCS-compatible Copper list continues to update high RGB nibbles.
- `BPLCON4=0` preserves the base sprite/bitplane palette mapping.

## Visual result

OCS/ECS renders the original 12-bit (4:4:4) palette. AGA retains the same high-nibble Copper animation but adds persistent low RGB nibbles, giving 24-bit (8:8:8) colour precision to the 16 displayed palette entries. The improvement is most visible in the neon logo, raster transitions and dark floor gradients.

## Deliberately not enabled

8 bitplanes, 64-bit fetch modes, HAM8, 1280-wide modes and AGA sprite extensions are not enabled in
this v5 release. Those change bandwidth/timing/data layout and require a separate measured renderer
rather than opportunistic register writes.
