# Death Star freighter — toolchain check

## Status
**Steps 1-4 complete, Step 5 partial, Step 6 not started.** Run by Codex
against the real, currently-installed game (see
`TOOLCHAIN-RESULTS-2026-09-25.md` for its raw report; this section is that
report folded into the tracked environment/step state). No game file or
save has been modified.

## Environment
| Item | Value | Status |
|---|---|---|
| Game | No Man's Sky | — |
| Platform | PC / Steam, app id `275850` | VERIFIED (Steam app id is public/static) |
| Installed Steam build | `25441199` — version **Cosmos 7.04**, dated 2026-09-21 | VERIFIED (confirmed locally by Codex, 2026-09-25) |
| Blender | 4.5.14 LTS | **VERIFIED** — launches successfully. Executable SHA-256: `57FA1D294EA76448C3BEC84CA758CAF4629611330ABBA7DCF55BB0C56A0A15AB` |
| PAK unpack tool | HGPAKtool 1.1.3 | **VERIFIED** — extracted a copied `NMSARC.globals.pak` from the current build |
| MBINCompiler | reports version `7.03.2.1` | **VERIFIED** — passed a no-edit round-trip (MBIN → MXML → MBIN → MXML) on `gcscratchpadglobals.global.mbin`; both MXML outputs had identical SHA-256 |
| NMSDK | source on its `cosmos_fixes` branch, commit `548bfe1` (2026-09-16) | **BLOCKED, NOT VERIFIED** — the add-on did not load in Blender: Python could not import its `hgpaktool` dependency. Do not treat NMSDK as usable until this is resolved and the add-on actually loads. |

**Steps 1-4 are complete and evidence-backed** (real hashes, a real
round-trip test — not just "it ran"). **NMSDK is the current blocker**:
nothing that needs the Blender add-on (building the sphere mesh) can start
until it loads.

## Safety — what this checklist does and does not touch
- Nothing here overwrites a game file or a save. Every step either reads
  an existing file or works on a **copy** in a separate working folder.
- Steps 5 and 6 read your unpacked game files and your save file
  respectively. Neither is written to in this checklist. **Do not make
  any save write until a fresh four-file backup exists**, per this
  framework's Rule 14 (saves are sacred) — that backup step comes before
  any future write step, not in this checklist.
- If anything below conflicts with what you actually see on screen, stop
  and report the discrepancy rather than pushing through — that's exactly
  the kind of thing this gate exists to catch.

## Step 1 — confirm the installed game build — DONE (2026-09-25)
Confirmed: **Cosmos 7.04**, Steam build `25441199`, dated 2026-09-21 — a
real patch after the Falcon project's last check (`25351301`,
2026-09-18). Reported by the user from a local check rather than run in
this session (no game access here).

## Step 2 — re-verify (or set up) the portable toolchain — DONE for Blender/MBINCompiler, BLOCKED for NMSDK (2026-09-25)
- **Blender**: VERIFIED. 4.5.14 LTS launches. Hash above.
- **MBINCompiler**: VERIFIED. Reports `7.03.2.1` (note: this is the exact
  version string reported now, distinct from the Falcon project's
  `v7.03.2-pre1` label — record it as its own value, not the same build).
  Round-trip proof passed (see Step 4).
- **NMSDK**: **BLOCKED**. On its `cosmos_fixes` branch, commit `548bfe1`
  (2026-09-16) — this branch name itself suggests the maintainer already
  knows Cosmos needs fixes, which is a good sign the project is being kept
  current, but the add-on still fails to load here: Python cannot import
  its `hgpaktool` dependency. Next action: install `hgpaktool` into
  Blender's own Python environment (not the system Python) and retry
  loading the add-on. This exact remedy is UNVERIFIED — NMSDK's own docs
  for the `cosmos_fixes` branch should be checked for the specific
  dependency-install method it expects before assuming this works.

