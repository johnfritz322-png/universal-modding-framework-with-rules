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
- The same current-build globals file declares `HangarFilename` as
  `MODELS/COMMON/SPACECRAFT/COMMONPARTS/HANGARINTERIORPARTS/HANGAR.SCENE.MBIN`.
  That separately extracted scene contains `Approach1a` through `Approach3c`,
  nine `Dock*` references, three animated hangar-door references, and explicit
  collision nodes. It is therefore the current configured hangar scene, with
  a larger runtime/collision surface than the legacy module.
- The freshly extracted `HANGARA.ENTITY.MBIN` supplies an actual
  `GcOutpostComponentData` docking configuration: `ApproachRange=45`,
  `ApproachAngle=80`, `PlayerAutoLandRange=280`,
  `DockingAttractRange=3003`, `DockingAttractConeAngle=90`, and
  `DockingAttractFacingAngle=10`. It also declares `HANGARDOOR` and
  `RotateToDock=true`.
- The current hangar's approach nodes form a local three-column grid:
  `Approach1*` at X `-45.3307762`, `Approach2*` at X `0`, and `Approach3*` at
  X `45.3307762`; all are at Y `0.302928` and Z between `-74.875460` and
  `-77.136600`. This confirms a minimum local doorway/approach span of
  `90.6615524` units before adding clearance.

## Unresolved attachment boundary

The inspected capital root scene and descriptor do not directly contain a
`HANGARA` reference path. A binary search of the extracted industrial assets
found the `HANGARROOT*` names only in capital root scenes, while the approach
names occur inside the engine-configured hangar module. The bridge between
those roots and the runtime-selected hangar module is therefore **UNVERIFIED**.

The modules' local approach/docking data is useful evidence that a hangar
opening has a nontrivial orientation and clearance requirement. The entity
values establish approach/docking tolerances, but they are not enough to derive
a world-space opening in the Death Star shell.

## Consequence

Do not cut a permanent or installable shell opening from the current locator
coordinates. First establish which stock hangar module attaches to Mothership,
which root it uses, and its accumulated runtime transform. A temporary visual
opening may be made later only if it remains explicitly non-installable and
does not claim dockability.
