# S-Class Death Star Freighter — build brief

## Status
**DESIGN / RESEARCH.** Nothing built, compiled, or installed. No game file or
save touched. See `FREIGHTER-MODDING-FEASIBILITY.md` for the technical gate
list this brief depends on, and `PROJECT_MANIFEST.md` for the tracked state.

A visual concept reference for this brief (silhouette schematic, the five
non-negotiables, and how the sphere envelope has to fit around
`Mothership`'s confirmed wedge hull) is published at
<https://claude.ai/artifact/HXVQFaWVzMVHtzaxj68zEH>. It is a schematic, not
a render — proportions and placement rules only, nothing traced from real
game geometry.

## Player-facing goal
Replace the exterior of one capital freighter (target: an S-class freighter)
with an original, Death-Star-styled spherical battle-station hull, while
keeping the freighter fully functional: hangar, bridge, NPCs, teleporters,
and freighter base building all continue to work exactly as on a stock
freighter.

## Visual identity: the non-negotiables

A capital ship silhouette in NMS is judged from a distance long before
surface greebling is visible, the same standard the Falcon Corvette brief
used. For the Death Star:

1. **Near-perfect sphere.** Every stock NMS freighter hull (Venator-family
   wedges, Sentinel-family segmented capitals) is elongated. A sphere is the
   single biggest silhouette break from anything in the base game and is the
   feature that must read correctly first. Do not let the hull drift toward
   an ellipsoid or a flattened disc.
2. **One offset superlaser dish.** A large, circular, *concave* (crater-like,
   not domed) dish set into the surface in one hemisphere, clearly off the
   equator and off the sphere's pole — never centered, never convex. This is
   the single most common mistake in fan reproductions and the brief
   explicitly forbids it.
3. **A continuous equatorial trench.** A shallow circumferential canyon
   running the full circumference at the hull's midline, with denser
   greeble/vent detail inside it than on the open hull plating. It visually
   splits the sphere into northern/southern hemispheres without breaking the
   silhouette.
4. **Dense uniform surface paneling.** A fine grid of small rectangular
   panels covers the whole sphere — this is what makes a plain sphere read
   as "Death Star" rather than "moon" or "planet" at range. Panel density
   should be roughly even; avoid large blank stretches of hull.
5. **No forward/aft asymmetry.** Unlike the Falcon, this is a station, not a
   ship with a nose. Orientation is set only by where the stock hangar mouth
   and freighter base entry point already sit on the donor freighter core —
   the sphere must not impose a "front" the way the Falcon's mandibles did.

## Scale approach

The first Death Star's canonical diameter is commonly cited at 120 km, with
the superlaser dish well around 35 km across (**HIGH CONFIDENCE** — multiple
secondary aggregations agree, including Wookieepedia and ST-v-SW.net; not
independently re-fetched from starwars.com in this session because the
sandbox's network egress proxy blocks that domain, see Sources below). That
scale is meaningless against a playable NMS freighter. Preserve **proportion**,
not absolute size:
- dish diameter ≈ 0.29 of hull diameter (35/120), placed off-centre in one
  hemisphere;
- trench width stays thin relative to hull diameter — a hairline groove, not
  a wide gap;
- overall hull size matches the stock freighter's existing bounding volume
  so the hangar mouth, docking approach, and freighter base attach points
  line up without rescaling the functional core.

### Hull envelope rule
`Mothership`'s confirmed donor hull (see `PROJECT_MANIFEST.md` → "Target
freighter") is an elongated Venator-family wedge, not a rounder shape — a
sphere cannot hug it, only enclose it. The rule: **sphere diameter equals
the stock hull's full length**, its largest dimension, so nothing pokes
through the shell at bow or stern. Where the dish and trench land relative
to the stock hangar mouth is a placement choice that still depends on
knowing exactly where that hangar mouth sits on the real hull — an open
item, tracked as gate 5/6 in `FREIGHTER-MODDING-FEASIBILITY.md` and
`TOOLCHAIN-CHECK.md`, not assumed here.

## Boardability rule (same discipline as the Falcon Corvette project)

The exterior is a shell around an **untouched, stock, functional freighter
core**. There may be no custom collision or visible mesh across:
- the stock hangar mouth / landing approach;
- the bridge and any interior teleporter volumes;
- any docking/base-building attach points on the hull.

The Falcon Corvette project's prior failure mode — a shipped build that was
never confirmed boardable — is the standard this project must not repeat.
The first in-game test is not a flyover: summon or warp to the freighter,
dock, walk its stock interior, exit, save, reload, and repeat before this is
ever called usable. See `FREIGHTER-MODDING-FEASIBILITY.md` for why a
freighter mod's risk surface is actually smaller than the Corvette's (an
added hull entry plus one save field, not a full interior part injection).

## Surface treatment

- Base: neutral-to-cool gunmetal gray, uniform enough to read as station
  armor rather than a weathered small ship.
- Panels: shallow raised/recessed rectangular plating, laid out in a loose
  grid that follows the sphere's curvature rather than a flat UV tile (a
  flat tile will visibly distort at the poles).
- Trench and dish interior: darker charcoal, denser greebles, sparse warm
  lighting accents only inside the dish well — the goal is a dark
  crater-like coldness, not the corvette brief's engine-strip blue glow.
- Geometry budget: low/medium-poly panel greebling with normal/detail maps
  for fine surface texture, matching the Falcon project's stated approach.
  No replacement collision mesh unless a later gate proves one is required;
  prefer none, per NMSDK's own guidance that mesh collision is expensive.

## Legal and scope guardrail

This is a private, fan-made visual replica using new, original geometry and
textures based on the public design description below — no Lucasfilm/Disney
model, texture, or another modder's packaged files are to be copied or
redistributed. Search turned up a "Death Star Capital Freighter" mod that
previously existed on Nexus Mods and was later deleted/removed by its
author; that mod's files are not a source for this project and must not be
downloaded, reused, or referenced beyond the fact that one existed.

## Sources

- Death Star diameter/dish/trench figures: aggregated from Wookieepedia
  (`starwars.fandom.com/wiki/Death_Star/Legends`) and ST-v-SW.net's Death
  Star size comparison page, both surfaced via web search; **not**
  independently re-fetched here because this sandbox's egress proxy blocks
  both `starwars.fandom.com` and `www.starwars.com`. Label: **HIGH
  CONFIDENCE**, not VERIFIED — re-fetch from starwars.com's own databank on
  a machine with unrestricted access before treating exact figures as load
  bearing (the game silhouette only needs the *ratios*, not the literal
  kilometer values, so this does not block design work).
- NMS freighter hull family structure (Venator vs. Sentinel-Design,
  segment-count naming) and the existence of a prior "Death Star Capital
  Freighter" Nexus mod (deleted): web search summaries of Nexus Mods listing
  pages, not independently re-fetched (`nexusmods.com` is also blocked by
  this sandbox's egress proxy). Label: **HIGH CONFIDENCE**.
