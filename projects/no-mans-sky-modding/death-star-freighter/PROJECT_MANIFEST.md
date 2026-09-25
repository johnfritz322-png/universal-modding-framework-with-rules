# Project Manifest

## Identity
- Project name: Death Star S-Class Freighter
- Game: No Man's Sky
- Exact game version/build: UNVERIFIED for this project. Last known Steam
  build from the sibling Falcon Corvette project was `25351301`
  (2026-09-18) — must be re-checked, not assumed current.
- Platform: PC / Steam (app `275850`), per the Falcon Corvette project's
  toolchain check.
- Engine: NMS's own engine; modding surface is `.MBIN`/`.EXML` assets via
  MBINCompiler, plus custom geometry via NMSDK (Blender add-on).
- Mod version: unreleased / not yet built.

## Toolchain
- Mod loader/framework: NMS `GAMEDATA\MODS` folder convention (unpack →
  decompile → edit → recompile → place as `.EXML`/`.MBIN` in a mod folder;
  no overwriting base `.pak` files).
- SDK/toolkit: NMSDK (Blender add-on), `github.com/monkeyman192/NMSDK`.
- Script extender: none used/needed for this project.
- Compiler/runtime: MBINCompiler. Falcon Corvette project last verified
  `v7.03.2-pre1`, hash-checked, against build `25351301` — needs
  re-verification for this project, not carried over as-is.
- Packaging tool: none beyond the mod-folder convention above.
- Other required tools: NMS save editor (e.g. goatfungus NMSSaveEditor) for
  the freighter seed/class fields, per
  `FREIGHTER-MODDING-FEASIBILITY.md`.

