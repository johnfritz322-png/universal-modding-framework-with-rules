# Runtime direct-load probe — 2026-09-12

## Purpose

Test whether the running retail game can resolve the known additive item package
without changing an inventory or save. This calls UE4SS `LoadAsset` for the
exact package path, then checks its exact object path with `StaticFindObject`.

## Preconditions

- Retail build `25232147` (display version 1.0.5 / 258504).
- Exact-build UE4SS loader `Dawnwalker-UE4SS-v1.2.1-rc6-build25232147`.
- `ForgeTestInventory.pak`, `.ucas`, and `.utoc` were in `Content/Paks/~mods`;
  pre-install collision and container checks passed.
- A newly created disposable Prologue manual save was loaded. No old save was
  opened or altered.

## Result

The first run used the package path and recorded:

```text
[ForgeItemLoadProbe] Loading /Game/_Dawnwalker/Inventory/Items/ITM_Weapon_ForgeTestSword0000
[ForgeItemLoadProbe] NOT_FOUND after LoadAsset
```

The three test container files were then renamed to match the working community
mod convention (`00000000_ForgeTestInventory_P.pak`, `.ucas`, `.utoc`). The game
was restarted, the same disposable save was loaded, and the probe tried both the
package path and the complete object path:

```text
[ForgeItemLoadProbe] Loading /Game/_Dawnwalker/Inventory/Items/ITM_Weapon_ForgeTestSword0000
[ForgeItemLoadProbe] NOT_FOUND after LoadAsset
[ForgeItemLoadProbe] Loading /Game/_Dawnwalker/Inventory/Items/ITM_Weapon_ForgeTestSword0000.ITM_Weapon_ForgeTestSword0000
[ForgeItemLoadProbe] NOT_FOUND after LoadAsset
```

No item was granted, no retail item was selected, and no save was written after
this probe.

## Meaning

The issue is not only the menu's initial object scan or the container filename.
The running game cannot resolve the new package by either exact `/Game` loading
form after a direct load request. Do not treat this packed clone as a usable
inventory item.

The remaining gate is a verified way to register an additive item package in
the cooked game's asset-registry / primary-asset discovery path. The native
inventory grant is usable only after that gate is demonstrated.

## Rollback

After the game is closed, remove the locally installed
`ue4ss/Mods/ForgeItemLoadProbe` folder and its one `ForgeItemLoadProbe : 1`
line from `ue4ss/Mods/mods.txt`. The probe does not touch the game executable,
package archives, or saves.
