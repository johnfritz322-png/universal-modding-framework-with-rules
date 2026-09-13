# Giant greatsword visibility test — build record (2026-09-13)

## Result

A separate, one-weapon appearance-test container was built for **The Vrakhir**
(`ITM_Weapon_SwordVampiric1a`). It replaces only its visual references with the
retail-game greatsword `L_Sword_NPC_50` and matching
`L_Sword_NPC_50_Scabbard`.

This is a deliberately conspicuous, **Cloud-size test**, not an exact custom
Cloud Buster Sword model. It uses only existing game geometry because custom
StaticMesh cooking is still not proven safe for this game version.

## Checks passed

1. The builder read the clean current table and found the Vrakhir row exactly
   once at byte offset `8176`.
2. It confirmed the original four indices were `(103, 583, 104, 584)` before
   changing them.
3. It changed only those four links to `(99, 529, 100, 580)` and recorded a
   manifest. No other table rows were changed.
4. `retoc to-zen --version UE5_5` completed and `retoc verify` returned
   `verified`.
5. The container has two chunks and exactly one expected base-game collision:
   `0x2b6fc8ead9260336`, the `DT_WeaponAppearances` export. There are no other
   collisions.
6. A composite read-back using the base containers plus this test container
   re-extracted the table. The Vrakhir row decoded to exactly
   `(99, 529, 100, 580)`.

## Output files

The proprietary game-data outputs are stored outside Git at:
`D:\Dawnwalker-Modding\cloud-size-test\zen\`.

| File | SHA-256 |
| --- | --- |
| `zzz_CloudSizeTest_P.pak` | `75E7144577253917F6DA7312EF5E585B12FB728226A22B0938323751A6B555CD` |
| `zzz_CloudSizeTest_P.ucas` | `21D960CC19015C569A6B362A9F62877733DECC751FB8838445BC2BD44171BF7F` |
| `zzz_CloudSizeTest_P.utoc` | `33555820A1DFAEE0EB5FDA548982F94E2DA7BC99938177C2AE5B6DA815AFD240` |

## Installation status

**Not installed.** The game was running while this was built, so nothing under
`Content\Paks\~mods` was touched. The existing `zzz_VisualLoadout_P` trio is
still installed and must not be installed alongside this test: both override
the same appearance table.

## Safe test and rollback

With the game closed, park the existing `zzz_VisualLoadout_P` trio in a backup
folder, then copy the three `zzz_CloudSizeTest_P` files into
`Content\Paks\~mods`. Start the game, equip and draw **The Vrakhir**, and the
very large retail greatsword should appear.

To roll back, close the game, remove only the three `zzz_CloudSizeTest_P` files,
and restore the parked `zzz_VisualLoadout_P` trio. This is a visual table
override only; it does not alter saves, weapon stats, inventory, base archives,
or executables.

## What still needs an in-game test

The package and its exact data links are verified, but the user has not yet
visually confirmed this particular `L_Sword_NPC_50` mapping in the game. Do not
represent the look as tested until that equip-and-draw check is complete.
