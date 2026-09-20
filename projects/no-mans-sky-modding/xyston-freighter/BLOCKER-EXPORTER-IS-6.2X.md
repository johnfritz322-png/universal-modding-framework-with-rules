# The blocker: NMSDK's exporter has not been updated for game version 7.x

**VERIFIED 2026-09-20 from NMSDK's own git history.** This supersedes every
rendering theory in `TEARING-INVESTIGATION.md`.

## The evidence

Commit `548bfe1`, "Update for Cosmos and temporarily remove importing of normals",
dated 2026-09-16, changes exactly six files:

    src/addon/nmsdk/ModelImporter/SceneNodeData.py
    src/addon/nmsdk/ModelImporter/import_scene.py
    src/addon/nmsdk/NMS/LOOKUPS.py
    src/addon/nmsdk/blender_manifest.toml
    src/addon/nmsdk/serialization/NMS_Structures/NMS_types.py
    src/addon/nmsdk/serialization/NMS_Structures/Structures.py

**Not one file under `ModelExporter/`.**

- Last commit touching the exporter: `a62dffc`, **2026-04-25**.
- Newest model format the project claims: `9e7dec8`, **"support for 6.2X model format"**.
- The game here is **7.03.1**.

The Cosmos commit also **comments out normal importing entirely** and leaves debug
code writing `7.x.normals_and_tangents.floats.txt`, i.e. the maintainer is still
working out how 7.x stores normals and tangents.

## Why that explains what we saw

Our exported geometry declares `normal:int_2_10_10_10, tangent:int_2_10_10_10` — the
6.2X layout, and precisely the data the maintainer cannot yet read back on 7.x.

A mesh written in a vertex format the engine no longer expects gives exactly the
observed behaviour: a few detached fragments during the warp-in animation, then
nothing once the ship is placed.

## What this does not mean

Every fault found before this was real, and all are fixed:

- mods globally disabled in `GCMODSETTINGS.MXML`
- wrong template GUID in the scene header
- mixed forward and backslashes in internal paths
- the scene naming itself one folder too deep
- geometry installed in the wrong folder
- inside-out normals on every sphere and cylinder
- untriangulated quads, which NMSDK's own docs warn about
- texture tile stretched roughly fiftyfold
- zero-area faces from the cylinder cap fans

None of them could have made the ship render, because the vertex format itself is
wrong for this game version. They were worth fixing and they were not the answer.

## Options

| Option | Assessment |
|---|---|
| Wait for NMSDK 7.x export support | The maintainer is actively working on 7.x. No timeline |
| Write the 7.x geometry serialiser | Real work, and the format is still being reverse-engineered by someone with far more context |
| **Build the ship from in-game Corvette parts** | Needs no custom mesh. Proven on this save — a 1,495-part Millennium Falcon exists in game. A Star Destroyer wedge is a far simpler shape than a Falcon |
| Revert to stock | `rm -rf "D:/steam/steamapps/common/No Man's Sky/GAMEDATA/MODS/XystonFreighter"` |

The non-mesh mods in this project are unaffected and work by different means:
`XystonFreighterMaxed` (upgrade rolls, ship parking) and `CorvetteExtras`
(teleporter, hatch) are EXML table patches, not geometry.
