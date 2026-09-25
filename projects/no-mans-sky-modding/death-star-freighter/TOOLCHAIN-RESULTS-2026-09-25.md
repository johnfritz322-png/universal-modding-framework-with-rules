# Toolchain results — 2026-09-25

## VERIFIED

- Installed game: Cosmos 7.04, Steam build `25441199`.
- Blender 4.5.14 LTS launches successfully. Its executable SHA-256 is
  `57FA1D294EA76448C3BEC84CA758CAF4629611330ABBA7DCF55BB0C56A0A15AB`.
- HGPAKtool 1.1.3 extracted a copied `NMSARC.globals.pak` from this build.
- MBINCompiler reports version `7.03.2.1` in generated MXML and passed a
  no-edit round trip on `gcscratchpadglobals.global.mbin`: MBIN -> MXML ->
  MBIN -> MXML. The two MXML outputs had identical SHA-256 hashes.

## BLOCKED / NEEDS FOLLOW-UP

- NMSDK source is on its `cosmos_fixes` branch at `548bfe1` (2026-09-16),
  but its add-on did not load in Blender because Python could not import
  `hgpaktool`. Do not call NMSDK verified until that dependency is installed
  and the add-on loads.
- A read-only filtered extraction of current game archives found freighter
  assets under `MODELS/COMMON/SPACECRAFT/`, including `BIGGS` and
  `COMMONPARTS/HANGARINTERIORPARTS`. It did not yet identify the procedural
  seed-to-hull lookup table. That architecture remains HIGH CONFIDENCE.

No game files or save files were modified.
