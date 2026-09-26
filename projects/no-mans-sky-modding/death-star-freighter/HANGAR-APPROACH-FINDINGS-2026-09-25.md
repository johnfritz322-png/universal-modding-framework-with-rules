# Hangar approach findings — 2026-09-25

## Scope

Read-only inspection of freshly extracted current-game industrial freighter
assets. No mod asset, package, game file, or save was changed.

## Verified observations

- The capital root exposes `HANGARROOTA` and `HANGARROOTB` locator nodes;
  their accumulated positions were previously measured in
  `BLENDER-ROUNDTRIP-2026-09-25.md`.
- `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/ACCESSORIES/HANGARA.SCENE.MBIN` exists
  in the installed game and is a full stock hangar module, not merely a name.
- Its scene contains a `HangarA` locator, docking references (`Dock1A` through
  `Dock3C`), a `REFHangarDoorway` reference, and an `Approach2c` locator. The
  latter has local transform `(0, 0.821991, -127.452271)` in the hangar scene.
- `REFHangarDoorway` is locally translated `(0, 0, -39.636480)` with a
  `180°` Y rotation.
- Freshly extracted `GCAISPACESHIPGLOBALS.GLOBAL.MBIN` explicitly declares
  `LegacyHangarFilename` as
  `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/ACCESSORIES/HANGARA.SCENE.MBIN`.
  This verifies that `HANGARA` is an engine-configured freighter hangar
  module, rather than an unused similarly named asset.

## Unresolved attachment boundary

The inspected capital root scene and descriptor do not directly contain a
`HANGARA` reference path. A binary search of the extracted industrial assets
found the `HANGARROOT*` names only in capital root scenes, while the approach
names occur inside the engine-configured hangar module. The bridge between
those roots and the runtime-selected hangar module is therefore **UNVERIFIED**.

The module's local approach/docking data is useful evidence that a hangar
opening has a nontrivial orientation and clearance requirement. It is not
enough to derive a world-space opening in the Death Star shell.

## Consequence

Do not cut a permanent or installable shell opening from the current locator
coordinates. First establish which stock hangar module attaches to Mothership,
which root it uses, and its accumulated runtime transform. A temporary visual
opening may be made later only if it remains explicitly non-installable and
does not claim dockability.
