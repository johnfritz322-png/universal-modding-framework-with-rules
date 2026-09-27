# Stage 4 overlay material fix — 2026-09-27

## Result

**DEPLOYED — awaiting in-game visual test. Not yet confirmed working.**

## Symptom (John's screenshot after the transform fix)

The shell now sits on/around the ship instead of floating off to the side
(the transform fix worked) — hull may sit slightly low relative to the
sphere, possibly just camera angle. Panel banding is visible on part of the
sphere. The shell is still washed out / see-through.

## Cause

The shell mesh used
`MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC/FREIGHTERPROC_MAT.MATERIAL.MBIN`.
Decompiled and inspected it: it is `Opaque` (not a transparency-class
material) but its `Metamaterial` field points at
`FreighterProc_Mat.metamaterial.mXml` — a procedural substance material
that Mothership's own generation system normally supplies per-instance
texture/tint/wear data to at spawn time. A plain static NMSDK mesh
reference never provides that per-instance data, so the shader has nothing
valid to sample — consistent with a flat, washed-out, semi-transparent
render (the partially-visible panel banding matches getting *some* geometry
detail through but no real material response).

## Fix

Switched the shell's material to
`MODELS/COMMON/SPACECRAFT/INDUSTRIAL/FREIGHTSHIP01/HULLPANELS_MAT.MATERIAL.MBIN`
(`tools/build_death_star_silhouette_stage3.py`). Decompiled and confirmed
this one: `Opaque`, empty `Metamaterial` field (no procedural substance
dependency at all), a real static diffuse texture
(`TEXTURES/COMMON/SPACECRAFT/SHARED/HULLPANELS.DDS`), used as-is on the
`freightship01` derelict-freighter model — a material designed to always
resolve the same way regardless of what references it.

Re-exported the shell through Blender/NMSDK with the same winding fix as
before, confirmed the new `MATERIAL` attribute in the decompiled scene
points at `HULLPANELS_MAT.MATERIAL.MBIN`, then rebuilt the overlay staging
tree with `build_overlay_mod.py` using the **same transform fix from the
previous pass** (`1.020752, 1956.979401, -135.783936`) so both fixes are
combined in one deployed build. Compiled with MBINCompiler and byte-verified
after copying into `GAMEDATA/MODS/DeathStarFreighterOverlay/`.

The previous (transform-fixed, still-washed-out) build was backed up to
`2026-09-26/who-x20/work/backups/pre-material-fix-20260926-222125/` before
being replaced.

## What was deliberately left unchanged

Position was not touched again this pass — John's screenshot showed it may
be sitting slightly high, but that read could just as easily be camera
angle, and there wasn't clear enough evidence to justify another position
change on top of the material change. If it's still visibly off after this
material fix, that's a separate, precise fix (small Y adjustment), not a
guess to make now.

## Next test

Launch the game, summon Mothership. Does the shell now render as a solid,
opaque hull-panel surface instead of see-through? If yes, next real
questions are exact vertical placement and whether it should be scaled up
(`--expanded-shell`) to fully enclose the ship — both trivial once the
render itself is confirmed correct. If still see-through, that rules out
the procedural-material theory and needs a fresh look rather than another
guess.
