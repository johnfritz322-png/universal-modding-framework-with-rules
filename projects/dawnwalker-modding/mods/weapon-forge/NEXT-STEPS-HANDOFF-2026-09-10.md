# Dawnwalker Weapon Forge — next-steps handoff

## Start here

The user requires **five separate new sword items in inventory**.  Replacing a
retail sword mesh is not acceptable.  Keep spoilers minimal and do not turn the
previous UE4SS installation back on.

The repository branch is `claude/dawnwalker-weaponforge-audit`.

## What is safely finished

- The actual Dawnwalker weapon-item package format is decoded and documented in
  `ITEM-WEAPON-DECODE-2026-09-10.md`.
- `clone_item_template.py` creates a same-length new-ID clone from a verified
  retail item without shifting serialized bytes.
- A disposable clone with the new ID `ForgeTestSword0000` was packed using
  official `retoc` 0.1.5.
- The resulting `ForgeTestInventory` container has **zero collisions** with the
  base game, passes `retoc verify`, and converts back to exactly one valid,
  readable item package.
- No game container, user mod, or save was changed.  UE4SS remains disabled.

See `DISPOSABLE-ITEM-TEST-2026-09-10.md` for the exact evidence and rollback.

## Current blocker

Packaging a separate ID works.  The remaining unproven operation is getting the
running game to discover and grant that ID on a disposable save.

The local `Dawnwalker-UE4SS-v1.2.0-rc5-build25129649` download is unsuitable:
its own log shows signature-resolution failure on the current executable
(`EngineVersion`, `GUObjectArray`, `GMalloc`, and `FText`).  Do not enable it.

Public inventory menus report that they can grant indexed items, but they have
not proved that they see a newly packed asset.  Do not treat that as proof.

## Exact safe next sequence

1. Obtain and verify a loader or save-editor route that is explicitly compatible
   with the installed game build and can enumerate the new test ID.  Preserve the
   disabled loader and make a manifest of every file the new route adds.
2. Use a **new disposable save**, never the user’s main save.
3. Copy only `ForgeTestInventory.pak`, `.ucas`, and `.utoc` into
   `Dawnwalker\\Content\\Paks\\~mods`, after re-running
   `verify_container.py --expect-none` and recording the three hashes.
4. Start the game, check whether `ForgeTestSword0000` is indexed, grant exactly
   one, and verify inventory, equip, save/reload, and clean uninstall.
5. If any step fails, remove only those three exact test files with the game
   closed.  Do not modify user mods, base containers, binaries, or saves.
6. Only after that test succeeds, create the five finished weapon assets,
   appearance rows, names/icons, and separate IDs.  Re-run all package and
   disposable-save checks per item.

## Important paths

| Purpose | Path |
| --- | --- |
| Shared repo | `C:\\Users\\johnf\\Documents\\BG3Mods\\universal-modding-framework-with-rules` |
| Game Paks | `D:\\steam\\steamapps\\common\\The Blood of Dawnwalker\\Dawnwalker\\Content\\Paks` |
| User-mod folder | `...\\Content\\Paks\\~mods` |
| Game executable folder | `...\\Dawnwalker\\Binaries\\Win64` |
| Disabled proxy | `...\\Win64\\dwmapi.dll.ue4ss-disabled` |
| Unreal Engine | `D:\\UE55\\UE_5.5` |
| Current mapping file | `C:\\Users\\johnf\\Downloads\\Dawnwalker.usmap` |

## Useful tools in this folder

- `clone_item_template.py` — safe same-length new-ID test clone.
- `verify_container.py` — confirms a container makes no base-game replacements.
- `dump_weapon_items.py` — reads known retail weapon item fields.
- `iostore_read.py`, `unversioned.py`, `usmap.py` — archive and property readers.

All third-party binaries and game-derived temporary assets stay ignored under
`.local`; only scripts and findings are committed.
