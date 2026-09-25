# Death Star freighter — feasibility and architecture

## Status
**Researched only.** Nothing installed, injected, compiled, or run. This
session has no No Man's Sky install, no Blender, and no unpacked game files
— it is a documentation/planning environment. Every hands-on step below
(unpacking, NMSDK, MBINCompiler, save editing) has to happen on the user's
own machine, the same way the Falcon Corvette project's toolchain work did
(see `../falcon-corvette/TOOLCHAIN-CHECK-2026-09-18.md`).

## Scope of this document
This document covers **verified/researched technical capability only** —
what the game and its modding tools can actually do. It deliberately does
**not** cover what the mod should look like: that is design intent, tracked
separately in `DEATH-STAR-BUILD-BRIEF.md` (sphere silhouette, dish/trench
placement, surface treatment). Keeping the two apart matters because a
design goal being desirable says nothing about whether the engine supports
it — see this framework's `AGENTS.md` rule 4 ("player-facing goals are not
proof of technical feasibility").

Every conclusion below is labelled one of:
- **VERIFIED** — confirmed against primary evidence (the user's own
  screenshots, this repo's own prior toolchain work, or a directly read
  primary source).
- **HIGH CONFIDENCE** — a `WebSearch` summary of a known-working example
  (an existing shipped mod, a wiki page), not independently re-fetched or
  tested in this session.
- **UNVERIFIED** — a working hypothesis only, not checked against real
  files or tested.
- **NEEDS TESTING** — the mechanism is plausible/designed but has no
  evidence yet either way; only a real test on the user's machine resolves
  it.

## What this is not
This is **not** the same problem as the Falcon Corvette. Corvettes can be
assembled part-by-part directly in a save's `Objects[]` layout (in-game
building, or a save-editor injection of that layout). Freighters cannot:
there is no player-facing freighter hull editor. The 2022 Endurance update
added deeper freighter *base* (interior) building, exterior platforms, and
capital-ship *engine recoloring* from the existing freighter paint UI — none
of that reaches hull shape (**HIGH CONFIDENCE**, from web search of the
Endurance update's own patch notes summary; not independently re-fetched,
see Sources). A new hull silhouette is only reachable by replacing/adding a
freighter exterior model asset, which is exterior-mod territory (NMSDK +
MBINCompiler), not save-editing territory.

## Donor chassis
No stock freighter hull is spherical. The two capital-freighter families
found in research are:
- **Venator-family**: wedge-shaped, Star-Destroyer-like silhouette.
- **Sentinel-Design family**: rounder, segmented capital hulls, classed by
  midsection segment count (Sentinel / Battleship / Dreadnought).

**VERIFIED from the user's own screenshot (2026-09-25, see
`PROJECT_MANIFEST.md` → "Target freighter")**: the actual donor, `Mothership`,
is a Venator-family wedge hull — the harder-shaped one of the two to hide
under a sphere, since it is long, flat, and has an angular bow rather than
already being roundish. Confirms rather than assumes the point below.

Neither family is close enough to a sphere to reskin by texture alone. This
confirms the same conclusion the Falcon brief reached for the Corvette: the
Death Star hull has to be a **fully custom NMSDK mesh**, built as an
exterior shell, not a retexture of an existing part. The stock freighter's
bridge, hangar, interior, NPCs, and base-building attach points stay the
untouched functional core underneath that shell — this is what keeps the
freighter's existing gameplay working and is the direct analogue of the
Corvette brief's "boardability rule."

## How freighter hull selection actually works (the important finding)
Research into an existing, actively maintained mod (**gFreighter — Custom
Freighters**, Nexus Mods) describes its mechanism directly: it **adds** new
capital freighter hull models without overwriting any vanilla hull, and a
player selects one of the added hulls by setting their freighter's
procedural **seed** value (via a save editor) to one of the seed values the
mod documents for each added model. Several of gFreighter's shipped hulls
are themselves other-franchise reskins (its list includes Star Wars
Harrower, Venator, Executor, and Imperial II entries), which is direct
precedent that this exact category of mod — franchise-styled capital hull,
selected by seed — already works in the current game version's modding
ecosystem.

**Label: HIGH CONFIDENCE**, not VERIFIED — this description comes from
secondhand summaries of the mod's Nexus page (the domain is blocked by this
sandbox's egress proxy, so the page itself was not read directly here), and
no exact MBIN table name or save-JSON field name was confirmed against real
files or an authoritative modding reference in this session. Treat "seed"
as the working hypothesis for the selection mechanism, to be confirmed
against the user's own unpacked game files before anything is built on it,
per Rule 1 (do not invent file schemas or fields).

### Candidate architecture — pending verification
If gates 2 and 3 confirm the table and seed mechanism, this is the smallest
compatible change available (Rule 6):
- add one new hull entry to the confirmed freighter model table — no vanilla
  table row is overwritten;
- change only the confirmed hull-selection field in the target freighter's
  save, rather than injecting a full `Objects[]` layout as the Corvette work
  required;
