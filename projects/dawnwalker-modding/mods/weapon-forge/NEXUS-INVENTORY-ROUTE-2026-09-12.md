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
| Dawnwalker UE4SS Cheat Menu v3.2 | It can browse indexed weapons/clothing and grant one item at a time after each native inventory action completes.  It started successfully here with the current-build UE4SS loader. | It did not list the separately packed `ForgeTestSword0000` item in the first live test. |
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

## Live test result — 2026-09-12

The exact-current UE4SS package, F12 Skill Point Menu v3.2, and the three
`ForgeTestInventory` container files were installed only after a full rollback
copy of the prior loader files was made.  The container collision check passed
immediately before installation.

On a new disposable `Prologue` manual save, the current menu indexed 827 normal
items.  Searching its item chooser for `ForgeTestSword0000` returned **No
matches**.  Searching the cloned retail source's display name returned one
retail `Master Blacksmith's Blade` row, which cannot safely be assumed to be
the new item.  No item was granted.

This is a valid stop condition under the project rules: the custom package is
not presently discovered as a separate inventory definition.  Do not replace a
retail weapon or grant the retail row as a stand-in.

## Next technical step

Determine the game's item-registration/indexing input for new
`ItemBaseDataAsset` packages.  The known custom package is readable and has no
chunk collisions; the unverified missing link is registration, not the native
inventory grant call or the visual mesh.  Continue from the game configuration
and asset-registry path rather than guessing an ID.

## Required safe test, in order

The first six steps have now been performed and step 6 stopped the test.  Do
not continue to a grant until new-item registration is demonstrated.

## Safety conclusion

Do **not** enable the locally downloaded old UE4SS package.  It targets build
`25129649`, previously failed core signature resolution here, and is not a
clean proof for build `25232147`.  The current build package is installed only
for the disposable test, and the main save was not touched.

## Sources consulted

- Dawnwalker UE4SS Cheat Menu v3.2 (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/119
- Dawnwalker UE4SS current loader (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/18
- DwSav - Dawnwalker Save Editor (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/285
- Dawnwalker Transmog Manager (Nexus, accessed 2026-09-12):
  https://www.nexusmods.com/thebloodofdawnwalker/mods/257
