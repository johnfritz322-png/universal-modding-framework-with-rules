# Xyston-class Sith Star Destroyer as an NMS capital freighter

Goal: replace the player's capital freighter with a Xyston-class Sith Star Destroyer
(the Final Order / Exegol fleet from *The Rise of Skywalker*), rebuilt at a much
larger scale than the vanilla freighter.

Date opened: 2026-09-19. Status: **research only, nothing built, nothing installed.**

---

## Target platform — VERIFIED

| Item | Value | How it was verified |
|---|---|---|
| Game version | No Man's Sky 7.03.1 "Cosmos" | Steam `appmanifest_275850.acf` buildid `25351301`, cross-checked against a Nexus mod that names build 25351301 as 7.03.1 |
| Install path | `D:\steam\steamapps\common\No Man's Sky` | on disk |
| Mods enabled | yes | `GAMEDATA\PCBANKS\ENABLEMODS.TXT` present; `GAMEDATA\MODS\` exists and holds no mods |
| Player freighter | capital, industrial | save key `/vLc/6f=/bIR/93M` = `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN` |

## Mod format for 7.x — VERIFIED

`.pak` mods stopped working at game version 5.50. Mods are now **plain folders**
under `GAMEDATA\MODS\<ModName>\`, mirroring the game's internal paths, containing
`.MBIN` (full file replacement) or `.EXML` (targeted patch) files. `DISABLEMODS.TXT`
is no longer used.

Source: Gumsk's mod index on Nexus (mods/1541), and live 7.03 mods on Nexus that
document their own install path, e.g. `MODS\CameraSensitivityFix\GLOBALS\GCCAMERAGLOBALS.GLOBAL.EXML`.

A custom *model* cannot be an EXML patch — it needs replacement `.MBIN` scene and
geometry files, so this will be a replacement-style mod.

## The existing Star Wars freighter mod is dead — VERIFIED

`gFreighter Custom Freighters` (Nexus mods/2200, Gumsk) added SW Imperial II,
SW Venator, SW Harrower and SW Annihilator as capital freighters, selected by
save-edited seed (`0x0`, `0x2F`, `0x1`, `0x1E`).

It is version 5.1.2.0a, last updated 29 September 2024, and the author's own index
lists it as **"Compatible? No"**. It predates the 5.50 format change. It cannot be
installed on 7.03.1 and there is no updated equivalent. There has never been a
Xyston-class mod.

## Frigates are the wrong target — VERIFIED

Frigate appearance cannot be changed. There is no in-game customisation, and of the
31 frigate mods on Nexus every one is stats, salvage rates, fleet economy or an LOD
fix — none touches a frigate model. The capital **freighter** is the correct target:
it is the ship the player walks around in, and its model is a single replaceable scene.

---

## How the vanilla capital freighter is built — VERIFIED by decompiling it

Extracted `models/common/spacecraft/industrial/capitalfreighter_proc.scene.mbin`
from `NMSARC.EntitySceneMBIN.pak` and decompiled it with MBINCompiler 7.03.2-pre1.
111 nodes: 1 MODEL, 6 LOCATOR, 17 MESH, 87 REFERENCE.

```
[MODEL]     CAPITALFREIGHTER_PROC              -> CAPITALFREIGHTER_PROC.GEOMETRY.MBIN
  [LOCATOR]   _Hull_A3            SCALE = 6            <-- master scale
    [MESH]      _Hull_A1          SCALE = 0.5
      [REFERENCE] _Base_A         SCALE = 2   @(0,-20,0)   -> HULL_B.SCENE.MBIN
      [REFERENCE] _HullSide_C1    SCALE = 2               -> HULLWINGS_C.SCENE.MBIN
      [REFERENCE] _HullBBot_C1    SCALE = 2   @(0,-87,2)  -> THRUSTERUNIT.SCENE.MBIN
      [REFERENCE] _HullBBot_C2    SCALE = 2   @(0,-72,1)  -> HULLBOTTOM.SCENE.MBIN
      [REFERENCE] _HullBTop_B     SCALE = 2   @(0,38,18)  -> HULLTOP.SCENE.MBIN
      [REFERENCE] Freighter_Medium1 SCALE = 0.333333      -> INVENTORY_MEDIUM.SCENE.MBIN
    [MESH]      _Hull_A2          SCALE = 0.5
      [REFERENCE] _HA2B_1         SCALE = 1.5 @(0,206,20) -> BRIDGEA.SCENE.MBIN
      [REFERENCE] _HA2B_2         SCALE = 1.5 @(0,206,20) -> BRIDGEB.SCENE.MBIN
      [LOCATOR]   HANGARROOTB     SCALE = 0.333333 @(0,185,-62)
      [REFERENCE] Freighter_Medium SCALE = 0.333333       -> INVENTORY_MEDIUM.SCENE.MBIN
  [LOCATOR]   MaintenanceSlot1                @(-1,81,80)
  [LOCATOR]   MaintenanceSlot0                @(1,23,-343)
