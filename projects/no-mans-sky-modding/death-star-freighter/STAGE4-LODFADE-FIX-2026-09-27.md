# Stage 4 overlay LOD-fade fix — 2026-09-27

## Result

**DEPLOYED — awaiting in-game visual test. Not yet confirmed working.**

## Symptom (John's three-angle test after the material fix)

- Solid-color material swap alone did not fix the see-through look.
- Up close, the shell looked "noticeably more solid and shaded."
- Viewed from below, still see-through.
- After flying through/into the shell, it disappeared completely; a shot
  taken at that point showed only the stock hull.

## Ruled out first: geometry/winding

Before chasing another material theory, independently verified the exact
deployed shell file is geometrically sound:

- Re-imported `DEATH_STAR_SILHOUETTE_STAGE4.SCENE.MBIN` (the file actually
  in `GAMEDATA/MODS`) through NMSDK and measured real face normals on the
  reimported mesh: 9108 of 9208 faces point outward (the remaining ~1% are
  edge-loop faces at the trench/aperture boundary, expected).
- Rendered that same imported mesh myself with backface culling enabled,
  matching how a renderer draws it: a fully solid, gapless opaque sphere
  from every controllable angle.

This ruled out winding/culling as the cause of what John was seeing, so no
winding change was made this pass — flipping it again would have made
things worse.

## Cause: `EnableLodFade`

Decompiled the material actually in use (`HullPanels_Mat`, from the
material-fix pass) and found `EnableLodFade="true"`. That's a
distance-based fade meant for ordinary small ship-part-sized objects.
John's symptom pattern — mostly solid at one middle distance, fading both
up close and from other angles/distances, vanishing entirely once the
camera passed inside it — matches a fade curve tuned for something a few
tens of units across being applied to a shell roughly **2100+ units**
across. Confirmed the exported geometry's own bounding box is correct
(`MeshAABBMin/Max` ≈ ±2118 to ±2141, matching the real shell size), so the
bounding volume itself isn't the problem — the fade behavior is.

## Fix

Did not edit the shared stock `HullPanels_Mat.MATERIAL.MBIN` (that's a
real game file used by the freightship01 wreck elsewhere). Instead:

1. Decompiled it to EXML, copied it unchanged except renaming to
   `DeathStarHullMat` and setting `EnableLodFade="false"`.
2. Compiled that to `DEATHSTARHULLMAT.MATERIAL.MBIN`.
3. Placed it as this mod's own asset, alongside the shell geometry, at
   `CUSTOMMODELS/DEATH_STAR_SILHOUETTE_STAGE4/DEATHSTARHULLMAT.MATERIAL.MBIN`,
   and pointed the shell mesh at that path instead of the stock file.
4. Updated `tools/pack_overlay_mod.py`'s required-file set to include this
   fifth file (previously hard-coded to expect exactly four).
5. Rebuilt the shell through Blender/NMSDK, rebuilt the overlay staging
   tree (same transform fix as before), compiled, and byte-verified the
   full 5-file package via `pack_overlay_mod.py`
   (`OVERLAY_ARCHIVE=passed files=5 ... byte_identical=true`).
6. Backed up the prior (material-fixed, still fading) build to
   `2026-09-26/who-x20/work/backups/pre-lodfade-fix-20260926-224254/`,
   then deployed all 5 files to `GAMEDATA/MODS/DeathStarFreighterOverlay/`
   and byte-verified each one after copying.

## What was deliberately left unchanged

Position and winding were untouched this pass — both already verified
correct. This isolates `EnableLodFade` as the one new variable.

## Next test

Launch, summon Mothership, and check from multiple distances/angles
including up close and from below — the same views John already reported
on. If the shell now stays solid regardless of distance/angle, this is
resolved and the remaining open items are purely cosmetic/scope (exact
vertical alignment, whether to scale up to fully enclose the hull) and the
long-standing gates (collision, docking safety) already tracked in
`RUNTIME-ATTACHMENT-EVIDENCE-PLAN.md`. If it still fades, that rules this
out too and needs fresh evidence rather than another guess.