## Step 3 — pick and confirm a PAK unpack tool — DONE (2026-09-25)
**VERIFIED**: HGPAKtool 1.1.3, confirmed by successfully extracting a
copied `NMSARC.globals.pak` from the current build. (Of the candidates
research surfaced — PSARCTool, HGPAKTool, NMS Modding Station, AMUMSS's
PCBanks Explorer — HGPAKTool is the one that was actually tried and works.)

## Step 4 — prove the toolchain round-trips before trusting it on anything real — DONE, PASS (2026-09-25)
**VERIFIED**: tested on `gcscratchpadglobals.global.mbin`. MBIN → MXML →
MBIN → MXML; the two MXML outputs had identical SHA-256 hashes. The
toolchain (MBINCompiler `7.03.2.1` + HGPAKtool 1.1.3) is proven safe to use
on real files for this build, independent of the still-blocked NMSDK.

## Step 5 — locate the real freighter hull table and geometry files — PARTIAL (2026-09-25)
This is gate 2 from `FEASIBILITY.md`: confirm or correct
the "hull selected by save seed, added via a new table entry" hypothesis
against real files, rather than trusting the secondhand mod description it
was built from.

**Found so far (VERIFIED present, from a read-only filtered extraction):**
freighter-related assets do live under `MODELS/COMMON/SPACECRAFT/`,
including a `BIGGS` path and `COMMONPARTS/HANGARINTERIORPARTS`. The
`HANGARINTERIORPARTS` name is worth noting for the hangar-in-trench design
decision: it suggests the hangar interior may be a shared, modular piece
attached to a socket on the hull rather than baked uniquely into each
hull's own mesh — if so, the thing to locate next is that attach socket's
position, not a hand-measured point on the hull.

**Still not found: the seed→hull lookup table itself.** The "hull selected
by save seed, added via a new table entry" architecture in `FEASIBILITY.md`
**remains HIGH CONFIDENCE, not VERIFIED** — this is the load-bearing gap.
Next pass: search for a table-like file near `BIGGS`/the freighter path
(names to try: anything with `GENERATIONTABLE`, `SPAWNTABLE`, `PARTSTABLE`,
or similar, mirroring how frigate paths were named in earlier research) and
open it to check whether it actually keys hull variants by a seed value.

Original lead, still useful context: research found that **Frigates** (the
small escort ships assigned to a freighter, not the freighter itself) live
under `MODELS/COMMON/SPACECRAFT/FRIGATES/`, e.g.
`COMBATFRIGATELOD4.SCENE.MBIN`, with geometry files generally following
`NAME.GEOMETRY.MBIN.PC` — a different object than `Mothership`'s own hull,
not assumed to mirror it.

## Step 6 — locate `Mothership`'s save record
1. Identify which save file (`save.hg` / `save2.hg`, or their higher-index
   `save*.hg` counterparts if you have multiple slots) and which slot
   contains `Mothership` — do this by name, using whatever save
   reader/editor you already have set up, not by assuming it's in the same
   slot or even the same save folder as the Falcon Corvette project's
   Corvette work.
2. Within that freighter's record, identify the field that looks like a
   generation seed (this is the field Step 5's table lookup will key on).
   Do **not** change it yet — this step is only locating and naming it.

Report: save file name, slot number, and the seed field's name and current
value.

## What to send back
Once you've run as much of this as you can:
- Step 1: build id + exe timestamp
- Step 2: Blender / NMSDK / MBINCompiler versions (+ any fresh hashes)
- Step 3: unpack tool + version + stated compatibility
- Step 4: pass/fail on the round-trip test, and which file was used
- Step 5: real freighter model folder path, file naming pattern, and the
  seed→hull table name if located
- Step 6: `Mothership`'s save file, slot, and seed field name/value

Partial results are fine — each gate that comes back confirmed lets the
next document narrow from "HIGH CONFIDENCE hypothesis" to "VERIFIED", and
any gate that comes back different from what research assumed is exactly
the kind of correction this checklist exists to surface before anything is
built on a wrong assumption.
