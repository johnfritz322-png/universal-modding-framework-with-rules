# Death Star S-Class Freighter

## Goal
Reskin the player's existing S-class capital freighter, **`Mothership`**,
with an original, Death-Star-styled spherical exterior hull — a near-
perfect sphere with one offset concave superlaser dish, a full-circumference
equatorial trench (the stock hangar mouth lives inside this trench, not
under the dish), and dense surface paneling — while leaving the freighter's
class, stats, name, crew, hangar, bridge, and interior completely untouched.

This is a **design/research and scratch-geometry project** as of 2026-09-25.
An original spherical exterior prototype has exported and re-imported through
NMSDK, but no mod package has been built or installed and nothing has been
tested in game.

## Current status
**Latest checkpoint:** start with [WHATS-NEXT.md](WHATS-NEXT.md).
NMSDK's missing dependency is fixed; Blender 5.0.1 with the dedicated
profile starts with the extension enabled. The actual capital scene and
descriptor have been located. Evidence and limits are in
[NMSDK-REPAIR-2026-09-25.md](NMSDK-REPAIR-2026-09-25.md) and
[FREIGHTER-SELECTION-FINDINGS.md](FREIGHTER-SELECTION-FINDINGS.md).

**Designed / scratch geometry verified.** No game file, save, or mod package
has been touched. See `WHATS-NEXT.md` for the precise breakdown of what's
done, what's open, and the exact next step. In short:

- Visual design (the sphere, dish, trench, paneling, hangar-in-trench
  placement, hull-envelope scaling rule) is fully worked out —
  `DEATH-STAR-BUILD-BRIEF.md`.
- The technical architecture (custom NMSDK exterior mesh, added as a new
  freighter hull table entry, selected via the target freighter's save
  seed field — no class/stat edits at all) is researched and recorded, but
  built on `WebSearch` summaries rather than primary sources or the user's
  own game files. Personal-only seed selection remains UNVERIFIED —
  `FEASIBILITY.md`.
- The target freighter is confirmed from the user's own screenshot:
  `Mothership`, S-class, a Venator-family wedge hull — `PROJECT_MANIFEST.md`
  → "Target freighter".
- Toolchain loading and specific file round trips have passed —
  `TOOLCHAIN.md`. An original stage-3 sphere/dish/trench/aperture prototype
  exports and re-imports; its aperture is visual-only because the live
  root-to-hangar transform remains unverified. See
  `BLENDER-ROUNDTRIP-2026-09-25.md` and
  `RUNTIME-ATTACHMENT-EVIDENCE-PLAN.md`.

## How to continue
1. Read `WHATS-NEXT.md` first — it has the ordered resume steps.
2. Run the checklist in `TOOLCHAIN.md` on the machine that has No Man's Sky
   installed. Completed local checks are linked above; report new
   results back into this project's docs.
3. Verify how `Mothership`'s resource/seed selects its model, then establish
   the active root-to-hangar runtime transform before packaging the already
   passing scratch sphere.
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
├── tools/
│   ├── build_death_star_silhouette_stage3.py (scratch geometry + QA renders)
│   └── verify_exported_scene_mesh.py (direct NMSDK mesh-stream verifier)
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
