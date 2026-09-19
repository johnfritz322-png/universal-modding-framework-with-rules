# The Corvette build grid — VERIFIED 2026-09-18

Derived by reading the exterior objects of **Darth Fritz**, the user's active,
in-game, flyable Corvette (base record 29, ship slot 8, 163 objects). This is a
working ship, so its coordinates are ground truth, not inference.

## The grid is 3.0 units

Every structural and exterior part sits on a multiple of **3.0** on all three axes.

Observed occupied coordinates on Darth Fritz:

- X: `-6, -3, 0, 3, 6`
- Y: `0, 3, 6, 9` for core modules
- Z: `-15, -12, -9, -6, -3, 0, 3`

## Half-step at 1.5 on Y for hung parts

Wings, shields, trusses and some decor sit on a **1.5 offset** in Y — `4.5` and
`7.5` — i.e. they hang between full cells rather than occupying one:

- `^B_WNG_P` / `^B_WNG_P_R` at Y `7.5`
- `^B_WNG_Q` / `^B_WNG_Q_R`, `^B_WNG_R` / `^B_WNG_R_R` at Y `4.5`
- `^B_SHL_E`, `^B_TRU_F` at Y `7.5`
- `^B_DECO_Q_0` at Y `7.5`

Interior wall parts (`^B_WALL_*`) are the exception — they sit at arbitrary
fractional positions and are placed freely, not snapped.

## Axis meaning

**+Z is forward.** The cockpit is the most positive Z, the engine end the most
negative:

| Part | Position | Role |
|---|---|---|
| `^B_COK_D` | `0, 3, +3` | cockpit, front |
| `^B_TUR_E` | `0, 3, 0` | turret |
| `^B_HAB_B` | `0, 3, -3` | hab core |
| `^B_LND_B` | `0, 0, -6` | landing gear, sits at Y 0 |
| `^B_ALK_A` | `0, 3, -9` | airlock — **the boarding entrance** |
| `^B_GEN_1` | `0, 6, -12` | generator |
| `^B_TRU_F` | `0, 7.5, -15` | truss, rear-most |

**Y is up**, and Y `0` is the ground plane where landing gear sits.

**X is lateral**, symmetric about `0`.

## Orientation vectors

Default facing is `wJ0` (Up) = `[0, 1, 0]` and `aNu` (At) = `[0, 0, 1]`.

A part rotated 90° about Y has At = `[1, 0, 0]` — seen on `^B_WALL_CARG2` and
`^B_WALL_CARG4`. So rotation is expressed by changing the At vector, not by an
Euler angle field.

## `^U_PARAGON` is the root

Every Corvette build — Darth Fritz and Falcon Courier both — has exactly one
`^U_PARAGON` at position `0, 0, 0`. It is the first object in the array and must be
preserved.

## What this unlocks

A Falcon can now be laid out on paper in real coordinates before a single byte is
written: a 3.0-unit cell grid, +Z forward, Y 0 as the ground, the cockpit offset to
one side in X, the airlock kept clear, and wings/dishes hung on the 1.5 half-step.

## Still NOT verified

The *footprint and shape* of each individual `structural_*` tile. The grid spacing is
now certain; which tile fills which cell shape is not. Darth Fritz only uses four
structural pieces (`^B_STR_H_S`, `^B_STR_K_NE`, `^B_STR_K_NW`, `^B_STR_S_N`), which
is too small a sample to infer the whole 139-tile set.
