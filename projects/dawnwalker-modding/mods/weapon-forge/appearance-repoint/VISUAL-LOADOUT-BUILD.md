# Visual Loadout build — two existing weapons, two existing-game visuals

This build is deliberately limited to the visual-replacement route that is
already proven reversible and save-safe.  It does **not** create new weapons in
inventory and it does not ship custom geometry.

| Existing weapon | Row | New visual source |
| --- | --- | --- |
| The Vrakhir | `ITM_Weapon_SwordVampiric1a` | `L_Sword_Unique_01` |
| Imbued Sword of St. Mihai | `ITM_Weapon_SwordDawnwalker5a` | `M_Sword_Ancient_Hero_01` |

Both replacements have matching existing scabbards and both source and target
FNames are present in the retail table name map.  The build script refuses to
run if the base table, row, or expected original values do not match exactly.

## Safety

The script copies a clean `retoc to-legacy` extraction into a new folder before
patching it.  It does not alter the source extraction, the game, a save, the
executable, or an existing mod.  The only eventual installation is one three-file
container in `Content/Paks/~mods`, after a successful container check.

The finished visual loadout must be tested on the existing disposable save with
both weapons drawn separately before it is used on a normal save.
