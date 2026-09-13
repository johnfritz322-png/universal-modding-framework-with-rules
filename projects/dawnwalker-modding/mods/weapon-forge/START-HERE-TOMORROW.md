# Start here

**Superseded in part — read [`BREAKTHROUGH-2026-09-13.md`](BREAKTHROUGH-2026-09-13.md)
first.** A DataTable override now works in game; the "nothing loads" framing below
applies only to custom StaticMesh.

Picking this up fresh? That page, then this one. Nothing else is required reading.

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

**The wall — NEW GEOMETRY ONLY:**

**Custom StaticMesh cooked in a stock UE 5.5 project will not load.** Six
attempts, six crashes, ending at `Serial size mismatch: Expected 17488, Actual
18589`. Proved by control: a plain engine cube fails identically, while the
game's own mesh round-tripped through retoc renders fine.

**This wall does NOT apply to data changes.** DataTable overrides work — see the
breakthrough page. Existing game meshes can be swapped freely.

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

**Currently INSTALLED (as of 2026-09-13):**

- `~mods\zzz_VrakhirGargoyle_P.{pak,ucas,utoc}` — the working appearance override
- `ue4ss\Mods\ForgeAppearanceProbe\` — the read-only probe, plus a line in
  `mods.txt` (backed up as `mods.txt.bak-before-appearanceprobe`)
- Older, inert: `ForgeRegistryProbe`, `ForgeItemLoadProbe`, and
  `Dawnwalker\Mods\ForgeRegistryProbe\`

The user's own `SkillsNoTimeCost` and `~JohnRTX5080Quality_P.pak` are untouched.
**No save, base archive or executable has ever been modified.**

Rollback is deleting those files and restoring the backed-up `mods.txt`.
- retoc is at `D:\Dawnwalker-Modding\tools\retoc\` (SHA256-verified).
- UE project at `D:\Dawnwalker-Modding\Projects\DawnwalkerWeaponForge`.
- Game is on build 25232147 (Hotfix 1.0.5) — it has patched three times in a
  week, so re-check the build before trusting any fingerprint.
