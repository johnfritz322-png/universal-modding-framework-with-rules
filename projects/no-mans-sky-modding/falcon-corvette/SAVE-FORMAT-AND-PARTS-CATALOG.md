# Corvette save format and parts catalog — VERIFIED 2026-09-18

Everything in this file was read directly from the user's live save and from the
installed game's own file listing. Nothing here is inferred.

## Save file format — VERIFIED

`save.hg` and `save2.hg` in `%APPDATA%\HelloGames\NMS\st_76561199262233576` are
**plain JSON**, null-padded at the end. They are *not* compressed.

They contain raw non-UTF-8 bytes inside some strings (glyph/coordinate fields), so
they must be read and written with `errors='surrogateescape'` to round-trip
byte-for-byte. A plain `utf-8` decode throws on byte `0x80` at offset 1892134.

## Where a Corvette build lives — VERIFIED

Path: `vLc / 6f= / F?0[]` — an array of 32 base records.

A record is a Corvette when `peI.DPp == "PlayerShipBase"`.

| Key | Meaning |
|---|---|
| `NKm` | build name |
| `CVX` (record level) | **ship slot index** the build is bound to |
| `@ZJ` | the `Objects[]` array |
| `peI.DPp` | record type: `PlayerShipBase` / `HomePlanetBase` / `FreighterBase` |

Per-object keys inside `@ZJ`:

| Key | Meaning |
|---|---|
| `b1:` | Timestamp |
| `r<7` | ObjectID, e.g. `^B_LND_B` |
| `CVX` (object level) | UserData |
| `wMC` | Position `[x, y, z]` |
| `wJ0` | Up vector |
| `aNu` | At vector |

Ship names also appear at `vLc / 6f= / @Cs[slot] / NKm`.

## Current live state — VERIFIED 2026-09-18

| Base record | Name | Type | Slot | Objects |
|---|---|---|---|---|
| 29 | `Default` | PlayerShipBase | **8** | 163 |
| 31 | `Falcon Courier` | PlayerShipBase | **7** | 295 |
| 27 | (blank) | FreighterBase | 0 | 131 |

Record 29 / slot 8 is Darth Fritz and is **unchanged** — its 163 objects match
`NMS-Corvette-Exports-20260918/Darth-Fritz-Original.json` exactly. There are exactly
two Corvettes; no third was added.

## The Corvette parts catalog — VERIFIED

Corvette parts are the "BIGGS" module set. In the shipped game file listing:

`models/common/spacecraft/biggs/modules/` — **533 scene files**.

Excluding `_placement` and `_snappoints` helper scenes, by category:

| Category | Count | Notes |
|---|---|---|
| `parts/wall/*` | 148 | interior |
| `parts/structural/structural_*` | 139 | **exterior hull tiles** — `1x1` with direction suffixes `n`, `ne`, `nw`, `new`, `netb`, each numbered 0-25 |
| `parts/wing_*` | 53 | `wing_a` … `wing_t`, most with `_l` / `_r` mirror pairs |
| `parts/connectors/connector_*` | 44 | |
| `parts/decoration/decoration_*` | 22 | |
| `parts/hab_*` | 12 | `1x1`, `1x2`, `2x2` cores |
| `parts/generators/generator_*` | 12 | |
| `parts/doorway_*` | 11 | `ns` / `ew` variants |
| `parts/airlock_*` | 10 | `airlock_ew_a`, `airlock_nesw_a..d` |
| `parts/ceiling*` | 9 | |
| `parts/floor*` | 7 | |
| `parts/gun_a..f` | 6 | turrets |
| `parts/cockpit_1x2_a/b/d` | 6 | each with an `_ext` exterior variant |
| `parts/shieldgenerator_*` | 5 | |
| `parts/zenginea..h` | 8 | main engines |
| `parts/backthruster_a/b/c` | 3 | |
| `parts/landinggear_leg_a/b/c` | 3 | |

Save `ObjectID` codes map onto these filenames directly:
`^B_LND_B` → `landinggear_leg_b`, `^B_COK_D` → `cockpit_1x2_d`,
`^B_TUR_E` → `gun_e`, `^B_WNG_Q_R` → `wing_q_r`, `^B_STR_K_NE` → structural `k`/`ne`,
`^B_HAB_B` → `hab_b_*`, `^B_SHL_E` → `shieldgenerator_e`, `^B_GEN_1` → generator.

## Toolchain — VERIFIED

MBINCompiler `v7.03.2-pre1` successfully decompiled a real asset copied out of the
installed game (Steam build `25351301`):
`gcbuildableshipglobals.global.mbin` → `.MXML`, header
`<!--File created using MBINCompiler version (7.03.2.1)-->`.

This closes the gate that `TOOLCHAIN-CHECK-2026-09-18.md` left open as an inference.

From that decompiled file:

- Corvette base scene: `MODELS/COMMON/SPACECRAFT/BIGGS/BIGGS.SCENE.MBIN`
- `ComplexityLimitWarning` = 100, `ComplexityLimitWarningNX` = 40
- Initial layout: `METADATA/SIMULATION/SHIPBASES/DEFAULTSHIPBASE.MXML`

## Course correction: drop the custom-mesh route

`REAL-FALCON-LAYOUT-RESEARCH-2026-09-18.md` offered two routes. Route 2 — model a
custom Falcon exterior in Blender/NMSDK and package it as a `.pak` — should be
**dropped**, for reasons now evidenced:

1. A Corvette has no single "exterior mesh" to replace. It is assembled at runtime
   from the 533-part catalog above, driven entirely by the `@ZJ` object list in the
   save. Replacing a part's mesh in a `.pak` changes that part **everywhere**.
2. Because the part meshes are shared, a mesh mod would also change Darth Fritz in
   slot 8. The user's hard constraint is that Darth Fritz is never modified.
3. Route 1 needs no game files touched, no `.pak` installed, and is reversible by
   restoring four save files.

Route 1 — compose the Falcon out of real catalog parts and write the `@ZJ` array —
is both safer and the method the game itself is built around.

## Why the rejected build failed

`Falcon Courier` used 295 objects built as an ellipse from repeated wing pieces. The
correct vocabulary for a Falcon silhouette is the **139 `structural_*` hull tiles**
for the saucer body and mandibles, `cockpit_1x2_d(_ext)` for the starboard cockpit,
`gun_*` for the dorsal/ventral turrets, `zenginea..h` for the full-width rear drive
band, and `airlock_*` / `doorway_*` to keep a boardable entrance.

## Still NOT verified

- The real-world size and snap geometry of each `structural_*` tile. Filenames give
  `1x1` / `1x2` footprints and a direction suffix, but not dimensions. These must be
  read out of the `_placement` / `_snappoints` scenes before a layout is trustworthy.
- Nothing about how any new build looks or whether it is boardable. That still
  requires launching the game.
