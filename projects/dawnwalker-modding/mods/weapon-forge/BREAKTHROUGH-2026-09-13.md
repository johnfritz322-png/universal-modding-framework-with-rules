# The override works. Read this first.

After six crashing attempts, one route now **works end to end**: a DataTable
override loads, is honoured, and changes what the game renders.

## Proven in game

Patched four FName indices in `DT_WeaponAppearances` to repoint
`ITM_Weapon_SwordVampiric1a` (The Vrakhir) from `L_Sword_Vampiric_01` to
`M_Sword_Gargoyle_01`, repacked with retoc, installed. A read-only probe in the
running game reports:

```text
L_Sword_Vampiric_01 loaded=false      <- the stock blade is not even loaded
M_Sword_Gargoyle_01 loaded=true
x2  M_Sword_Gargoyle_01               <- live components in the scene
x1  M_Sword_Gargoyle_01_Scabbard
VERDICT=OVERRIDE_LIVE
```

The game resolved the item to our blade. **No crash.** That is the first time
anything this project built was accepted and acted on.

## The one open question

Whether those Gargoyle components are on **the player pawn** or on an NPC that
also uses that blade. Probe v3 (deployed, not yet run) answers it by comparing
each holder against the real pawn.

- `isPlayerPawn=true` → done; the technique generalises to all 206 weapons.
- `isPlayerPawn=false` → the player's drawn blade comes from somewhere the table
  does not reach. Next suspects: `AppearanceSubsystem.ItemAppearanceMap`, the
  equip path, or a story-scripted weapon. Note the test save is in
  `Map_Blockout_Valley` with a `CS004_wakeUp` cutscene actor present, so it is
  worth confirming the sword in hand is the inventory weapon at all.

## How to reproduce the working build

1. **Hardlink view of Paks** — retoc cannot build a composite across the base and
   `DualSenseAtlas` (different TOC versions). Hardlink `global.utoc`,
   `global.ucas`, `Dawnwalker-Windows.{utoc,ucas,pak}` into a scratch folder.
2. **Extract**, with the key **before** the subcommand:
   `retoc -a <key> to-legacy -f DT_WeaponAppearances <view> <out>`
   This also emits `scriptobjects.bin` (3,837,469 B) — **the ingredient every
   failed build lacked.**
3. **Patch** the `.uexp`. Both source and target names are already in the table's
   name map, so index swaps are size-neutral:
   ```text
   offset 8186  blade     103/583 -> 109/589
   offset 8206  scabbard  104/584 -> 110/590
   ```
   Row name `ITM_Weapon_SwordVampiric1a` sits at 8176. Each pattern occurs once.
4. **Repack**: `retoc to-zen --version UE5_5 <legacy dir> <out>.utoc`
   `scriptobjects.bin` must be in the input directory.
5. **Verify**: `verify_container.py` → expect 2 chunks, 1 collision on
   `0x2b6fc8ead9260336`.
6. **Install** the `.pak`/`.ucas`/`.utoc` trio into `~mods`.

## What does NOT work, and why

**Stock-UE-cooked StaticMesh will not load in this game.**

```text
Serial size mismatch: Expected read size 17488, Actual read size 18589
```

The game's reader consumes 1,101 bytes more than our package declares — its
engine expects `UStaticMesh` fields stock UE 5.5.4 does not write. Proved by
control: a plain engine cube fails identically to a custom sword, and the game's
*own* mesh round-tripped through retoc renders fine. Material, collision and
Nanite all ruled out (Nanite twice, verified by readback).

**So: data changes work, new geometry does not.** Any near-term win comes from
repointing, stats, and effects — not custom meshes.