- leave class (C/B/A/S), stats, name, and crew untouched.

Until those gates pass, this is a **HIGH CONFIDENCE candidate architecture**,
not an established implementation path.

## Getting to S-class — resolved: reuse the existing freighter, touch nothing but the hull
**Decision (2026-09-25): the target is the user's own already-owned S-class
freighter.** This removes the class/stat question entirely rather than
choosing between the two paths below — no class field, hyperdrive tier, or
any other stat is touched by this mod at all. The only planned save write
is the one field this project already needed: that freighter's hull-seed
value, changed to select the added Death Star hull entry. Class, stats,
name, and crew stay exactly as they already are.

This is a strictly smaller change than either alternative previously
considered:
1. ~~Legitimate in-game grind~~ — unnecessary, no new freighter is being
   acquired.
2. ~~Save-edit the class field~~ — unnecessary, and it drops the stat-block
   caveat that path carried (editing only the class letter risks a
   cosmetic-only S-class). Not touching the class field at all avoids that
   risk outright.

**Still needed from the user before gate 3 below can be done:** which save
slot/freighter this is (name and slot number), the same way the sibling
Falcon Corvette project tracks its target as "slot 7" and its
never-touch freighter as "Darth Fritz in slot 8". Nothing here assumes an
identity for it yet.

## Toolchain reuse
The Falcon Corvette project already hash-verified a working local toolchain
on 2026-09-18 (Blender 4.5.14, NMSDK cloned from
`github.com/monkeyman192/NMSDK`, MBINCompiler `v7.03.2-pre1`) against Steam
build `25351301`. That toolchain is the right starting point here too, but
it is **not** carried over as verified for this project: the framework's own
prior write-up already labels the version match as an inference, not proof,
and time has passed since then. Re-confirming it is the first gate below.

## Required research/verification gates before any implementation
In the order the framework's workflow requires (research → architecture →
minimal baseline → one testable feature):

1. Re-run the installed-build check and confirm MBINCompiler still
   compiles/decompiles a copied asset on the current build (mirrors
   `../falcon-corvette/TOOLCHAIN-CHECK-2026-09-18.md`, but must be redone —
   do not assume the 2026-09-18 result still holds).
2. On the user's own unpacked game files, locate and confirm the actual
   freighter hull/model table MBIN and the real seed-to-hull selection
   mechanism. The "seed" hypothesis above must be confirmed this way, not
   carried over from a secondhand mod description.
3. Confirm the exact save-data field for a freighter's hull selection and
   identify the target save/slot — the same
   backup-before-touching discipline the Falcon handoff already established
   (see `../falcon-corvette/HANDOFF-2026-09-18.md`) applies here unchanged:
   never touch a save without a fresh four-file backup first.
4. Build the sphere mesh in Blender/NMSDK and locally inspect it (geometry,
   UVs at the poles, normals, materials) before any packaging step.
5. Package as an **additive** mod (new table entry only, no vanilla file
   overwrite), matching gFreighter's own precedent, and keep collision-free
   per NMSDK's own guidance unless a gate proves collision is required.
6. Back up saves and the `MODS` folder, install only with the game closed,
   then run the boardability test (summon/dock, walk the interior, exit,
   save, reload, repeat) before this is ever called usable.

No claim of a compiling, loading, or in-game-tested build is made anywhere
in this document.

## Sources
- No in-game freighter hull editor / Endurance update scope (recoloring,
  base building, not hull shape): web search summary of the Endurance
  update's own page and community discussion. Not independently re-fetched
  — `nomanssky.com`/`nomanssky.fandom.com`/`nomanssky.miraheze.org` are all
  blocked by this sandbox's egress proxy.
- Capital freighter family/class naming (Venator vs. Sentinel-Design,
  segment-count classes): web search summary of community wiki content
  (same blocked domains as above), cross-checked against a second,
  independent search pass with consistent results.
- gFreighter mod mechanism (additive hulls, seed-based selection, Star Wars
  hull examples already shipped): web search summary of its Nexus Mods
  listing page. `nexusmods.com` is blocked by this sandbox's egress proxy,
  so the page was not read directly.
- S-class rescue-event odds and save-edit class-field caveat: web search
  summary of community guides (nomansskyrecipes.com and Steam Community
  discussion threads).
- General MBINCompiler/NMSDK unpack-decompile-edit-recompile-repack
  workflow: web search summary, consistent with the workflow already
  recorded in `../falcon-corvette/TOOLCHAIN-CHECK-2026-09-18.md`.

All of the above are labelled **HIGH CONFIDENCE** rather than **VERIFIED**:
this session's `WebFetch` tool is blocked for every NMS-modding-relevant
domain tried (`nomanssky.fandom.com`, `nomanssky.miraheze.org`,
`nomansskyresources.com`, `nexusmods.com`, `monkeyman192.github.io`,
`starwars.com`), so every fact above comes from `WebSearch`'s synthesized
summaries rather than a primary document read in full. Re-verify against
primary sources or the user's own game files before treating any of it as
load-bearing.
