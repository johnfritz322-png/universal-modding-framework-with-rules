# Riftforged blade over The Vrakhir — built, awaiting install

A custom sword that actually appears in game, by overriding the blade mesh of an
item the player already owns.

## What it is

`zzz_RiftforgedVrakhir_P.pak` (53,745 bytes) publishes the Riftforged Slabblade
V2 mesh at exactly:

```text
/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01/L_Sword_Vampiric_01
```

which `weapon_appearances.csv` shows is the blade of `ITM_Weapon_SwordVampiric1a`
— **The Vrakhir**, one of the player's own weapons. Same package name means the
same chunk id, and `~mods` loads after the base container, so the mod's mesh wins.
That is the mechanism `SkillsNoTimeCost` (112 of 113 chunks) and `DualSenseAtlas`
(4 of 5) already use on this install.

The mesh is the real V2 model — **526 verts, 255 faces, with UVs and normals** —
not the 40-vert blockout the original audit rejected.

## Honest scope

This changes The Vrakhir's **appearance**. Its name, stats and identity stay the
game's. It is not a new inventory item; that still needs the registry work in
`REGISTRY-OVERRIDE-PROGRESS-2026-09-12.md`.

## ANSWERED: a legacy .pak cannot override an IoStore package

Installed and tested in game 2026-09-13. **The blade did not change.**

That settles a question this project had carried as an assumption. The base
game resolves packages through the IoDispatcher by chunk id; a legacy `.pak`
supplies files by path and never gets consulted for a package the IoStore
container already owns. It is why every working asset mod here —
`SkillsNoTimeCost`, `DualSenseAtlas` — ships `.utoc`/`.ucas`/`.pak` as a trio and
not a lone pak.

Recorded as VERIFIED: **an asset override needs a real IoStore container.**

Two UnrealPak invocations that do *not* produce one, so nobody retries them:

```text
UnrealPak out.pak  -create=resp.txt -iostore    -> legacy pak only
UnrealPak out.utoc -create=resp.txt -iostore    -> a pak with a .utoc filename,
                                                   byte-identical to the above
```

The supported route is UAT staging with `-pak -iostore`, which emits real
containers.

## Install

Game closed, then drop the pak in:

```text
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\
```

Equip The Vrakhir and look at the blade.

## Uninstall

Delete `zzz_RiftforgedVrakhir_P.pak` from `~mods`. Nothing else is touched — no
base archive, no save, no other mod.
