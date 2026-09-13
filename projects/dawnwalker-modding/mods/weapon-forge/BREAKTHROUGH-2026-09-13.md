# Visual replacement works. Read this first.

> **Scope, stated plainly: this replaces the appearance of an EXISTING weapon.**
> It does **not** create a new inventory item. The additive-item goal is a
> separate, still-unsolved problem — see `OWN-ITEM-ROUTE-2026-09-12.md` and
> `REGISTRATION-LEAD-2026-09-12.md`. Do not describe this as solving that.

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

## CONFIRMED: the player is holding the overridden blade

Probe v3, run 2026-09-13 15:39 (`ue4ss/ForgeAppearanceProbe/results/`):

```text
[1] player pawn = BP_PlayerCharacter_C ...PersistentLevel.BP_PlayerCharacter_C_2147480040

[1b] holders of the candidate blades
  mesh=M_Sword_Gargoyle_01
    holder=BP_PlayerCharacter_C ...BP_PlayerCharacter_C_2147480040
    isPlayerPawn=true
  mesh=M_Sword_Gargoyle_01
    holder=...same pawn...
    isPlayerPawn=true
```

Two components, both on the player pawn, both the overridden mesh. The stock
blade is not loaded at all.

**The weapon-appearance override is working end to end.** The technique
generalises: `weapon_appearances.csv` maps all 206 weapons, and there are 173
blades to choose from.

Note the probe's own `VERDICT=` line is stale — it predates the holder check in
`[1b]` and does not consider it. The holder match is the authoritative result.

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
