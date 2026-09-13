# Dawnwalker Weapon Forge — separate inventory items

This note covers the user's explicit requirement: the five custom swords must be
**new items in the player's inventory**, not visual replacements of current game
weapons.

Status: **DESIGNED / RESEARCH IN PROGRESS. NOT IMPLEMENTED. NOT TESTED.**

The mesh-override technique in `ATTACHMENT-FINDINGS-2026-09-09.md` is a different
architecture. It can replace a base mesh globally, but cannot satisfy the
separate-inventory-item requirement by itself.

## Verified on local build 258042

The installed executable reports:

```text
dw1-pc-258042-shipping-patch2-all-CL-258042
SHA-256: 02D424EDDBD364ED25F3777A7A2FA1B0DFE84690AE18F84EC9EB2997B0828C33
```

Using the current AES key and `Dawnwalker.usmap`, a read-only CUE4Parse/FModel
inspection successfully mounted the base archive and parsed the following:

| Evidence | Result |
| --- | --- |
| `/Game/_Dawnwalker/Player/BP_PlayerCharacter` | contains `DogwoodInventory.InventoryComponent` |
| Native mapping names | include `AddItem` and `FlowNode_AddItemsToInventory` |
| `/Game/_Dawnwalker/Inventory/Items/ITM_Weapon_SwordGreatMaster1a` | parses as `ItemWeaponDataAsset` |
| `/Game/_Dawnwalker/Inventory/Items/DT_WeaponAppearances` | parses as the item-to-blade/scabbard map |
| `Dawnwalker/Config/DefaultGame.ini` | extracted directly from the mounted archive |

The `ItemWeaponDataAsset` example carries an item id, name/description keys,
rarity, weight, buy/sell value, damage range, custom effects, combo, icon, and a
weapon actor-class reference. This establishes the required shape of a distinct
weapon item; it is not proof that we can author one yet.

## Registration rule

The extracted `DefaultGame.ini` includes this primary-asset scan:

```text
PrimaryAssetType: DW_ItemAsset
Base class: /Script/DogwoodInventory.ItemBaseDataAsset
Directory: /Game/_Dawnwalker/Inventory/Items
```

This is the core constraint. A new item cannot simply be a static mesh in a plugin.
The game must discover a compatible item data asset, and the item must have a
corresponding appearance-table entry before it can behave as a normal inventory
weapon.

## The five requirements before a build exists

1. **Registration:** prove a non-destructive way to extend the `DW_ItemAsset`
   scan to a mod-owned item directory.
2. **Item assets:** author five valid `ItemWeaponDataAsset` objects compatible with
   the retail `DogwoodInventory` module. The standalone UE editor project does not
   include that private authoring module, so this is currently **UNSOLVED**.
3. **Appearance data:** add five item-id rows to `DT_WeaponAppearances`, each
   pointing at a blade and scabbard asset. The table was successfully read; safely
   writing a new cooked row has not been proven.
4. **Grant:** invoke the verified inventory `AddItem`/flow-node route with the new
   assets. The exact callable signature and loader mechanism remain **UNVERIFIED**.
5. **Validation:** package only the intended files, use a disposable save, confirm
   all five items persist, equip correctly, animate, sheath, display proper icons,
   and uninstall without corrupting the test save.

## Important non-solutions

- Replacing an existing mesh changes that mesh for every user of it. It is not a
  new inventory item.
- The retired `DawnwalkerWeaponForge-VerifiedBuild` is not an install candidate;
  it contains accidental stock Engine payloads and duplicate content paths.
- Do not use UE4SS for this task. A prior UE4SS attempt crashed during world
  teardown; no current runtime-hook path is verified.
- Do not patch game binaries, overwrite the base containers, or use a guessed item
  id, data-table row, inventory API, socket, or package path.

## Next research task

The read-side layout is now resolved—see
[`ITEM-WEAPON-DECODE-2026-09-10.md`](ITEM-WEAPON-DECODE-2026-09-10.md), which
validates 191 present retail weapon packages. The remaining task is to prove a
way to **author and package** a new cooked `ItemWeaponDataAsset` for the retail
`DogwoodInventory` module, then prove that the game's asset scan discovers it
and that its item id can be granted without the previously crash-prone UE4SS
route. Current public Dawnwalker cooked tools document only asset/data-table
replacement, not a tested additive inventory-item workflow. Until that is
solved, describe the feature only as a design goal, not a working mod.
