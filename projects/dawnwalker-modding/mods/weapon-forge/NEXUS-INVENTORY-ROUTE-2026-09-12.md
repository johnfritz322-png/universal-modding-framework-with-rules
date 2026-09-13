# Nexus inventory-route research — 2026-09-12

## The answer

The current community route for placing weapons into inventory is a runtime menu
that calls the game's **native inventory action** on a selected, **already
indexed** item.  It does not edit game binaries and it does not replace a weapon
to grant it.  This is the closest verified grant mechanism for the Forge's goal
of separate items.

## What the relevant mods actually do

| Mod type | What it proves | What it does not prove |
| --- | --- | --- |
| Dawnwalker UE4SS Cheat Menu v3.2 | It can browse indexed weapons/clothing and grant one item at a time after each native inventory action completes. | It was tested on Steam build `25129649`, not the installed `25232147`, and does not claim it can discover a newly packed ID. |
| DwSav save editor | It can add/remove **supported** inventory stacks and writes a separate save copy. | It does not claim to register a custom game asset or a new item ID. |
| Dawnwalker Transmog Manager | Cooked `.pak/.ucas/.utoc` appearance changes work without UE4SS. | It retains an existing item's identity and stats; it is explicitly a transmog/replacement route, not a new inventory item. |

## What this changes

The Forge's `ForgeTestSword0000` container is still the right first test.  Its
new item package is zero-collision and readable after packing.  If a current,
clean runtime menu indexes that ID, its native grant action can give the test
item without replacing any retail item.

That is a testable route, **not yet a completed route**.  No public Dawnwalker
mod found in this review documents a wholly new custom weapon with a new mesh,
new inventory definition, and successful grant.  Do not claim that part until
we observe it on a disposable save.

## Required safe test, in order

1. Obtain a loader/menu explicitly compatible with installed Steam build
   `25232147`, or verify it directly against this executable.
2. Record its files and hashes; disable all nonessential helper/gameplay mods.
3. Re-run `verify_container.py ForgeTestInventory.utoc --expect-none`.
4. Copy only the three `ForgeTestInventory` files into `Content\\Paks\\~mods`.
5. Create a new disposable save, then open the menu and search for exactly
   `ForgeTestSword0000`.
6. If the ID is absent, stop: registration/indexing is the blocker.  Do not
   guess an ID or grant a substitute.
7. If present, grant one item only; verify inventory, equip, save/reload, then
   exit and remove the three exact test files with the game closed.

## Safety conclusion

Do **not** enable the locally downloaded old UE4SS package.  It targets build
`25129649`, previously failed core signature resolution here, and is not a
clean proof for build `25232147`.  Do not install the test container or touch
the main save until step 1 is satisfied.

## Sources consulted

- Dawnwalker UE4SS Cheat Menu v3.2 (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/119
- DwSav - Dawnwalker Save Editor (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/285
- Dawnwalker Transmog Manager (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/257
