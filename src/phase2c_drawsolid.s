; NEON VECTORS — experimental solid renderer research module
; ----------------------------------------------------------
; NOT included by src/main.s and NOT part of the release binary.
;
; This file preserves the next renderer direction without pretending that an
; outline is a filled/Gouraud polygon renderer.  It documents the ABI and data
; layout that a future implementation must satisfy before integration.
;
; Production BlitLine ABI (src/main.s):
;   d0=x1, d1=y1, d2=x2, d3=y2, a0=destination plane, a6=CUSTOM
;   caller presets BLTCMOD, BLTDMOD, BLTADAT, BLTBDAT, BLTAFWM, BLTALWM.
;
; Face record contracts used by the abandoned prototype:
CUBE_FACE_BYTES EQU 8      ; nx.b,ny.b,nz.b,v0.b,v1.b,v2.b,v3.b,material.b
OCTA_FACE_BYTES EQU 7      ; nx.b,ny.b,nz.b,v0.b,v1.b,v2.b,material.b
;
; OCS display contract:
;   BPLCON0=$4200 => four displayed bitplanes => palette indices 0..15 only.
;   A future solid renderer must either draw a 4-bit index into all required
;   planes or reserve a subset of planes/colours. Values 16..31 are impossible
;   without changing the display mode to five bitplanes.
;
; Required integration stages (none are falsely exported here):
;   1. transform face normals with the same object matrix as the vertices;
;   2. back-face cull in a documented winding convention;
;   3. clip polygons/edges to the MID band before any blitter address math;
;   4. depth-order intersecting objects or use a visibility-safe alternative;
;   5. implement actual polygon fill (edge draw + area fill or span fill);
;   6. map lighting to legal 0..15 palette indices / bitplane masks;
;   7. prove blitter ownership/waits and hidden-buffer-only writes;
;   8. add emulator-visible golden-frame or framebuffer invariants.
;
; This deliberately contains no callable DrawSolid symbol.  An unfinished
; renderer therefore cannot be linked accidentally by adding this file to SRCS.
