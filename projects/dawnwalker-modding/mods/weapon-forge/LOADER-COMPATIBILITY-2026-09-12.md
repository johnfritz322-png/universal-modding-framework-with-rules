# Loader compatibility check — 2026-09-12

## Current game

- Steam build: `25232147` (Hotfix 1.0.5)
- Executable SHA-256:
  `CB9B7D7BD88A6754C0A9C08318AA64D5013DDFD92D5BADCAE84E1B4EA980DCFC`

## Result

No loader was found that is **explicitly verified for this build** and can be
shown to enumerate a newly packed item asset.

The locally available `Dawnwalker-UE4SS-v1.2.0-rc5-build25129649` is ruled out:

- it targets Steam build `25129649`, not `25232147`;
- its local log previously failed to resolve core signatures; and
- it enables several default runtime mods, making a clean loader-only test
  impossible without a separately verified configuration.

The web search found community loader pages and item menus, but their release
claims are not proof of compatibility with the current executable or of support
for a new custom item ID.  Do not install them for this project until their
current-build support can be independently verified.

## Safe resume condition

Resume the in-game item test only when a loader or save tool can meet all four:

1. states support for Steam build `25232147` (or is verified directly against
   this executable);
2. has a published file hash or another trustworthy integrity check;
3. can start alone with no default gameplay mods enabled; and
4. can enumerate `ForgeTestSword0000` before granting it on a disposable save.

Until then, do not copy `ForgeTestInventory` into `Content\\Paks\\~mods`, do not
enable `dwmapi.dll.ue4ss-disabled`, and do not touch saves.
