# Visual loadout set — plan and verified inputs

The first two-row build is now created and has passed container and read-back
checks. See `VISUAL-LOADOUT-BUILD-2026-09-13.md`. **Existing game meshes only**
— the custom-StaticMesh route is still blocked.

## Weapons identified

Display names live in a string table, not the item asset, so items were matched
by **damage range** from `dump_weapon_items.py` against the scraped catalogue.

| Weapon | Item row | Damage | Current blade |
| --- | --- | --- | --- |
| **The Vrakhir** | `ITM_Weapon_SwordVampiric1a` | 49–70 | `L_Sword_Vampiric_01` |
| **Imbued Sword of St. Mihai** | `ITM_Weapon_SwordDawnwalker5a` | 54–78 | `S_Sword_Dawnwalker_01` |
| third slot | _TBD_ | | |

Both confirmed unique on damage. The Imbued Sword being a `Dawnwalker5a` row is
worth noting — the St. Mihai progression (Broken → Partly Restored → Restored →
Mostly Restored → Imbued) does not use `St_Mihai` ids.

## Per-row checks before shipping — every row, no assumptions

1. Exact item row exists in `DT_WeaponAppearances`.
2. Target blade **and** scabbard packages both exist
   (`verify_asset_path.py`, expect FOUND for both).
3. Both target names already in the table's name map, so the patch stays
   **size-neutral**.
4. Each byte pattern occurs **exactly once** in the `.uexp` (no collateral rows).
5. Container shows **only** the `DT_WeaponAppearances` collision
   (`0x2b6fc8ead9260336`), 2 chunks.
6. In game: probe reports `OVERRIDE_ON_PLAYER` with the weapon **drawn**.
7. Restart and re-confirm.

## Choosing targets

Pick **silhouette-distinct** blades. `M_Sword_Gargoyle_01` proved the mechanism
but looks like another dark sword, so the user reported "looks normal" while it
was in fact working. Candidates with obviously different shapes:

- `M_Sword_Ancient_Hero_01`, `M_Sword_Matron_01`, `M_Sword_Skender_01`
- `SM_Axe_01`, `SM_Hammer_01`, `SM_Pickaxe_01` — improvised weapons, unmistakable
- `L_Sword_Unique_01`, `S_Sword_Unique_03`

Every blade needs a matching `_Scabbard` — check first; the improvised weapons
may not have one.

## Rollback

One documented file list for the whole set:

```text
Content\Paks\~mods\zzz_VisualLoadout_P.pak
Content\Paks\~mods\zzz_VisualLoadout_P.ucas
Content\Paks\~mods\zzz_VisualLoadout_P.utoc
```

Proven reversible and save-safe — see `PERSISTENCE-TEST.md`.
