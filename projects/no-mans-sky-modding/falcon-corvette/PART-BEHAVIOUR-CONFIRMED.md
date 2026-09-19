# Corvette part behaviour - CONFIRMED BY IN-GAME TEST 2026-09-18

The user installed a 293-part Falcon into slot 7, launched the game, and looked at
it. Two findings come from that test and are therefore observations, not inference.

## 1. `^B_STR_*` structural parts render as an OPEN FRAME, not solid plating

User's words: *"it looks like a frame not solid"*.

The whole hull was built from `^B_STR_S_N` / `^B_STR_K_NE` / `^B_STR_K_NW`. In game
it reads as scaffolding. **Structural parts are a skeleton, not a skin.** Do not use
them for a surface that is meant to look solid.

This also explains the earlier `Falcon Courier` failure differently than assumed:
it was not only that wings are thin fins, it is that the entire `B_STR` family is
see-through.

## 2. Core parts left in the boarding path trap the player

User's words: *"i can't use the door it doesn't open when i hit the button the rear
hatch closes over me"*.

Copying Darth Fritz's core verbatim placed **nine objects inside the walk-in route
to the airlock**, including `^B_SHL_E` at `(0, 7.5, -9)` sitting directly on top of
the airlock at `(0, 3, -9)`, plus `^B_GEN_1`, `^B_TRU_F`, `^B_DECO_J` and four wing
parts.

On the small stock Corvette that cluster is harmless because the ship is open. Once
a large hull is built around it, those parts seal the entrance.

**Rule: after composing a build, assert that the volume between the hull edge and
the airlock contains nothing but the airlock itself.** Pin only
`^U_PARAGON`, `^B_ALK_A`, `^B_LND_B` and `^B_HAB_B` to their original positions;
everything else in the core is safe to relocate.

## 3. Measured part footprints

Nearest-neighbour pitch of each part across the user's 2,882-object Corvette-1
build. Parts whose `Up` vector is unit length are unscaled, so the pitch is the
real footprint.

| Part | Copies | Pitch | Up | Note |
|---|---|---|---|---|
| `^M_FLOOR` | 379 | **3.33** | unit (319/379) | solid panel; tiling at 3.0 overlaps slightly, no gaps |
| `^C_FLOOR` | 172 | **5.33** | unit | larger solid panel |
| `^B_WALL` | 64 | **5.33** | unit (31/64) | solid wall |
| `^BUILDFLATPANEL` | 893 | **3.00** | 61 distinct, non-unit | flat plating, but scaled - see below |
| `^B_CHEV_WIN2` | 44 | ~3.33 | mixed | window panel |

## 4. Non-unit `Up` vectors carry SCALE - HIGH CONFIDENCE, not yet confirmed

`^BUILDFLATPANEL` has 61 distinct `Up` vectors in one build, with magnitudes from
0.58 to ~3.0, while `At` stays unit length. `^B_WALL_CARG5` on Darth Fritz has
`Up = [0, 0.25, 0]`; `^STORAGEPANEL` has `Up = [0, -2.95, 0]`.

A magnitude of 1.0 appears on every part placed at its natural size. The reading
that `|Up|` is a uniform scale factor fits every observation so far, and it matches
`^BUILDFLATPANEL`'s dominant 3.0 pitch appearing alongside 3.0-magnitude `Up`
vectors. It has **not** been confirmed in game, so prefer unit-`Up` parts whose
footprint is measured until it is.

## What was installed after these findings

572 parts. Frame kept as internal structure at y 3 and 6, with solid `^M_FLOOR`
skins at y 1.5 and 9.0 above and below it, and `^B_WALL` closing the rim. The nine
blocking core parts were relocated onto the hull flanks at y 10.5 as surface detail.

Still unconfirmed: whether the `^M_FLOOR` skin reads as solid plating from outside,
and whether the airlock now opens.

---

# 5. The airlock needs clearance on the INSIDE - CONFIRMED 2026-09-18

Second in-game test. User: *"i can't access the door at all something is blocking
it"*, with a screenshot of the airlock sealed and showing **two red indicator
lights**. Red on a Corvette door means obstructed.

