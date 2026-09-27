# Stage 4 overlay transform fix — 2026-09-27

## Result

**DEPLOYED — awaiting in-game visual test. Not yet confirmed working.**

## Symptom (John's in-game screenshot, first Stage 4 test)

Mothership summoned successfully (no repeat of the earlier breakage). The
Death Star shell rendered, but: looked washed out / see-through, sat offset
away from the ship, and the stock Mothership hull was still fully visible
beside it rather than enclosed by the shell.

## Root cause found: reference node had no translation

`tools/build_death_star_silhouette_stage3.py` places the shell's Blender
root empty at the measured donor bounding-box centre
`(1.020752, 1956.979401, -135.783936)` purely so the QA renders frame the
model correctly. That placement was assumed to carry through to the
exported scene, but it does not: decompiling the exported
`DEATH_STAR_SILHOUETTE_STAGE4.SCENE.MBIN` shows its root node's own
`Transform` is `(0, 0, 0)` — NMSDK does not bake a reference-scene root's
world position into the file; a scene meant to be reused via `REFERENCE`
always exports at local identity and expects whoever references it to
supply the placement.

`tools/build_overlay_mod.py` (both Codex's original and this session's
Stage 4 rebuild) injected the `DeathStarExteriorOverlay` `REFERENCE` node
with `TransX/TransY/TransZ` hard-coded to `0.000000`. So the shell was
loading at the capital scene's own local origin — about 1957 units away
from the freighter hull's actual position — which matches exactly what was
seen: a separate, offset shape with the real ship still visible on its own.

## Fix

Added `--trans-x/--trans-y/--trans-z` to `build_overlay_mod.py`, applied to
the injected `REFERENCE` node's transform. Rebuilt the overlay staging tree
with the same donor-centre coordinates already used for the shell geometry,
compiled, and decompiled the result back to confirm the injected node now
carries `TransX=1.020752 TransY=1956.97937 TransZ=-135.783936`. The
previously-deployed (offset) build was backed up to
`2026-09-26/who-x20/work/backups/pre-transform-fix-20260926-221418/` before
being replaced. All four files were byte-verified against the freshly
built, compiled staging tree after copying into
`GAMEDATA/MODS/DeathStarFreighterOverlay/`.

## What was deliberately left unchanged this pass

The "washed out / see-through" material appearance was **not** touched in
this pass — only the position was fixed, to test one variable at a time.
The shell mesh still uses
`MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC/FREIGHTERPROC_MAT.MATERIAL.MBIN`,
which is confirmed `Opaque` (not the cause of transparency by material
class), but is a `_PROC` procedural-texture material that normally expects
per-instance texture/tint data supplied by the freighter's own generation
system — data a plain static NMSDK mesh reference does not provide. That
is the leading suspect for the washed-out look, but it has not been
verified, and should only be investigated after confirming whether
correct positioning alone changes what's seen (lighting/backdrop differed
significantly out in open space near the origin vs. against the actual
hull).

## Next test

Launch the game, summon Mothership, and look at the exterior only. Compare
against the last screenshot: is the shell now positioned against/around the
actual hull? If yes but still washed out, the material is the next fix. If
still offset or otherwise wrong, report exactly what's seen — do not guess
further blind.
