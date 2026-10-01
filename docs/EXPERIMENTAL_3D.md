# Experimental solid 3D path — quarantine contract

The release binary uses the double-buffered wireframe renderer in `src/main.s`.
Solid polygons, per-face lighting, a procedural sphere, particles and painter
sorting are **not shipping features**. Earlier snapshots mixed prototype code
into the production translation unit and described it as complete; this pass
removes that ambiguity.

## Correct data contracts

The old cube record was 8 bytes (`normal[3] + vertex[4] + material[1]`), not 10.
The old octahedron record was 7 bytes (`normal[3] + vertex[3] + material[1]`),
not 10. Any future decoder must use explicit record-size constants rather than
magic pointer increments.

`BlitLine` takes `(d0,d1) -> (d2,d3)` and requires its caller to preset the
shared line-mode blitter registers. The former prototype passed coordinates in
other registers and therefore was not ABI-correct.

## Display constraint

The active display is four bitplanes (`BPLCON0=$4200`), so only colour indices
0–15 exist. The prototype's 24–31 shade range could never be displayed. A real
solid renderer must either compose a legal 4-bit colour across the four planes,
reserve selected planes for the object, or intentionally redesign the display.

## Definition of done

A solid renderer is eligible for `src/main.s` only after all of these are true:

1. Face normals are transformed consistently with object rotation.
2. Front-face winding and back-face culling are specified and tested.
3. Geometry is clipped before bitplane address calculation.
4. Filled polygons are actually filled; an outlined quad is not called solid.
5. Colour writes respect the active bitplane count.
6. Every blitter launch obeys ownership, wait, modulo and mask invariants.
7. Rendering targets only the hidden wire buffer until swap.
8. Static validation plus assembled 68000 execution tests cover the new path.
9. At least one framebuffer/golden-frame check proves visible output semantics.

`src/phase2c_drawsolid.s` is therefore a research contract, not a build source.
