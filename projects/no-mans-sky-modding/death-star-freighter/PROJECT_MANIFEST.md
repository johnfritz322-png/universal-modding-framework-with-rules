# Project Manifest

## Identity
- Project name: Death Star S-Class Freighter
- Game: No Man's Sky
- Exact installed Steam build: `25441199`, reread locally 2026-09-25 UTC.
  Project release label: Cosmos 7.04. Recheck after any game update.
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
- Compiler/runtime: existing `v7.03.2-pre1` executable, generated MXML
  version `7.03.2.1`; same SHA-256 as the prior check. No-edit round trips
  pass for the three files listed in `TOOLCHAIN.md`.
- Packaging tool: none beyond the mod-folder convention above.
- Other required tools: NMS save editor (e.g. goatfungus NMSSaveEditor) for
  any eventual verified hull-selection fields, per
  `FEASIBILITY.md`.

## Dependencies
| Dependency | Version / range | Required? | Verified source |
|---|---|---|---|
| Blender | 5.0.1 for native extension; 4.5.14 registration also passes | Yes | **VERIFIED 2026-09-25** — fresh-process extension enable in dedicated 5.0.1 profile; matches SDK manifest >=5.0.0. See repair report for hashes. |
| HGPAKtool | 1.1.3 | Yes (unpack tool) | **VERIFIED 2026-09-25** — extracted a copied `NMSARC.globals.pak` from Cosmos 7.04 |
| MBINCompiler | reports `7.03.2.1` | Yes | **VERIFIED 2026-09-25** — passed a no-edit MBIN→MXML→MBIN→MXML round trip on `gcscratchpadglobals.global.mbin`; both MXML outputs SHA-256-identical |
| NMSDK | `cosmos_fixes` + local compatibility commits `2d8c239`, `19f467a`, `390ef27`; manifest `0.10.0-alpha14` | Yes | **VERIFIED for capital-root and original-shell import/export** — isolated Blender 5.0.1 profile, current-game dependency closure, and a generated mesh re-import all pass. |
| Python archive dependencies | hgpaktool 1.1.3; zstandard 0.23.0; lz4 4.4.5 in Blender 4.5 | Yes | See `NMSDK-REPAIR-2026-09-25.md` for installation scope and hashes; native 5.0.1 uses its extension wheel environment. |
| Save editor | goatfungus NMSSaveEditor (or equivalent) | Only for the seed step | web search, not independently confirmed against this game version |

## Repository state
- Project root: `projects/no-mans-sky-modding/death-star-freighter/`
- Default branch: `main`
- Current work branch: `claude/death-star-freighter-mod-iteration`
  (canonical branch for this project's documentation as of 2026-09-25).
- Rollback commit: `origin/main` at `abde3fbb925c263b31aa252e78aa80dc7b3aef7a`
  — since no game file, save, or mod package has been touched, "rollback"
  for this project only ever means discarding/not merging this branch;
  no game/save rollback is needed. Local dependency/profile rollback for
  the new tooling setup is described in `NMSDK-REPAIR-2026-09-25.md`.
- Last known-good commit/build: none — no game build/mod package exists
  yet, only documentation.
- Current milestone: design brief + feasibility research complete;
  toolchain re-verified against Cosmos 7.04 by Codex — Blender, HGPAKtool,
  and MBINCompiler all VERIFIED working (Steps 1-4 of `TOOLCHAIN.md`);
  freighter asset folder located (Step 5, partial); visual concept
  reference published as a Claude artifact and exported into this repo as
  `concept-reference.html` (see `README.md`).
- Current follow-up: NMSDK dependency repair and capital-root scene
  import/export pass. Actual capital scene, descriptor and AI mapping found;
  see `FREIGHTER-SELECTION-FINDINGS.md`.
- Next milestone: measure the donor root and make one minimal original
  exterior-shell probe — see `WHATS-NEXT.md`.
- Review checkpoint branch: `codex/death-star-nmsdk-fix`, based on canonical
  commit `2a57866`; preserve newer canonical work during incorporation.

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
- `NMSDK-REPAIR-2026-09-25.md` — dependency repair and startup evidence
- `FREIGHTER-SELECTION-FINDINGS.md` — current game model/descriptor evidence
- `HANGAR-APPROACH-FINDINGS-2026-09-25.md` — stock hangar-module and approach
  evidence; runtime attachment remains unverified
- `SAVE-READONLY-FINDINGS-2026-09-25.md` — live Mothership resource and seed
  evidence, read-only
- `BLENDER-ROUNDTRIP-2026-09-25.md` — reproducible current-build scene
  import/export blocker
- `WHATS-NEXT.md` — resume order and local paths
- `tools/verify_nmsdk_load.py` — repeatable load and archive check
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
**candidate, still UNVERIFIED for personal-only selection**, consisting of an
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
| Capital scene/descriptor under `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/`; AI mapping distinguishes BIGGS as Corvette | VERIFIED for inspected data | `FREIGHTER-SELECTION-FINDINGS.md` | 2026-09-25 |
| Mothership uses the capital-freighter scene and its current seed is known | VERIFIED — Primary, read-only | `SAVE-READONLY-FINDINGS-2026-09-25.md` | 2026-09-25 |
| NMSDK current-build capital-root scene import/export | VERIFIED for the actual capital root after isolated `InstanceTransforms` compatibility patch and read-only dependency closure; recursive referenced components remain untested | `BLENDER-ROUNDTRIP-2026-09-25.md` | 2026-09-25 |
| NMSDK starts enabled in dedicated Blender 5.0.1 profile | VERIFIED for loading/archive access | `NMSDK-REPAIR-2026-09-25.md` | 2026-09-25 |

## Experimental / unverified features
| Feature | Status | Main uncertainty | Next verification step |
|---|---|---|---|
| Spherical Death Star exterior mesh | Scratch-only stage 2 passes export/re-import: sphere, concave off-axis dish, equatorial trench, and shallow panel relief | Hangar clearance and in-game behavior are absent | Establish docking approach, build a clear opening, then verify selection architecture before packaging |
| Full recursive capital component import/export | NEEDS TESTING | Root control intentionally did not recursively import component scenes | Re-run against a complete recursive dependency closure before relying on component fidelity |
| Personal-only additive hull selection | UNVERIFIED | Observed descriptor/model mapping does not establish custom seed registration | Trace target resource/seed and a verified working implementation |

## Risks
- **Save corruption / lost freighter or progress**: mitigated by never
  writing to the target save without a fresh four-file backup first
  (framework rule 14); no write has happened yet.
- **Wrong freighter/slot edited**: mitigated by confirming `Mothership`'s
  exact save slot before any write (open item, see `HANDOFF.md`).
- **Toolchain mismatch with current geometry**: tested loading and sample
  conversions pass, but geometry export is unverified. Use the manifest-
  compatible Blender 5.0.1 profile and verify a minimal exported scene
  before building the custom hull.
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
