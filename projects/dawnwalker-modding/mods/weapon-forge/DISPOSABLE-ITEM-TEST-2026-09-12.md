# Disposable custom-item test — 2026-09-12

## Scope

Test whether the separately packed `ForgeTestSword0000` appears in the game's
runtime item index.  This test did not attempt to add an item unless the exact
test ID was present.

## Setup verified before launch

- Game: Steam build `25232147`, version 1.0.5 / 258504.
- Loader: `Dawnwalker-UE4SS-v1.2.1-rc6-build25232147` (Nexus mod 18 v1.3).
- Loader ZIP SHA-256:
  `772C1C16EE2FBFA9F84AB35F469D9276DC2523057788E5F05AFDFF7802CF0365`.
- ZIP's bundled SHA-256 manifest: passed.
- Menu: Dawnwalker UE4SS Cheat Menu / F12 Skill Point Menu v3.2.
- Test container collision check: passed with zero base-container collisions.
- Rollback copy: `D:\\steam\\steamapps\\common\\The Blood of Dawnwalker\\Dawnwalker\\Binaries\\Win64\\DawnwalkerWeaponForgeRollback-20260912-2151`.

## Observed result

1. The game reached a new, separate `Prologue` manual save.
2. UE4SS started and loaded the F12 menu.  No crash occurred during this test.
3. The menu reported `827 standard items indexed`.
4. Filtering for the exact internal test ID `ForgeTestSword0000` returned
   `No matches`.
5. Filtering for the original retail display name showed one `Master
   Blacksmith's Blade` row.  The menu does not expose enough identity data to
   prove that row is the custom package, so it was not granted.

## Conclusion

**FAILED AS EXPECTED-SAFE:** current runtime indexing does not expose the
separate custom package to the native grant menu.  The test did not add a
retail item, did not change an equipped weapon, and did not write to an
existing save.

## Next required proof

Find and reproduce the game's item-registration path for a newly added
`ItemBaseDataAsset`, then repeat this exact test.  Only after the exact custom
ID is visible may one item be granted and verified through inventory, equip,
save, and reload.
