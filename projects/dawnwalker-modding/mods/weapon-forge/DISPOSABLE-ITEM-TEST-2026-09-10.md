# Disposable additive-item test — 2026-09-10

## Purpose

This is a **format and container test only** for the eventual five new inventory
weapons.  It proves that a separate, collision-free Dawnwalker item package can be
made from a verified retail item without editing the game installation.

It does **not** prove that the game registers, grants, displays, or equips the
item.  Nothing from this test has been installed in the game, and no save has
been touched.

## Test item

| Field | Value |
| --- | --- |
| Source item | `ITM_Weapon_SwordGreatMaster1a` |
| Test item | `ITM_Weapon_ForgeTestSword0000` |
| Source identifier | `SwordGreatMaster1a` |
| New identifier | `ForgeTestSword0000` |
| Identifier length | 18 bytes in both cases |
| Intended role | Prove discovery of a new item ID, not provide a finished weapon |

The temporary item deliberately keeps the source item's existing retail data and
visual references.  It is not one of the five weapons and is not a custom visual.
Keeping the identifier byte length identical avoids shifting serialized offsets
while the package format is being proven.

## Checks completed

1. `clone_item_template.py` made a loose legacy clone outside the game folder.
   It replaced all 6 identifier occurrences in the `.uasset` and all 2 in the
   `.uexp`, and preserved both file sizes (2046 and 218 bytes).
2. Official `retoc` 0.1.5 packed the clone as an Unreal 5.5 IoStore container.
3. `retoc verify` reported `verified`.
4. `verify_container.py --expect-none` reported **0 collisions** against
   `Dawnwalker-Windows.utoc`.  The container has 2 chunks, both additive.
5. A read-back conversion using the current game AES key and the retail global
   script-object data extracted exactly one asset with no failures:
   `ITM_Weapon_ForgeTestSword0000.uasset` (2046 bytes) and `.uexp` (218 bytes).
   The read-back asset contains 6 new-ID occurrences and zero old-ID occurrences;
   its `.uexp` contains 2 and zero, respectively.

All generated data, the verified `retoc` binary, and the temporary read-back data
are intentionally ignored by Git.  They contain proprietary game-derived data or
third-party binaries.  The reproducible scripts and this record are versioned.

## Remaining gate — do not guess

The game must be shown to **register and grant** this new item ID on a disposable
save without UE4SS.  The old UE4SS path remains disabled because it previously
crashed the game.  No verified native grant mechanism has been found yet.

Current public inventory menus describe adding indexed weapon IDs, but that is
not proof that they can see a newly packed asset.  The locally downloaded
`Dawnwalker-UE4SS-v1.2.0-rc5-build25129649` also fails its own signature scan on
the current game executable (`EngineVersion`, `GUObjectArray`, `GMalloc`, and
`FText` are unresolved), so it is not a safe fallback.  It remains disabled.

Do not install the test container or claim the item is in inventory until that
mechanism is verified.  Once it is, use this test first; only after it appears in
inventory should the five authored weapon assets be built and added.

## Rollback

There is currently nothing to roll back: the test exists only in ignored local
work areas and the game `Content\\Paks\\~mods` folder was not changed.

If this test is later installed, rollback must be only removing its three files
(`.pak`, `.ucas`, `.utoc`) by their exact `ForgeTestInventory` name, after first
closing the game.  Never delete or overwrite another mod or save.
