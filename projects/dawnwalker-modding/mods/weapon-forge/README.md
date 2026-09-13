# Dawnwalker Weapon Forge

Custom weapon visuals for The Blood of Dawnwalker — five original swords with
matching scabbards, authored by Codex in an Unreal 5.5.4 content-only plugin.

**Status: NOT SHIPPABLE. Do not install the current build.**

**Additive inventory-item test: container format verified; registration/grant is
not yet verified. Do not install it.**

**The game updated on 2026-09-12.** The test remains collision-free and the
retail item format still reads correctly, but no loader from the earlier build
may be used. See `BUILD-RECHECK-2026-09-12.md`.

- [`AUDIT-2026-09-09.md`](AUDIT-2026-09-09.md) — why the cooked build is retired
- [`ATTACHMENT-FINDINGS-2026-09-09.md`](ATTACHMENT-FINDINGS-2026-09-09.md) — Codex's
  asset paths verified, AES key confirmed valid on 258042, and the mesh-override
  route that is actually available
- [`DT_WEAPONAPPEARANCES-2026-09-09.md`](DT_WEAPONAPPEARANCES-2026-09-09.md) — Oodle solved
- [`USMAP-DECODING-2026-09-09.md`](USMAP-DECODING-2026-09-09.md) — property values now
  decode; **`weapon_appearances.csv` maps all 206 weapons to their meshes**
- [`FTEXT-HANDOFF-2026-09-09.md`](FTEXT-HANDOFF-2026-09-09.md) — **read before touching
  `ItemWeaponDataAsset`**: FText solved (string tables), but the item decode is still
  misaligned and the open question is written out with exact offsets
- [`ITEM-WEAPON-DECODE-2026-09-10.md`](ITEM-WEAPON-DECODE-2026-09-10.md) — correction:
  the item decoder is now verified on 191 present weapon packages; new-item
  authoring and registration are still separate unsolved gates
- [`INVENTORY-ITEM-FINDINGS-2026-09-10.md`](INVENTORY-ITEM-FINDINGS-2026-09-10.md)
  — separate-inventory-item route, its verified evidence, and its remaining
  authoring blocker
- [`DISPOSABLE-ITEM-TEST-2026-09-10.md`](DISPOSABLE-ITEM-TEST-2026-09-10.md)
  — a new-ID, zero-collision container that has passed packing and read-back
  checks; game registration and granting remain the final unsolved gate
- [`NEXT-STEPS-HANDOFF-2026-09-10.md`](NEXT-STEPS-HANDOFF-2026-09-10.md)
  — exact resume point, finished checks, safety limits, and the first in-game
  test sequence
- [`BUILD-RECHECK-2026-09-12.md`](BUILD-RECHECK-2026-09-12.md) — current Steam
  build fingerprint and the tests repeated after the update
- [`LOADER-COMPATIBILITY-2026-09-12.md`](LOADER-COMPATIBILITY-2026-09-12.md) —
  current-build loader check and the conditions required before an in-game test

## Where the pieces live

These paths are on John's PC and are not mirrored into this repository — the build
alone is 143 MB.

| Piece | Path |
| --- | --- |
| Unreal project | `D:\Dawnwalker-Modding\Projects\DawnwalkerWeaponForge` |
| Engine | `D:\UE55\UE_5.5` |
| Source meshes | `…\SourceArt\Weapons`, `…\SourceArt\Scabbards` |
| Cooked build | `Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\outputs\DawnwalkerWeaponForge-VerifiedBuild` |
| Codex's handoff | same `outputs\` folder, `DawnwalkerWeaponForge-HANDOFF.md` |

The five swords: Riftforged Slabblade, Nightfall Colossus, Moonrend Cleaver,
Emberveil Saber, Oathlight Longsword.

## What has to be true before this ships

1. **Cook scope.** Only `/DawnwalkerWeaponForge/Weapons`, engine content excluded.
   Verify with `python verify_container.py <mod.utoc> --expect-none` — it must
   report 0 collisions. The current build reports 390.
2. **Real geometry.** The source meshes are 40-vert boxes with no UVs and no
   normals. They need actual modelling before any visual judgement is meaningful.
3. **An attachment route.** Now partly answered — see
   `ATTACHMENT-FINDINGS-2026-09-09.md`. The available route is a **targeted mesh
   override**, not an additive plugin, which means gate 3 below changes from "zero
   collisions" to "collides with exactly the intended packages and nothing else".
   Still unknown: which sword folder a given item uses. That mapping lives in
   `/Game/_Dawnwalker/Inventory/Items/DT_WeaponAppearances`.
4. **Build match.** The game patched to `dw1-pc-258042` (Steam build 25191761) on
   2026-09-09. Re-verify against the current build, not the notes.
5. **Disposable save.** First install goes on a throwaway save, never the main
   playthrough.

## verify_container.py

Reports which base-game packages a mod container replaces, by intersecting IoStore
chunk-ID tables. Works on the encrypted base container with **no AES key and no
Oodle** — chunk IDs live in the TOC header region, outside the encrypted directory
index. Standard library only.

```bash
python verify_container.py "<mod>.utoc"                 # report replacements
python verify_container.py "<mod>.utoc" --expect-none   # additive mod: fail on any
```

Collision is normal for a *replacement* mod — `SkillsNoTimeCost` collides on 112 of
113 chunks and that is it working. Use `--expect-none` only for mods that mean to
add rather than replace.

## Related

- Format research: [`../../../../games/blood-of-the-dawnwalker/`](../../../../games/blood-of-the-dawnwalker/)
- Build fingerprint: [`../../GAME_VERSION.md`](../../GAME_VERSION.md)