```

### The scale finding, and why it matters

The capital freighter is not modelled at its final size. **Hello Games scale it up
with a scene-node scale of 6 on `_Hull_A3`**, then halve it again on the hull meshes,
giving a net 3x on hull geometry.

The player-facing attachments are deliberately **scale-compensated back to 1.0**:

    HANGARROOTB:  6 x 0.5 x 0.333333 = 1.0
    Freighter_Medium: 6 x 0.5 x 0.333333 = 1.0

So the hangar and the inventory volume render at true world scale no matter what the
hull scale is. That is the mechanism that makes "make it huge" plausible: the hull
scale and the player-usable scale are already separated by design, by the developers,
in the shipped file.

**UNVERIFIED / NEEDS TESTING:** that raising `_Hull_A3` above 6 actually enlarges the
ship in game rather than being overridden by a gameplay global; and what breaks when
it does — hangar approach path, landing trigger volume, the freighter teleporter,
warp-in animation, capital-ship collision, LOD swap distances, and the space-map icon.
Nothing here has been installed or launched. Do not claim any of it works.

---

## Toolchain — VERIFIED present and version-matched

| Tool | Version | Location | Purpose |
|---|---|---|---|
| HGPAKtool | 1.1.3 | `work/nms-toolchain/HGPAKtool-1.1.3/hgpaktool.exe` | list and extract `.pak` archives |
| MBINCompiler | 7.03.2-pre1 | `work/nms-toolchain/MBINCompiler-v7.03.2-pre1/` | `.MBIN` <-> `.MXML`, matches the live game version |
| NMSDK | 0.10.0-alpha13 | `work/NMSDK` | Blender add-on, custom models into NMS |
| Blender | 4.5.9 LTS portable | `work/nms-toolchain/blender/` | modelling (downloaded 2026-09-19) |

Full archive index built for all 97 paks: 194,605 files. The previous index covered
only `NMSARC.MetadataEtc.pak`.

### The real risk is the mesh export, not the scale

NMSDK's last tagged release is v0.9.28 (October 2024), which predates the 5.50 format
change. The active work is on the **`cosmos_fixes` branch**, whose head commit is
**2026-09-16, "Update for Cosmos and temporarily remove importing of normals"** — three
days before this was written. So custom-model support for 7.x is being repaired right
now, in alpha, on a branch.

Supporting evidence that custom meshes are currently a frontier and not a solved path:
searching Nexus for custom-model mods returns only 2019-era mods. Nobody has shipped a
new custom ship mesh for the 5.50+ format that could be found.

**Conclusion: the mesh pipeline must be smoke-tested with a throwaway shape before any
Star Destroyer is modelled.** Modelling first and discovering the exporter is broken
would repeat the mistake made on the Falcon build.

---

## Plan, in dependency order

1. **Scale test first.** Rebuild the vanilla scene with `_Hull_A3` raised and the
   hangar/inventory nodes compensated, install as a MODS folder, launch, look. This
   needs no Blender and no custom mesh, and answers the biggest unknown — whether
   "huge" is possible at all, and what breaks.
2. **Mesh smoke test.** Export a trivial shape (a box) through Blender + NMSDK
   `cosmos_fixes` and get it to appear in place of the freighter hull. Proves the
   exporter works on 7.03.1 before any art time is spent.
3. **Model the Xyston hull.** 2,400 m wedge, flat-bottomed, with the axial cannon
   trench along the belly. Geometrically simple — flat planes — unlike the Falcon.
4. **Reattach the player-facing parts** at the right world scale: hangar, teleporter,
   inventory, maintenance slots, bridge.
5. **Materials and the red axial glow.**

## Backup rule carried over from the Falcon work

Take a fresh four-file save backup before every write that touches the save, and
restore only the affected subtree, never the whole file. Twenty-three backups were
taken during the Falcon build and three were needed.
