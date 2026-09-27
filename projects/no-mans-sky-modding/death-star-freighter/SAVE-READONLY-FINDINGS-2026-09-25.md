# Owned freighter save record — read-only findings

Recorded 2026-09-25, America/Denver. This check read the live save data only;
no save, manifest, game archive, or game configuration was modified.

## VERIFIED — Primary

Both current saves, `save.hg` and `save2.hg`, decode as the game's LZ4 save
container and identify the player's freighter as `Mothership`. Their current
freighter records agree exactly:

- Resource filename:
  `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`
- Seed: enabled, `0x89D78FF0C1755CDC`
- Alternate ID: empty

The save-record resource is the same capital-freighter scene investigated in
`FREIGHTER-SELECTION-FINDINGS.md`. This verifies that Mothership uses that
capital-freighter model family and establishes the exact current seed value.

## Method and evidence boundary

The existing local `hgsave.py` decoder was used read-only to decode the live
`.hg` containers. In the current obfuscated schema, the record is at JSON
pointer `/vLc/6f=/bIR`; it contains the filename and seed above. The player
freighter display name is separately stored at `/vLc/6f=/vxi`. A teleporter
endpoint also carries the same display name, so the name alone must not be
used as evidence of the owned-freighter model record.

The checked `save.hg` SHA-256 was
`EB24D74970F7F84BFBF3BA4D9E317F38DCAB3DC6E45CDCAAADE88B878AD40CD8`; the
checked `save2.hg` SHA-256 was
`2FB5B2BDB8576549DFB2A8BE676B80DDB704D0B53DBD3AEDD168D66A75F8381F`.

## What this does not prove

This does **not** prove that adding an external scene/descriptor entry can be
selected by this seed, that selection can be isolated to one owned freighter,
or that a custom hull will preserve docking and interiors. Those remain
**UNVERIFIED**. The next independent gate is a minimal scene/geometry
import-export round trip using the dedicated Blender 5.0.1/NMSDK profile.
