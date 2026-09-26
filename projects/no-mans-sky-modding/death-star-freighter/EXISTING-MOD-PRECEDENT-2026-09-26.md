# Existing shipped-mod precedent for custom capital-freighter hulls

Recorded 2026-09-26 from this cloud session, via `WebSearch` only. This
session has no No Man's Sky install, Nexus Mods account, or ability to
download/open the mod archives below. Everything here is **HIGH
CONFIDENCE**, not VERIFIED — it is a secondhand summary of Nexus Mods /
Allmods.net page descriptions, not an inspection of the mods' actual
`.pak`/MBIN contents. Treat it as a lead for the local session to check
against real files, not as a substitute for that check.

## Why this matters

`WHATS-NEXT.md` and `BLENDER-ROUNDTRIP-2026-09-25.md` both name two open
gates: (1) whether an additive hull-table + seed-selection architecture is
real and reachable, and (2) how the hangar opening should be built/attached.
A shipped mod claiming to do exactly this on the exact same file this
project already found is a strong precedent worth checking before designing
either mechanism from scratch — per this framework's rule 5 (prefer
established systems) and rule 3 (research before architecture).

## What was found

**gFreighter Custom Freighters** (Nexus Mods mod ID `2200`,
[nexusmods.com/nomanssky/mods/2200](https://www.nexusmods.com/nomanssky/mods/2200)):
adds several new capital freighter models **without replacing** existing
vanilla freighters — both old and new freighters can still be encountered.
Its listed affected files are:

- `CAPITALFREIGHTER_PROC.SCENE.MBIN` — **this is the exact same resource
  file** this project's own save read (`SAVE-READONLY-FINDINGS-2026-09-25.md`)
  found on Mothership's live save record, and the same file
  `FREIGHTER-SELECTION-FINDINGS.md` already decompiled and inspected.
- `HULL_A_CUSTOM.SCENE.MBIN` — a plausible sibling to the `_HULL_A1` /
  `_HULL_A2` branches already found nested under `_HULL_A3` in the
  decompiled descriptor. Not confirmed as the same tree; the naming
  similarity is suggestive, not proof.
- `HANGARA_EXTERIOR.SCENE.MBIN` — a **separate, apparently modular** hangar
  scene file. This lines up with the earlier `HANGARINTERIORPARTS` hint
  that the hangar may be a shared/attached piece rather than baked into
  each hull, and would materially change the open hangar-opening gate: if
  true, the hangar may not need to be carved into the new sphere mesh at
  all, but referenced/attached at the existing `HANGARROOTA`/`HANGARROOTB`
  locators instead.

A related page (**gFleet Custom Freighters Unified**,
[allmods.net/no-mans-sky-mods/vehicles/gfleet-custom-freighters-unified](https://allmods.net/no-mans-sky-mods/vehicles/gfleet-custom-freighters-unified/))
and a search-engine summary describe a seed-to-model list: loading a save
editor and setting a capital freighter's seed to one of the mod's listed
values selects one of its added custom hulls, including entries labelled
(verbatim from the summary) `SW Harrower (0x1)`, `SW Venator (0x27)`,
`SW Executor (0x1E)`, `SW Imperial II (0x5)`, among other non-Star-Wars
entries. **This was not read from a primary source** — it is a search
summary of a mod-list page, and the grouping label `"384c Freighters"` in
that summary is unexplained and must not be assumed to mean anything
specific (e.g. a literal internal ID) without checking the mod itself.

Taken together, if accurate, this would mean: (a) the additive hull-table
architecture this project has labelled UNVERIFIED is not just plausible but
already shipped and working on some prior game build, and (b) other authors
have already solved Star-Wars-capital-ship silhouettes (including a
Venator, the same wedge family as `Mothership`'s stock hull) on this exact
mechanism.

## What this does not establish

- Not confirmed against the actual mod archive — file names above come from
  a Nexus Mods page description, not from opening the `.pak`/MBIN inside it.
- Not confirmed compatible with the current Cosmos 7.04 build (`25441199`);
  these mods may predate it and could be stale, exactly the kind of
  assumption this project's own `TOOLCHAIN-RESULTS-2026-09-25.md` correction
  warned against.
- Does not establish that the same mechanism can be scoped to a single
  owned freighter only, isolated from other players'/NPCs' freighters, or
  that it survives this project's boardability/regression test bar.

## Recommended next step (local machine only)

Download `gFreighter Custom Freighters` (mod 2200) and, if accessible,
`gFleet Custom Freighters Unified` from Nexus Mods, and open their `.pak`
contents read-only (same HGPAKtool/MBINCompiler toolchain already verified
in this project). Specifically check:

1. Does `HULL_A_CUSTOM.SCENE.MBIN` (or an equivalent) sit as a sibling
   under the same `_HULL_A3` descriptor node this project already found in
   `CAPITALFREIGHTER_PROC.DESCRIPTOR.MBIN`?
2. What literal seed value(s) does the mod's own table associate with its
   added hull(s), and where is that mapping actually stored (which MBIN,
   which field)? This directly answers the outstanding "seed→hull lookup
   table" question in `FREIGHTER-SELECTION-FINDINGS.md`.
3. Does `HANGARA_EXTERIOR.SCENE.MBIN` reference or attach at
   `HANGARROOTA`/`HANGARROOTB`, or an equivalent locator? If so, the hangar
   gate may be "reference the existing exterior scene," not "cut and build
   a new opening."

This is scratch/read-only investigation, same as prior gates — no game
file, save, or mod install required to do this check.
