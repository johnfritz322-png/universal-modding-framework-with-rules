# John Loadout Optimizer

UE4SS Lua prototype for The Blood of Dawnwalker.

## Goal

Optimize the current equipment loadout from inside the game:

- Numpad 1: optimize for attack.
- Numpad 2: optimize for defense.

## Current State

This is a first-pass runtime mod. It is intentionally defensive because DW's save
and cooked asset property layout is not fully mapped yet.

The game exposes useful inventory functions:

- `InventoryComponent.GetCurrentItems`
- `InventoryComponent.GetEquippedItem`
- `InventoryComponent.GetValidEquipmentSlotsForItem`
- `InventoryComponent.TryEquipItem`
- `InventoryComponent.TryEquipItemInSlot`
- `InventoryComponent.SetActiveLoadout`
- `ItemWeaponDataAsset.GetDamagePerSecond`
- `ItemWeaponDataAsset.GetWeaponDamage`
- `ItemBaseDataAsset.GetItemProperty`

The mod starts with those calls and logs any missing pieces to UE4SS logs. Once we
see the live shapes of item handles and equipment slots, the scorer can be made
stricter.

## Install

This requires UE4SS to be installed for DW first. DW does not currently have UE4SS
in `Dawnwalker\Binaries\Win64`, so this mod will not load until that dependency is
present.

After UE4SS is installed, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

Expected installed structure:

```text
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Binaries\Win64\ue4ss\Mods\JohnLoadoutOptimizer\
├─ enabled.txt
└─ Scripts\
   └─ main.lua
```

## Notes

This is a prototype. If Numpad 1 or 2 logs that it found the inventory but could
not score/equip items, the next step is a short in-game probe run with UE4SS object
inspection enabled.

