# Why a new item never registers — the asset registry lead

Picks up Codex's blocker: a cooked item package loads but the game never lists it
as an item. This is the most promising explanation found so far, plus the exact
test that would confirm or kill it.

## The lead

**Cooked UE5 builds do not scan the filesystem for primary assets.** `UAssetManager`
resolves `PrimaryAssetType` scans against an **asset registry baked at cook time**.
A package added by a mod container is not in that registry, so it is never
discovered — no matter how correctly it is packaged, named, or mounted.

That matches Codex's symptom exactly: the package loads without error, and the
item simply is not in the list.

## What is verified

`Dawnwalker/AssetRegistry.bin` exists, inside the **encrypted legacy `.pak`** —
not the IoStore container, which is why earlier searches of the `.utoc` index
missed it (and why my "that file does not exist" flag about `DefaultGame.ini` was
wrong; it is in the same place).

Measured from the decrypted pak index:

| Property | Value |
| --- | --- |
| Path | `Dawnwalker/AssetRegistry.bin` |
| Compressed size | 5,426,463 bytes |
| Compression | method 1 (Oodle), 21 blocks |
| Encrypted | yes |
| Pak | `Dawnwalker-Windows.pak`, v11, 260,318 entries, mount `../../../` |

A 5.4 MB registry is the right order of magnitude for a 260k-entry cook.

**Status: HIGH CONFIDENCE, NOT PROVEN.** The file's existence and role are
established; that it is what blocks registration is inference from the symptom.

## The test that settles it

Extract `AssetRegistry.bin`, decompress (Oodle, via Epic's signed
`oo2core_9_win64.dll` — see `iostore_read.py`), and search it for:

1. `ITM_Weapon_SwordGreatMaster1a` — a retail item that **does** appear in game.
2. `ForgeTestSword0000` — the test item that does **not**.

If the first is present and the second absent, the lead is confirmed and the
blocker is identified precisely.

## If confirmed, the likely route

An **AssetRegistry.bin override** — ship a modified registry that also lists the
new item. Note what that implies: it is a *replacement*, not an additive mod, so
it collides by design. That is the mechanism already proven to work on this
install (`SkillsNoTimeCost` collides on 112 of 113 chunks, `DualSenseAtlas` on 4
of 5), but it also means the "zero collisions" gate has to be restated as
"collides with exactly the intended packages and nothing else".

Risks to weigh before building it: the registry is build-specific and every game
patch replaces it, so the mod would need rebuilding each patch; and a malformed
registry is likely to break asset discovery globally rather than fail quietly.
**Disposable save only.**

## New capability: the legacy pak is readable

The `.pak` index is AES-256-ECB encrypted with the same key as the IoStore
container. `pak_index.py` decrypts the footer-referenced primary index and the
full directory index, giving all 260,318 file paths — config `.ini` files and the
asset registry included, none of which appear in the `.utoc` directory index.

**Nothing was installed. No game file or save was modified.**
