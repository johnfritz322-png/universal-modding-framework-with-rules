# Loader compatibility check — 2026-09-12

## Current game

- Steam build: `25232147` (Hotfix 1.0.5)
- Executable SHA-256:
  `CB9B7D7BD88A6754C0A9C08318AA64D5013DDFD92D5BADCAE84E1B4EA980DCFC`

## Result

An exact-current loader was published and tested on 2026-09-12:

- Nexus file: `Dawnwalker-UE4SS-v1.2.1-rc6-build25232147` (mod 18, file v1.3);
- its README targets Steam build `25232147` and the executable hash above;
- downloaded ZIP SHA-256:
  `772C1C16EE2FBFA9F84AB35F469D9276DC2523057788E5F05AFDFF7802CF0365`;
- its bundled `SHA256SUMS.txt` manifest passed locally; and
- it started the installed game and loaded the F12 Skill Point Menu v3.2 on a
  disposable `Prologue` save without a crash.

This proves the current loader starts.  It does **not** prove that a new cooked
item package is registered as a distinct inventory item.

The locally available `Dawnwalker-UE4SS-v1.2.0-rc5-build25129649` is ruled out:

- it targets Steam build `25129649`, not `25232147`;
- its local log previously failed to resolve core signatures; and
- it enables several default runtime mods, making a clean loader-only test
  impossible without a separately verified configuration.

The older local `v1.2.0-rc5-build25129649` package remains ruled out.  It was
not used for this test.

## Safe resume condition

The loader conditions are now met.  The remaining item condition failed in the
first live check: the menu did not list `ForgeTestSword0000`.  See
`DISPOSABLE-ITEM-TEST-2026-09-12.md` for the exact result and next step.

Do not grant a similarly named retail sword as a substitute.  The test package
must first be made indexable as its own item.

## Rollback

Before installing the current loader, the previous `dwmapi.dll` and complete
`ue4ss` folder were copied to:

`D:\\steam\\steamapps\\common\\The Blood of Dawnwalker\\Dawnwalker\\Binaries\\Win64\\DawnwalkerWeaponForgeRollback-20260912-2151`

No user save was overwritten.  The disposable save is a new `Prologue` manual
slot created on 2026-09-12.
