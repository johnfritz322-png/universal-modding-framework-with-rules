# Appearance repoint — loads cleanly, no visible change

First build this project has produced that the game **accepts without crashing**.
The blade still renders as normal, so the lever is wrong, not the packaging.

## What was built

`DT_WeaponAppearances` extracted with retoc, four name indices patched, repacked.
Size-neutral — both target names were already in the table's own name map:

```text
offset 8186  blade     103/583 -> 109/589   L_Sword_Vampiric_01 -> M_Sword_Gargoyle_01
offset 8206  scabbard  104/584 -> 110/590
```

Each byte pattern occurred exactly once, so no other weapon is affected. The row
name `ITM_Weapon_SwordVampiric1a` sits at 8176, ten bytes before the blade field.

Container: **2 chunks, 1 collision** on `0x2b6fc8ead9260336` (the table itself),
decompressed size 51,047 — identical to the original table.

## Result

**No crash. No visible change.** The Vrakhir still shows its own blade.

That is progress: the StaticMesh serialization wall that killed six previous
attempts is not in play on this route, because no mesh is shipped.

## What is known about the visual chain

- `ITM_Weapon_SwordVampiric1a` → `WeaponBlueprint` =
  `BP_Weapon_StraightSword_C` (from `dump_weapon_items.py`).
- `BP_Weapon_StraightSword` has a `WeaponMesh` component but **no mesh asset path
  anywhere in its name map** — so the mesh is assigned at runtime, not baked into
  the blueprint.
- `DT_WeaponAppearances` maps that item to `L_Sword_Vampiric_01`.

So the table *should* be the source. Two explanations remain, and they are
distinguishable:

1. **Our container is not winning.** Load order or packaging. It sorts after the
   base and after `00000000_SkillsNoTimeCost_P`, so this would be surprising.
2. **The appearance is resolved before or independently of our table** — cached in
   `AppearanceSubsystem.ItemAppearanceMap`, baked into the save at equip time, or
   driven by a different asset entirely.

## The diagnostic that settles it

A read-only UE4SS Lua probe that asks the **running game** what
`DT_WeaponAppearances` reports for `ITM_Weapon_SwordVampiric1a`:

- reports **M_Sword_Gargoyle_01** → our mod is live, the visual comes from
  elsewhere, and the search moves to `AppearanceSubsystem` / the equip path.
- reports **L_Sword_Vampiric_01** → our container is not winning, and it is a
  load-order or packaging problem.

`ue4ss/ForgeRegistryProbe/Scripts/main.lua` is a working template — it loads,
binds a key, and writes a status file. Reuse it. Remember: F8 not F10, forward
slashes in paths, and `ExecuteInGameThread` around anything touching UObjects.

Also untried and free: unequip and re-equip the weapon, in case the appearance is
resolved once at equip time.

## Not installed

Removed 2026-09-13 at the user's request. `~mods` holds only their own
`SkillsNoTimeCost` and `~JohnRTX5080Quality_P.pak`.

The built container is kept in this folder as `zzz_VrakhirGargoyle_P.utoc` for
reference. To reinstall, rebuild the trio with retoc from the patched legacy files
— see the patch offsets above — and copy all three into `~mods`.
