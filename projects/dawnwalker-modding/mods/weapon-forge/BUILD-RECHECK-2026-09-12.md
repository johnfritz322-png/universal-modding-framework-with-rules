# Build recheck — 2026-09-12

The Steam game updated after the first disposable-item package was built.

| Field | Current value |
| --- | --- |
| Steam app | `3751260` |
| Steam build | `25232147` |
| `Dawnwalker.exe` SHA-256 | `CB9B7D7BD88A6754C0A9C08318AA64D5013DDFD92D5BADCAE84E1B4EA980DCFC` |
| Base `.utoc` SHA-256 | `0C0CA54F551A7B02CB7900B99F8391F275B752028BB668199312D10DA2AF0846` |

## Rechecks that passed

- `ForgeTestInventory.utoc` still has **zero collisions** against the new base
  container (`778,395` base chunks).
- The current base item `ITM_Weapon_SwordGreatMaster1a` still decodes with the
  existing mapping file: ID `SwordGreatMaster1a`, Great weapon, damage `37–53`,
  Master rarity.  The known item format therefore remains readable.

## What this does not prove

It does not prove the new test item can be registered or granted in the updated
game.  The previously downloaded UE4SS package targets Steam build `25129649`,
not this build, and remains disabled.  Do not install or enable it.

Before any in-game test, find a route specifically verified for Steam build
`25232147`, then use the disposable item and disposable save sequence in
`NEXT-STEPS-HANDOFF-2026-09-10.md`.
