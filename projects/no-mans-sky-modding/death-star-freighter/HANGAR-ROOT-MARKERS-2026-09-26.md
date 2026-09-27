# Hangar-root marker export — 2026-09-26

## Result

**PASS — scratch-only diagnostic asset exported and its mesh stream loaded
back through NMSDK.**

`tools/build_hangar_root_markers.py` creates two simple original marker meshes
at the accumulated capital-root positions previously measured for
`HANGARROOTA` and `HANGARROOTB`:

- `HANGARROOTA_MARKER`: `(0, 295.910309, 226.413742)`
- `HANGARROOTB_MARKER`: `(0, 184.549149, 553.673706)`

The asset was exported with the dedicated Blender 5.0.1/NMSDK profile to a
scratch-only directory outside this repository. NMSDK wrote the scene and
geometry files, reporting 42 indices for marker A and 672 indices for marker
B. `tools/verify_exported_scene_mesh.py` then loaded the generated scene's
mesh stream successfully (`EXPORTED_SCENE_MESH_LOAD=passed`).

## Scope and limitation

This asset is only a future diagnostic aid for a separately reviewed,
stock-root observation method. It does not alter a game archive, save,
installed mod, stock freighter scene, collision, or docking data.

The marker coordinates originate from static capital-root measurements. They
do **not** identify the active runtime hangar module or its transform. The
attachment/clearance gate in `RUNTIME-ATTACHMENT-EVIDENCE-PLAN.md` remains
open; do not package or install these markers as a Death Star mod.

## Reproduction

Use the dedicated Blender profile specified in `NMSDK-REPAIR-2026-09-25.md`,
then run the marker generator followed by the direct mesh-load verifier
against `DEATH_STAR_HANGAR_MARKERS.SCENE.MBIN`.