## Dependencies
| Dependency | Version / range | Required? | Verified source |
|---|---|---|---|
| Blender | 4.5.14 (matches NMSDK's stated 4.2+ support) | Yes | Reused from `../falcon-corvette/TOOLCHAIN-CHECK-2026-09-18.md`; not re-verified for this project |
| NMSDK | latest from upstream repo | Yes | `github.com/monkeyman192/NMSDK` |
| MBINCompiler | `v7.03.2-pre1` (last known) | Yes | Reused from `../falcon-corvette/TOOLCHAIN-CHECK-2026-09-18.md`; not re-verified for this project |
| Save editor | goatfungus NMSSaveEditor (or equivalent) | Only for the seed/class step | web search, not independently confirmed against this game version |

## Repository state
- Project root: `projects/no-mans-sky-modding/death-star-freighter/`
- Default branch: `main`
- Current work branch: `claude/death-star-freighter-mod-itel2i`
- Last known-good commit/build: none — no build exists yet.
- Current milestone: design brief + feasibility research complete;
  `TOOLCHAIN-CHECK.md` written and handed to the user to run; visual
  concept reference published (silhouette schematic + hull-envelope fit —
  <https://claude.ai/artifact/HXVQFaWVzMVHtzaxj68zEH>).
- Next milestone: results of `TOOLCHAIN-CHECK.md` (build match, real
  freighter model path, `Mothership`'s save slot/seed field).

## Target freighter
**VERIFIED from an in-game screenshot supplied by the user (2026-09-25)** —
the first directly-observed evidence in this project, as opposed to the web
search material everywhere else in these docs:
- Name: `Mothership`
- Class: **S** (confirmed by the in-game class badge, not inferred)
- Hyperdrive Range: 3306.1
- Warp Efficiency: 1.0
- Storage Space: 120
- Fleet Coordination: 55.0
- Hull silhouette in the screenshot: an elongated, flat, angular-bowed
  wedge — visually matches the **Venator-family** description in
  `FREIGHTER-MODDING-FEASIBILITY.md`, not the rounder Sentinel-Design
  family. This confirms (rather than just assumes) that the Death Star hull
  has to be a full custom exterior shell over this donor, not a retexture.

Still needed before gate 3 in the feasibility doc: the save slot number
this freighter occupies (the name alone may be enough to locate its record
in the save JSON, but the slot is the same belt-and-suspenders identifier
the sibling Falcon Corvette project records for its own ships).

## Owned files
- `DEATH-STAR-BUILD-BRIEF.md`
- `FREIGHTER-MODDING-FEASIBILITY.md`
- `TOOLCHAIN-CHECK.md`
- `PROJECT_MANIFEST.md` (this file)

No game asset, save file, or mod package exists yet.

## Stable identifiers
None allocated yet. No FormID/UUID/namespace/resource-key equivalents exist
in this project until the freighter hull table entry and its seed value are
chosen in gate 2/3 of the feasibility doc. When they are, they get recorded
here and are never casually regenerated afterward, per framework rule 7.

## Vanilla systems touched
None yet. Planned (pending verification, see feasibility doc gate 2):
- one **added** freighter hull/model table entry (exact MBIN not yet
  confirmed);
- one freighter's save-data hull-seed field, on the user's existing
  already-owned S-class freighter. Nothing else in that freighter's record
  (class, stats, name, crew) is planned to change.

No vanilla table row is planned to be overwritten — only added to, matching
the non-destructive precedent found in the gFreighter mod.

## Architecture
See `FREIGHTER-MODDING-FEASIBILITY.md` in full. Summary: a fully custom
NMSDK-built spherical exterior mesh, added as a new freighter hull table
entry (not a replacement of any stock entry), selected on the target save
by setting that freighter's seed field. The stock freighter core (hangar,
bridge, interior, base-building attach points) is left untouched underneath
the new exterior shell, the same boardability principle the sibling Falcon
Corvette project used for its Corvette core.

## Verified features
| Feature | Verification state | Evidence | Last tested |
|---|---|---|---|
| (none) | — | — | — |

## Experimental / unverified features
| Feature | Status | Main uncertainty | Next verification step |
|---|---|---|---|
| Spherical Death Star exterior mesh | Designed only | Not yet modeled | Build in Blender/NMSDK, inspect locally |
| Additive freighter-hull table entry, seed-selected | HIGH CONFIDENCE architecture, UNVERIFIED specifics | Exact MBIN table + save field names unconfirmed | Inspect user's unpacked game files directly |

## Compatibility
- Known compatible mods: none checked yet.
- Known conflicts: any other mod that also adds/overwrites freighter hull
  table entries is a likely conflict surface — not yet checked.
- Shared edit surfaces: freighter hull/model table (planned addition only).
- Existing compatibility patches: none.
- Needed compatibility patches: unknown until gate 2 identifies the real
  table.

## Save / persistence notes
- Safe on existing saves?: not yet established — depends on gate 3.
- Safe to update mid-save?: unknown.
- Safe to uninstall mid-save?: unknown; freighter would very likely revert
  to whatever hull its seed's default table entry resolves to once the
  added entry is removed, but this is an ASSUMPTION until tested.
- Fresh-save testing required?: a full save backup (4-file, mirroring the
  Falcon project's practice) is required before any write to the target
  save, regardless of which save is used.

## Known bugs and limitations
None yet — nothing has been built.

## Test procedure
- Test save/profile: target is `Mothership`, the user's existing S-class
  freighter (see "Target freighter" above). Save slot number still needed.
  Unrelated to, and must not be confused with, the sibling Falcon Corvette
  project's own slot 7 / slot 8 (`Darth Fritz`).
- Launch steps: TBD, pending toolchain re-verification.
- Feature test steps: summon/warp to the freighter, dock, walk the stock
  interior, exit, save, reload, repeat — per the boardability rule in the
  build brief.
- Regression test steps: confirm no other freighter/save data changed, and
  that freighter base building still functions.
- Logs to inspect: TBD once the toolchain is re-verified.

## Build and release
- Build command/process: TBD (NMSDK export → MBINCompiler recompile →
  mod-folder packaging), pending gate 2.
- Validation command/process: TBD.
- Packaging process: additive mod folder under `GAMEDATA\MODS`, no vanilla
  `.pak` overwrite.
- Release artifact location: not applicable yet — private/local build only
  per the legal guardrail in the build brief.
