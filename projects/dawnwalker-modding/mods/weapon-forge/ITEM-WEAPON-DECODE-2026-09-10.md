# ItemWeaponDataAsset decode — resolved

This corrects the open issue in `FTEXT-HANDOFF-2026-09-09.md`.

## Cause

The `.usmap` inheritance lookup was reversed.  Unversioned schema indices start
with the **most-derived class**, then continue into each parent after that
class's declared `PropertyCount`.  This is independently corroborated by
CUE4Parse's `Struct.TryGetValue`: it tries its current type, then recursively
looks up the parent with `index - PropertyCount`.

`ItemWeaponDataAsset` therefore starts like this:

| Header indices | Actual fields |
| --- | --- |
| 0–6 | `ItemWeaponDataAsset` fields (`WeaponType`, blueprint, damage, effects) |
| 7–31 | `ItemBaseDataAsset` fields |
| 32 | `DataAsset.NativeClass` |

The old base-first lookup mislabeled child data as base data.  The apparently
unexplained 53 bytes were valid weapon fields, including damage and custom
effect parameters, followed by the real `ItemId`.

## Verification

`dump_weapon_items.py` reads item packages directly from the encrypted base
IoStore archive using the verified AES key and the signed UE Oodle runtime.  It
successfully decoded **191 present weapon packages** from the 206-item
appearance-map list.  Every decoded package consumed exactly its declared
export size minus the same four-byte zero trailer; no failures occurred.

The other 15 entries in `weapon_appearances.csv` are not packages at the
expected `/Game/_Dawnwalker/Inventory/Items/<Item>.uasset` path, so they are
reported as missing rather than invented or treated as failures.

Spot checks:

| Package | Weapon blueprint | Damage |
| --- | --- | --- |
| `ITM_Weapon_SwordGreatMaster1a` | `BP_Weapon_GreatSword_C` | 37–53 |
| `ITM_Weapon_AxeLongMaster1a` | `BP_Weapon_Axe_C` | 32–46 |
| `ITM_Weapon_SwordVampiric1a` | decoded from its own package | 49–70 |

## What this unlocks—and what it does not

We now have verified read access to the exact serialized shape of a retail
weapon data asset: identifier, localized text keys, weapon actor class, damage,
effects, rarity, price, icon, and other present fields.  This removes the item
data *reading* blocker.

It does **not** prove we can safely author a new cooked
`ItemWeaponDataAsset` for the game's private `DogwoodInventory` module, extend
the retail asset scan, add localization and appearance-table entries, or grant
the item.  Those remain separate gates before a new inventory item can be
built, installed, or tested.  Nothing was installed and no save or game file
was changed.
