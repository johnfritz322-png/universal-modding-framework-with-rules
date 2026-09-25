# Death Star freighter — handoff

## Completed work
- **Visual design finalized** (`DEATH-STAR-BUILD-BRIEF.md`): near-perfect
  sphere, offset concave superlaser dish (≈0.29× hull diameter), full-
  circumference equatorial trench, dense uniform panel greebling, no
  forward/aft asymmetry. Hull-envelope rule set: sphere diameter = the
  stock hull's full length. Hangar placement decided: inside the trench,
  not centered under the dish (matches source material's own placement of
  landing bays, and is the lower-risk build — one coordinate to match
  instead of two, and no risk of collision near a crater-shaped opening).
- **Target freighter confirmed from direct evidence** (`PROJECT_MANIFEST.md`
  → "Target freighter"): `Mothership`, S-class (confirmed by the in-game
  class badge in a user-supplied screenshot, not inferred), a Venator-
  family wedge hull. This is VERIFIED, not HIGH CONFIDENCE — it came from
  the user's own game, not secondhand research.
- **Scope decision recorded**: the mod targets this already-owned S-class
  freighter. No class, stat, name, or crew field will be touched — the
  only planned save write is the freighter's hull-seed field. This removed
  the earlier open question of "grind vs. save-edit for S-class" entirely.
- **Technical architecture researched** (`FEASIBILITY.md`): no in-game
  freighter hull editor exists (unlike Corvettes), so a new silhouette
  needs a custom NMSDK exterior mesh. Working mechanism, based on an
  existing shipped mod's documented behavior: add a new hull entry to the
  freighter model table (non-destructive, no vanilla row overwritten),
  select it on the target save via that freighter's procedural seed field.
  Labelled **HIGH CONFIDENCE, not VERIFIED** — built from `WebSearch`
  summaries; the exact MBIN table and save field names have not been
  confirmed against real files.
- **Toolchain re-verified against the real, current build** (Cosmos 7.04,
  Steam build `25441199`) by Codex, 2026-09-25 — `TOOLCHAIN.md` and
  `TOOLCHAIN-RESULTS-2026-09-25.md`:
  - **VERIFIED, evidence-backed**: Blender 4.5.14 LTS launches (SHA-256
    recorded); HGPAKtool 1.1.3 extracts real archives; MBINCompiler
    `7.03.2.1` passed a no-edit MBIN→MXML→MBIN→MXML round trip with
    identical MXML hashes.
  - **BLOCKED**: NMSDK (`cosmos_fixes` branch, commit `548bfe1`) fails to
    load in Blender — its `hgpaktool` Python dependency doesn't import.
    Nothing needing the Blender add-on (building the sphere mesh) can
    start until this is fixed.
  - **Partial**: freighter assets confirmed present under
    `MODELS/COMMON/SPACECRAFT/` (`BIGGS`, `COMMONPARTS/HANGARINTERIORPARTS`
    — the latter hints the hangar may be a shared modular piece attached
    to a socket, not baked into each hull). The seed→hull lookup table
    itself is **still not found** — the core architecture hypothesis
    remains HIGH CONFIDENCE, not VERIFIED.
  - No game file or save was modified during any of this.
- **Visual concept reference published**, both as a hosted Claude Artifact
  and exported into this repo as `concept-reference.html`, showing the
  silhouette schematic, the five non-negotiables, and the hull-envelope
  fit over `Mothership`'s confirmed hull shape.

## Remaining work
In dependency order (later steps need earlier ones):
1. **Unblock NMSDK**: install its `hgpaktool` Python dependency into
   Blender's own Python environment (not system Python) per whatever the
   `cosmos_fixes` branch's own docs specify, then confirm the add-on
   actually loads.
2. Continue `TOOLCHAIN.md` Step 5: find the seed→hull lookup table itself,
   now that the freighter asset folder is located — try names like
   `GENERATIONTABLE`, `SPAWNTABLE`, or `PARTSTABLE` near `BIGGS`. Also
   worth chasing: the `HANGARINTERIORPARTS` socket-attachment lead, since
   it may change how hangar placement gets built.
3. Run `TOOLCHAIN.md` Step 6: locate `Mothership`'s exact save slot and
   its hull-seed field, by name, without changing anything yet.
4. Once 1-3 are confirmed: build the sphere mesh in Blender/NMSDK
   (geometry, UVs — careful at the poles, normals, materials), matching
   the envelope rule and hangar-in-trench placement from the build brief.
5. Add the new hull entry to the real table (found in step 2 above) via
   MBINCompiler, keeping the change additive (no vanilla row overwritten).
6. Back up the target save (fresh four-file backup, mirroring the sibling
   Falcon Corvette project's practice) before touching it at all.
7. Set `Mothership`'s hull-seed field to select the new entry. No other
   field on that freighter changes.
8. Test: summon/dock at the freighter, walk the stock interior, exit,
   save, reload, repeat — per the boardability rule — before this is ever
   called usable.
9. Regression check: confirm no other save data changed and freighter base
   building still works.

## Blockers
- **NMSDK does not load** — missing `hgpaktool` Python dependency inside
  Blender. This is the active blocker; everything requiring the Blender
  add-on waits on it.
- **The seed→hull lookup table is still unconfirmed.** The freighter asset
  folder is now known, but the actual table that would need a new entry
  has not been found yet.
- **`Mothership`'s save slot number is not yet known** (its name is known
  from the screenshot, which may be enough to locate the record, but the
  slot has not been separately confirmed — Step 6 not yet run).
- **No fresh backup of the target save exists yet** — required before any
  future write step, not optional.
- This cloud session still has no No Man's Sky install, no Blender, and no
  unpacked game files — every remaining step has to run on the machine
  that has the game (Codex has been doing this).

## Exact next verification step
Install `hgpaktool` into Blender's own Python environment so NMSDK's
`cosmos_fixes` add-on actually loads, then confirm it loads. Everything
past that (sphere mesh, table search) is gated on this one fix.

## Honest status
Highest verified state reached, per this framework's own scale (Designed
→ Implemented → Compiles → Validates → Loads → Tested In-Game →
Regression Tested → Compatibility Tested → Release Ready):

**Designed.** The visual design is finished and the technical architecture
is researched to HIGH CONFIDENCE, but nothing has been implemented,
compiled, loaded, or tested. No claim beyond "Designed" is made anywhere
in this project's documentation.