## Cause

`^B_ALK_A` on Darth Fritz sits at `(0, 3, -9)` with `At = [0, 0, 1]`. **`At` is the
facing direction, so the door opens toward +Z - into the ship, not out of it.**

The first fix only cleared the *approach* (z from -21 to -9, outside the door). The
side the door actually opens into was packed solid. Inspection found
`^B_STR_S_N` at `(0, 3, -6)`: three units directly in front of the door at exactly
door height.

Clearing the outside approach is therefore necessary but **not sufficient**. Both
sides of an airlock need clearance, and which side is "inside" is given by `At`.

## Second, larger cause

The hab core `^B_HAB_B` at `(0, 3, -3)` is a large walkable room - measured minimum
gap between habs elsewhere is 14.5 units. The hull generator had been filling every
cell of the ship's footprint at four heights, so the hab's interior was packed with
floor panels and frame. The ship was a solid brick with a room's worth of geometry
jammed through it.

**Rule: a Corvette hull must be generated as a shell with a hollow interior.** Keep
the roof so it still reads solid from above, and void everything below it inside the
hab volume and the corridor.

## The test that catches this

Rather than guessing at clearances, assert that the volume the player walks through
contains **only objects the working ship also has at those same coordinates**:

```
player volume = (corridor OR hab footprint) AND 0 < y < roof height
every object in it must match (ObjectID, position) on the known-good Corvette
```

On the current build that volume holds 23 objects and all 23 are Darth Fritz's own,
at Darth Fritz's own coordinates. Roof panels and the under-belly turret are
correctly excluded by the `0 < y < roof` bound - an early version of the check
included them and produced 59 false positives.

## Also corrected

Relocation of blocking core parts must key off the **corridor only**, never the hab.
Keying it off the whole cleared footprint threw the ship's own interior furniture -
kitchen, tech walls, cargo panels - out onto the roof.

## Status: FIX CONFIRMED 2026-09-18

User: *"the door opens now"*. Hollowing the hull and clearing the inside face of
the airlock resolved it. The assertion above is the regression test.

---

# 6. Moving the cockpit strands it - CONFIRMED 2026-09-18

Same test: *"NOW I CAN'T ACCESS THE COCKPIT"*.

`^B_COK_D` had been relocated from its stock `(0, 3, 3)` out to a starboard pod at
`(24, 3, 3)`. The pod was built from hull tiles with no walkable route from the hab,
so the cockpit was unreachable.

**Rule: treat the cockpit like the airlock - it is only reachable if it sits inside
the hollow interior.** Leave it at its stock position and put a second, purely
decorative `^B_COK_D` wherever the silhouette needs a canopy. Two cockpits in one
build is valid: Corvette-1 shipped with two.

# 7. Fine placement and free rotation ARE available

Measured in Corvette-1, so these are real placements the game accepted:

| Part | Copies | Pitch | Rotations seen |
|---|---|---|---|
| `^C_TRIFLOOR_Q` | 32 | **1.54** | 5 distinct `At`, including 60 and 120 degrees |
| `^M_FLOOR_Q` | 28 | ~0.94 | includes `(0, -0.7, -0.7)`, a 45 degree tilt |
| `^M_WALL_Q` | 17 | 5.33 | 6 distinct |
| `^M_ARCH` | 20 | 3.77 | 4 distinct |

So a Corvette is **not** restricted to the 3.0 structural grid or to axis-aligned
placement. Curved and sloped surfaces can be built by stepping a quarter-floor
around an arc with its `At` set to the local tangent. The current build uses 210
`^C_TRIFLOOR_Q` at 3-degree steps around the hull edge.

There are 171 distinct part IDs proven valid in this save, drawn from both
Corvettes - including base-building parts, so the palette is not Corvette-only.

## Hard ceiling worth recording

A save edit can only place geometry the game already ships. However finely it is
placed, the result is an assembly of NMS parts, not an arbitrary mesh. Matching a
specific real-world silhouette exactly requires a custom model shipped in a `.pak`,
which is a different piece of work with its own risk: replacing a shared part's mesh
changes every ship that uses it.
