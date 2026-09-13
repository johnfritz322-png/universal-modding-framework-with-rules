# Giant greatsword visibility test

## Purpose

This is a temporary, easy-to-see check for the working weapon-appearance
route. It maps **The Vrakhir** (`ITM_Weapon_SwordVampiric1a`) to the retail
game's `L_Sword_NPC_50` greatsword and its matching scabbard.

It is intentionally **not** Cloud's exact Buster Sword. Creating and cooking
new mesh geometry is still not reliable for this game version. This uses an
existing verified greatsword asset so the test is safe and reversible.

## What it changes

Only four FName references in one `DT_WeaponAppearances` row:

| Existing item | New visual | Matching scabbard |
| --- | --- | --- |
| The Vrakhir | `L_Sword_NPC_50` | `L_Sword_NPC_50_Scabbard` |

No save, executable, base archive, item stats, inventory, or quest data is
changed.

## Safety checks required before installation

1. Extract the table fresh from the current base containers.
2. Run `build_cloud_size_test.py`; it refuses unexpected source bytes.
3. Pack with `retoc to-zen --version UE5_5`.
4. Run `retoc verify`.
5. Confirm the package contains only the one expected table collision.
6. Read the packed table back and confirm the Vrakhir row uses `(99, 529, 100, 580)`.

## Installation and rollback

Install only one appearance-table replacement at a time. To test this build,
the game must be closed and the existing `zzz_VisualLoadout_P` trio must be
parked in a backup folder before the `zzz_CloudSizeTest_P` trio is copied into
`Content\Paks\~mods`.

Rollback is restoring the parked `zzz_VisualLoadout_P` trio, or removing the
three test files. Existing saves remain unchanged.
