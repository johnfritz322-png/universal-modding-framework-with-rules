# AssetRegistry override — progress, and an alternative worth considering first

**The override is NOT built.** This records how far it got, what is verified, and
the two routes forward. Nothing was installed; no game file or save was modified.

## Why this is the task

Confirmed in `REGISTRATION-LEAD-2026-09-12.md`: every item the game lists is in
the baked `AssetRegistry.bin`, and the mod-added `ForgeTestSword0000` is not.
Discovery reads the registry, not the filesystem, so a new item is invisible
until the registry names it.

## Verified so far

`assetregistry.py` parses the header and name table of the live registry
(build 25232147, 5,426,463 bytes):

| Field | Value |
| --- | --- |
| Version GUID | `e79e7f713a49b0e93291b3880781381b` |
| Version | 17 |
| `bFilterEditorOnlyData` | 1 |
| Names | **40,908** |
| Name string bytes | **2,090,524 — consumed exactly** |
| Body offset | 2,499,644 |
| Body magic | `0x12345679` (fixed tag store) |
| Body size | 2,926,819 bytes — **not parsed** |

Items appear as three separate names, which is the pattern a new item must match:

```
[11712] /Game/_Dawnwalker/Inventory/Items/ITM_Weapon_SwordVampiric1a   package path
[11713] ITM_Weapon_SwordVampiric1a                                     asset name
[33813] SwordVampiric1a                                                ItemId tag value
```

## What remains — and why it stopped here

The body is `FixedTagPrivate::FStore` followed by the asset-data array and the
dependency graph. Writing a **correct** serializer for all three is a substantial
job, and correctness cannot be eyeballed: a malformed registry does not fail
quietly, it is likely to break asset discovery **globally**. Shipping one that has
not been round-trip verified would be worse than shipping nothing.

The next concrete milestone is a **byte-exact round trip**: parse the registry and
re-serialize it to an identical 5,426,463 bytes. Until that passes, no modified
registry should go near the game. That is the same bar every other tool here was
held to, and it is what caught two silent misparses earlier.

After a clean round trip, the edit itself is small: append three names, clone one
asset entry with the new name indices, update counts.

## A cheaper route that may make this unnecessary

**Repurpose an existing item rather than registering a new one.**

Overriding an item's *package* is a chunk-ID collision, which is already proven to
work on this install (`SkillsNoTimeCost` collides on 112 of 113 chunks). Pick an
obscure or unused retail item, override its `ITM_Weapon_*` package with custom
stats, name and mesh reference, and it appears in inventory with the custom sword
— because the registry already lists it, so discovery is satisfied.

Trade-offs, honestly:

- It occupies an existing item's identity rather than adding a slot. Whether that
  counts as "a new inventory item" is the user's call, not ours.
- It needs no registry work at all, so it survives patches far better — only the
  item package must be rebuilt, not a 5.4 MB registry.
- Risk is bounded and reversible: three files in `~mods`, removable.

A tried-and-failed shortcut, recorded so nobody repeats it: several items named in
`DT_WeaponAppearances` (`ITM_Weapon_AxeTest`, `...DemoOnly`, etc.) have **no package
in the archive** — but they are **also absent from the registry**, so there is no
pre-existing registry entry to fill. Registry and archive are consistent.

## Tools

- `assetregistry.py` — header and name table parser, name search
- `pak_extract.py` — pulls `AssetRegistry.bin` out of the encrypted pak
