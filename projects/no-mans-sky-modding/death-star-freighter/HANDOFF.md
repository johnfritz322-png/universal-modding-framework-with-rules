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
- **Toolchain re-verification checklist written** (`TOOLCHAIN.md`): six
  steps (build check, portable Blender/NMSDK/MBINCompiler re-verification,
  pick + confirm a PAK unpack tool, a compile/decompile round-trip proof,
  locate the real freighter hull table, locate `Mothership`'s save
  record/seed field). Not yet run.
- **Visual concept reference published**, both as a hosted Claude Artifact
  and exported into this repo as `concept-reference.html`, showing the
  silhouette schematic, the five non-negotiables, and the hull-envelope
  fit over `Mothership`'s confirmed hull shape.

## Remaining work
In dependency order (later steps need earlier ones):
1. Run `TOOLCHAIN.md` Steps 1-4 on the machine with the game installed:
   confirm current Steam build, re-verify or update Blender/NMSDK/
   MBINCompiler, pick a PAK unpack tool, prove a compile/decompile
   round-trip on a harmless file.
2. Run `TOOLCHAIN.md` Step 5: locate the real freighter hull/model table
   and geometry file naming convention (only the *frigate* — small escort
   ship — path is confirmed from research so far; the freighter path is
   still unconfirmed and must not be assumed to mirror it).
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
- **This session has no No Man's Sky install, no Blender, and no unpacked
  game files.** Every step above from Step 1 onward has to run on the
  user's own machine; nothing here can build, compile, or test anything.
- **The real freighter hull table/model path is unconfirmed.** Research
  only confirmed the naming pattern for *frigates* (a different, smaller
  object than the freighter itself); do not assume the freighter table
  mirrors that pattern without checking.
- **`Mothership`'s save slot number is not yet known** (its name is known
  from the screenshot, which may be enough to locate the record, but the
  slot has not been separately confirmed).
- **No fresh backup of the target save exists yet** — required before any
  future write step, not optional.

## Exact next verification step
Run `TOOLCHAIN.md` **Step 1** (confirm the currently installed Steam
build id and the game executable's timestamp) on the machine that has No
Man's Sky installed, and report the result back into this project. Every
later gate assumes this is current, not the week-old figure carried over
from the sibling Falcon Corvette project.

## Honest status
Highest verified state reached, per this framework's own scale (Designed
→ Implemented → Compiles → Validates → Loads → Tested In-Game →
Regression Tested → Compatibility Tested → Release Ready):

**Designed.** The visual design is finished and the technical architecture
is researched to HIGH CONFIDENCE, but nothing has been implemented,
compiled, loaded, or tested. No claim beyond "Designed" is made anywhere
in this project's documentation.
