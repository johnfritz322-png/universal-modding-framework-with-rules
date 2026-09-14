# Dawnwalker Weapon Forge — end-of-session handoff

## Current game files

The current installed appearance mod is the previously proven **Vrakhir →
Gargoyle blade** replacement:

```text
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods\
  zzz_VrakhirGargoyle_P.pak
  zzz_VrakhirGargoyle_P.ucas
  zzz_VrakhirGargoyle_P.utoc
```

It is a visual replacement only. It does not add an inventory item, change
stats, edit saves, change the executable, or modify base game archives.

## What was proved earlier

`M_Sword_Gargoyle_01` and its scabbard were found as live components on the
player pawn while the Vrakhir replacement was installed. That is the known-good
appearance route.

## What happened this session

1. A test mapped the Vrakhir to the retail `L_Sword_NPC_50` greatsword to make
   the difference obvious.
2. The package passed structural verification and a full table read-back.
3. In the game, that blade was invisible when drawn. Therefore it is not a
   usable player-weapon visual for this route, despite being a valid retail
   table reference. Do not reinstall it as a final choice.
4. The test files were moved, not deleted, to:

```text
D:\Dawnwalker-Modding\cloud-size-test\installed-backup-2026-09-13\
```

5. The prior two-sword VisualLoadout build is also preserved at:

```text
D:\Dawnwalker-Modding\visual-loadout\installed-backup-2026-09-13\
```

## F8 verification probe

The installed `ForgeAppearanceProbe` was corrected to look for the actual
current Vrakhir target: `M_Sword_Gargoyle_01` rather than its stale old target.
UE4SS reads its Lua only when the game starts, so this needs one full game
restart before F8 can report correctly.

After restarting, draw the Vrakhir, press F8, then read:

```text
D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Binaries\Win64\ue4ss\Mods\ForgeAppearanceProbe\status.txt
```

The desired line is `OVERRIDE_ON_PLAYER`. If it reports
`STOCK_ON_PLAYER`, stop and investigate the active appearance package rather
than guessing at another mesh.

## Important limits

- The working route replaces the visual of an existing inventory weapon. It
  does **not** create a new inventory item.
- Custom weapon geometry, including an exact Cloud Buster Sword, is still
  blocked: stock UE 5.5.4-cooked StaticMesh assets crash this game due a
  serialization mismatch. Do not try to install custom meshes until a matching
  game-compatible cooker or serializer is proven.
- The huge `L_Sword_NPC_50` test is not suitable for use because it rendered
  invisible on the Vrakhir.

## Best next step

Restart the game once and use the corrected F8 probe with the Vrakhir drawn.
If `OVERRIDE_ON_PLAYER` is confirmed but the Gargoyle design is not distinct
enough, pick another **previously player-visible** blade and test it one at a
time. Preserve the same one-table, one-weapon, reversible package process.
