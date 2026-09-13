# Visual Loadout build record — 2026-09-13

## Scope

This is a two-weapon **appearance replacement** mod. It does not add inventory
items or new geometry.

| Existing weapon | Item row | Replacement blade | Replacement scabbard |
| --- | --- | --- | --- |
| The Vrakhir | `ITM_Weapon_SwordVampiric1a` | `L_Sword_Unique_01` | `L_Sword_Unique_01_Scabbard` |
| Imbued Sword of St. Mihai | `ITM_Weapon_SwordDawnwalker5a` | `M_Sword_Ancient_Hero_01` | `M_Sword_Ancient_Hero_01_Scabbard` |

## Build checks passed

1. Fresh `retoc to-legacy` extraction from the current base-container view:
   one table extracted, zero failures, and current `scriptobjects.bin` present.
2. `build_visual_loadout.py` copied that clean extraction and changed only the
   four FName references in each exact, uniquely located row. It rejected any
   unexpected source values.
3. `retoc to-zen --version UE5_5` produced one IoStore trio.
4. `retoc verify` reported `verified`.
5. `verify_container.py` reported exactly one base collision, the expected
   `DT_WeaponAppearances` export chunk `0x2b6fc8ead9260336`, and no other
   package collision.
6. A composite read-back using the base containers plus the new trio extracted
   the table successfully. Both rows had the expected four patched indices.
7. All four target blade/scabbard package paths were independently found in the
   current base container.

## Output fingerprint

The build outputs live outside Git because they contain proprietary game data:
`D:\Dawnwalker-Modding\visual-loadout\zen\`.

| File | SHA-256 |
| --- | --- |
| `zzz_VisualLoadout_P.pak` | `75E7144577253917F6DA7312EF5E585B12FB728226A22B0938323751A6B555CD` |
| `zzz_VisualLoadout_P.ucas` | `63285B41E587D215E6C9A96A0F05F5BEA4A6F9F4AFD7D178706D06052261A2B8` |
| `zzz_VisualLoadout_P.utoc` | `5011D9022364757BE37EF0C959DAF4ED86A7E51F028F62AFED0D19761D18B07B` |

## Install and rollback

Install only these three files, with the game closed:

```text
Content\Paks\~mods\zzz_VisualLoadout_P.pak
Content\Paks\~mods\zzz_VisualLoadout_P.ucas
Content\Paks\~mods\zzz_VisualLoadout_P.utoc
```

To roll back, close the game and remove only those same three files. The prior
single-Vrakhir persistence test proved table appearance overrides are reversible
and do not bind a save to the mod. This new two-row mapping still requires its
own in-game test on the disposable save before it is used on a main save.

## Installation status

The trio was copied to `Content\Paks\~mods` only after all checks above passed.
The installed SHA-256 values matched the output fingerprints exactly. The game
launched and loaded normally with the trio present. No inventory change, weapon
grant, equip action, or save write was performed during that launch.

The currently loaded save did not have either target sword resident/equipped, so
this record does **not** claim an in-game visual confirmation for the new two-row
loadout yet. That must be done on the already-established disposable save with
each matching weapon equipped and drawn.
