# Start here

Picking this up fresh? Read this page, then `vrakhir-override/RETOC-RESULT-2026-09-13.md`.
Nothing else is required reading.

## The goal

A custom sword in The Blood of Dawnwalker, as its own inventory item.

## Where it actually stands

**Solved and proven:**

- The whole game archive is readable — AES, Oodle, usmap property decoding.
  `weapon_appearances.csv` maps all 206 weapons to their meshes;
  `dump_weapon_items.py` emits 192 items with real stats.
- **The override route works.** A container in `~mods` at a matching package path
  does replace the game's asset. Chunk ids match, collisions verified at exactly 1.
- Why a *new* item never registers: it is not in the baked `AssetRegistry.bin`.
  Confirmed by extraction — every listed item is in it, the test item is not.

**The wall:**

**Packages cooked in a stock UE 5.5 project are not loadable by this game.** Five
in-game attempts, five crashes. Proved by control: a plain engine cube fails
identically to a custom sword, so mesh content is not the cause. retoc's
`to-zen` produces a structurally perfect container — 347-byte stub pak matching
the working mods, correct chunk id, 1 collision — and it still crashes.

## Do this first tomorrow

**Establish a known-good round trip before building anything new.**

1. Take `00000000_SkillsNoTimeCost_P.*` from `~mods` — it demonstrably works.
2. `retoc to-legacy` it.
3. Change one trivial thing, or nothing at all.
4. `retoc to-zen` it back.
5. Install and confirm the game still works.

If the untouched round trip fails, the problem is in the conversion and that is
where to dig. If it survives, add one small change at a time until it breaks —
the break point is the answer.

**This is the step that was skipped.** Everything so far built custom content
first and tested the pipeline last, which is why it took five failures to locate
the wall.

## The other open lead

Script objects. Cooked packages reference classes through indices into a table in
the global container; this game defines 58,720, and a stock UE 5.5 project's set
differs. `retoc print-script-objects` on the game's `global.utoc` will dump it.
May need reflection data via [jmap](https://github.com/trumank/jmap).

## Tools, all in this folder

| File | Does |
| --- | --- |
| `iostore_read.py` | Read any package out of the encrypted archive (AES + Oodle) |
| `usmap.py`, `unversioned.py` | Decode cooked property values |
| `pak_index.py`, `pak_extract.py` | Read the legacy pak — config and AssetRegistry live there |
| `assetregistry.py` | Parse the registry header and name table |
| `verify_container.py` | What a mod replaces — **run before every install** |
| `verify_asset_path.py` | Confirm an asset path exists, no key needed |
| `dump_weapon_appearances.py`, `dump_weapon_items.py` | The data dumps |

`vrakhir-override/BUILD-PIPELINE.md` has the full build steps and seven documented
dead ends. Do not rediscover them.

## State of the machine

- **Nothing of ours is installed.** `~mods` has only `SkillsNoTimeCost` and the
  RTX 5080 profile. No save, base archive or executable was ever modified.
- retoc is at `D:\Dawnwalker-Modding\tools\retoc\` (SHA256-verified).
- UE project at `D:\Dawnwalker-Modding\Projects\DawnwalkerWeaponForge`.
- Game is on build 25232147 (Hotfix 1.0.5) — it has patched three times in a
  week, so re-check the build before trusting any fingerprint.
