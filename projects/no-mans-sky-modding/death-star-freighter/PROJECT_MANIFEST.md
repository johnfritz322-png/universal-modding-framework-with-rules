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
  decompile to `.MXML` → edit → recompile → place the required mod files in
  a mod folder; if the loader requires `.EXML`, rename the finished `.MXML`
  only after confirming that requirement for the current game build). No base
  `.pak` files are overwritten.
- SDK/toolkit: NMSDK (Blender add-on), `github.com/monkeyman192/NMSDK`.
- Script extender: none used/needed for this project.
- Compiler/runtime: MBINCompiler. Falcon Corvette project last verified
  `v7.03.2-pre1`, hash-checked, against build `25351301` — needs
  re-verification for this project, not carried over as-is.
- Packaging tool: none beyond the mod-folder convention above.
- Other required tools: NMS save editor (e.g. goatfungus NMSSaveEditor) for
  the freighter seed/class fields, per
  `FEASIBILITY.md`.

## Dependencies
| Dependency | Version / range | Required? | Verified source |
|---|---|---|---|
| Blender | 4.5.14 LTS | Yes | **VERIFIED 2026-09-25** — launches against Cosmos 7.04. SHA-256: `57FA1D294EA76448C3BEC84CA758CAF4629611330ABBA7DCF55BB0C56A0A15AB` |
| HGPAKtool | 1.1.3 | Yes (unpack tool) | **VERIFIED 2026-09-25** — extracted a copied `NMSARC.globals.pak` from Cosmos 7.04 |
| MBINCompiler | reports `7.03.2.1` | Yes | **VERIFIED 2026-09-25** — passed a no-edit MBIN→MXML→MBIN→MXML round trip on `gcscratchpadglobals.global.mbin`; both MXML outputs SHA-256-identical |
| NMSDK | `cosmos_fixes` branch, commit `548bfe1` (2026-09-16) | Yes | **BLOCKED 2026-09-25** — add-on fails to load in Blender: its `hgpaktool` Python dependency does not import. See `TOOLCHAIN.md` Step 2. |
| Save editor | goatfungus NMSSaveEditor (or equivalent) | Only for the seed step | web search, not independently confirmed against this game version |

## Repository state
- Project root: `projects/no-mans-sky-modding/death-star-freighter/`
- Default branch: `main`
- Current work branch: `claude/death-star-freighter-mod-iteration`
  (canonical branch for this project's documentation as of 2026-09-25).
- Rollback commit: `origin/main` at `abde3fbb925c263b31aa252e78aa80dc7b3aef7a`
  — since no game file, save, or mod package has been touched, "rollback"
  for this project only ever means discarding/not merging this branch;
  nothing outside git needs to be undone.
- Last known-good commit/build: none — no game build/mod package exists
  yet, only documentation.
- Current milestone: design brief + feasibility research complete;
  toolchain re-verified against Cosmos 7.04 by Codex — Blender, HGPAKtool,
  and MBINCompiler all VERIFIED working (Steps 1-4 of `TOOLCHAIN.md`);
  freighter asset folder located (Step 5, partial); visual concept
  reference published as a Claude artifact and exported into this repo as
  `concept-reference.html` (see `README.md`).
- Next milestone: unblock NMSDK (missing `hgpaktool` Python dependency),
  then continue Step 5 (locate the seed→hull lookup table) and Step 6
  (`Mothership`'s save slot/seed field) — see `HANDOFF.md`.

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
  `FEASIBILITY.md`, not the rounder Sentinel-Design
  family. This confirms (rather than just assumes) that the Death Star hull
  has to be a full custom exterior shell over this donor, not a retexture.

Still needed before gate 3 in the feasibility doc: the save slot number
this freighter occupies (the name alone may be enough to locate its record
in the save JSON, but the slot is the same belt-and-suspenders identifier
the sibling Falcon Corvette project records for its own ships).

## Owned files
- `README.md` — goal, status, how to continue, concept-reference link/description
- `DEATH-STAR-BUILD-BRIEF.md` — desired visual/design (kept separate from feasibility)
- `FEASIBILITY.md` — verified/researched technical capability
- `TOOLCHAIN.md` — environment, tools, and the re-verification checklist
  (folds in Codex's real results)
- `TOOLCHAIN-RESULTS-2026-09-25.md` — Codex's raw toolchain-check report
- `HANDOFF.md` — completed work, remaining work, blockers, next step
- `PROJECT_MANIFEST.md` (this file)
- `concept-reference.html` — the visual concept page, exported as a repo
  file (not just a private Claude artifact link)

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
See `FEASIBILITY.md` in full. Summary: a fully custom
NMSDK-built spherical exterior mesh, added as a new freighter hull table
entry (not a replacement of any stock entry), selected on the target save
by setting that freighter's seed field. The stock freighter core (hangar,
bridge, interior, base-building attach points) is left untouched underneath
the new exterior shell, the same boardability principle the sibling Falcon
Corvette project used for its Corvette core.

## Verified features
| Feature | Verification state | Evidence | Last tested |
|---|---|---|---|
| Toolchain runs on Cosmos 7.04 (Blender launches, HGPAKtool extracts, MBINCompiler round-trips) | VERIFIED | Hashes + identical-SHA-256 round trip, see `TOOLCHAIN.md` Steps 2-4 | 2026-09-25 |
| Freighter assets exist under `MODELS/COMMON/SPACECRAFT/` (`BIGGS`, `COMMONPARTS/HANGARINTERIORPARTS`) | VERIFIED (files present) | Read-only filtered extraction | 2026-09-25 |

## Experimental / unverified features
| Feature | Status | Main uncertainty | Next verification step |
|---|---|---|---|
| Spherical Death Star exterior mesh | Designed only | Not yet modeled | Blocked on NMSDK loading — see below |
| NMSDK add-on | BLOCKED | `hgpaktool` Python dependency fails to import in Blender | Install the dependency into Blender's own Python env per NMSDK's `cosmos_fixes` docs, retry load |
| Additive freighter-hull table entry, seed-selected | HIGH CONFIDENCE architecture, UNVERIFIED specifics | Seed→hull lookup table not yet located (freighter asset folder is, hangar-socket lead is new) | Continue Step 5's table search near `BIGGS`/the freighter path |

## Risks
- **Save corruption / lost freighter or progress**: mitigated by never
  writing to the target save without a fresh four-file backup first
  (framework rule 14); no write has happened yet.
- **Wrong freighter/slot edited**: mitigated by confirming `Mothership`'s
  exact save slot before any write (open item, see `HANDOFF.md`).
- **Toolchain mismatch with the current game build**: the Falcon Corvette
  project's toolchain versions are a week old and not re-verified for this
  project; using them unverified risks a build that doesn't load. Mitigated
  by `TOOLCHAIN.md`'s Step 1/2/4 (build check + round-trip proof) before
  anything is built for real.
- **Mod conflicts with other freighter-hull mods**: unknown until the real
  hull table is located (gate 2); any other mod editing the same table is a
  likely conflict.
- **Hangar/collision risk to boardability**: mitigated by the hangar-in-
  trench design decision (see `DEATH-STAR-BUILD-BRIEF.md`) and by the rule
  that the custom exterior mesh must add no collision over the stock
  hangar, ramp, or interior volumes.
- **Legal/asset-rights risk**: mitigated by using only original geometry
  and textures; a previously deleted "Death Star Capital Freighter" Nexus
  mod is not a source for this project (see `DEATH-STAR-BUILD-BRIEF.md`).

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
  added entry is removed, but this is UNVERIFIED / NEEDS TESTING.
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
