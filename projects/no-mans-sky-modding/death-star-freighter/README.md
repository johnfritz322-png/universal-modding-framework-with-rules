# Death Star S-Class Freighter

## Goal
Reskin the player's existing S-class capital freighter, **`Mothership`**,
with an original, Death-Star-styled spherical exterior hull — a near-
perfect sphere with one offset concave superlaser dish, a full-circumference
equatorial trench (the stock hangar mouth lives inside this trench, not
under the dish), and dense surface paneling — while leaving the freighter's
class, stats, name, crew, hangar, bridge, and interior completely untouched.

This is a **design/research project only** as of 2026-09-25. Nothing has
been built, compiled, installed, or tested in game.

## Current status
**Designed / Researched.** No game file, save, or mod package has been
touched. See `HANDOFF.md` for the precise breakdown of what's done, what's
open, and the exact next step. In short:

- Visual design (the sphere, dish, trench, paneling, hangar-in-trench
  placement, hull-envelope scaling rule) is fully worked out —
  `DEATH-STAR-BUILD-BRIEF.md`.
- The technical architecture (custom NMSDK exterior mesh, added as a new
  freighter hull table entry, selected via the target freighter's save
  seed field — no class/stat edits at all) is researched and recorded, but
  built on `WebSearch` summaries rather than primary sources or the user's
  own game files, so it is labelled HIGH CONFIDENCE, not VERIFIED —
  `FEASIBILITY.md`.
- The target freighter is confirmed from the user's own screenshot:
  `Mothership`, S-class, a Venator-family wedge hull — `PROJECT_MANIFEST.md`
  → "Target freighter".
- A toolchain re-verification checklist is written but not yet run —
  `TOOLCHAIN.md`.

## How to continue
1. Read `HANDOFF.md` first — it has the exact next verification step.
2. Run the checklist in `TOOLCHAIN.md` on the machine that has No Man's Sky
   installed (this repo's own sessions do not have game access). Report
   results back into this project's docs.
3. Once the real freighter hull table and `Mothership`'s save slot/seed
   field are confirmed (gates 2, 3, 5, 6 in `FEASIBILITY.md` /
   `TOOLCHAIN.md`), move to building the sphere mesh in Blender/NMSDK.
4. Keep every claim honestly labelled — VERIFIED, HIGH CONFIDENCE,
   UNVERIFIED, or NEEDS TESTING — and never call a design "implemented" or
   "tested" without direct evidence, per this framework's `AGENTS.md`.

## Visual concept reference
The sphere silhouette, the five non-negotiables, and how the sphere has to
fully enclose `Mothership`'s elongated wedge hull (the "envelope rule") are
shown as diagrams, not just described in prose. Two copies exist:

- **In this repository**: `concept-reference.html` — a static, self-
  contained HTML file. Open it directly in a browser; no server or network
  access required. This is the authoritative, durable copy — it does not
  depend on any external account or link staying alive.
- **Hosted (private, for interactive viewing only)**:
  <https://claude.ai/artifact/HXVQFaWVzMVHtzaxj68zEH> — a Claude Artifact
  page, private to the user's account. Do not treat this link as the
  primary record; `concept-reference.html` in this folder is.

What the page shows, in detail:
- A side-profile schematic of the sphere: the offset concave dish (sized
  at roughly 0.29× the hull diameter, positioned off the pole and off the
  equator), the full-circumference equatorial trench with a marked hangar
  opening inside it, and a panel-grid texture representing the dense
  surface paneling.
- The five non-negotiable silhouette rules from `DEATH-STAR-BUILD-BRIEF.md`
  as a checklist.
- A comparison diagram showing `Mothership`'s confirmed elongated wedge
  hull enclosed inside a dashed circle sized to the hull's full length (the
  envelope rule), with the hangar mouth marked as sitting inside the trench
  band at an as-yet-unconfirmed position around the ring.
- A materials/surface-treatment swatch set (cold gunmetal hull, dark
  trench/dish interior, a warm accent reserved for the dish well only).
- A status strip repeating this framework's own verification labels
  against each design claim, so the page doesn't imply more certainty than
  the written docs do.

## Repository layout for this project
```text
projects/no-mans-sky-modding/death-star-freighter/
├── README.md                  (this file)
├── DEATH-STAR-BUILD-BRIEF.md  (desired visual/design)
├── FEASIBILITY.md             (verified/researched technical capability)
├── TOOLCHAIN.md               (environment + re-verification checklist)
├── HANDOFF.md                 (done / remaining / blockers / next step)
├── PROJECT_MANIFEST.md        (environment, dependencies, risks, tests, rollback)
└── concept-reference.html     (exported visual concept page)
```

## Related project
The sibling `../falcon-corvette/` project (a Millennium Falcon Corvette
reskin) established the toolchain this project reuses (Blender, NMSDK,
MBINCompiler) and the boardability discipline (stock functional core must
stay untouched under any custom exterior). It is a different game system
(Corvettes are player-buildable via save `Objects[]`; freighters are not)
and a different save target — do not confuse the two projects' save slots
or ships.
