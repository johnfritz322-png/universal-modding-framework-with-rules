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
