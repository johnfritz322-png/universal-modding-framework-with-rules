# Where the functional parts actually sit inside the Falcon

Read from the live save on 2026-09-19, slot 7, 1,495 objects, 83 distinct part types.
Coordinates are the build grid's own units, as stored in `wMC`.

| Part | Id | Position (x, y, z) | What it is |
|---|---|---|---|
| Cockpit | `^B_COK_A` | (-18.00, 3.00, 9.00) | where you fly from |
| Airlock | `^B_ALK_Z_A` | (0.00, 3.00, -3.00) | 21.63 units from the cockpit |
| Airlock | `^B_ALK_C` | (0.00, 3.00, -6.00) | 23.43 units from the cockpit |
| Habitation | `^B_HAB1_C` | (0.00, 0.00, 0.00) | the large walkable room, at the origin |
| Turret | `^B_TUR_C` | (0.00, 6.00, 0.00) | directly above the hab |
| Generator | `^B_GEN_1` | (6.00, 3.00, -6.00) | |
| Save point | `^BUILDSAVE` | (-3.68, 3.23, -7.44) | |
| Archive | `^ARCHIVE` | (-10.28, 3.23, 7.89) and (1.43, 5.33) | two of them |

## There is no teleporter in this ship — VERIFIED

All 83 part types were listed and none contains TELE, PORT, BEAM or WARP. The ship's
installed technology list (`@Cs[7]/;l5/:No`) is empty. So whatever the player uses to
reach their other ship, it is **not a placed object in this build** — it is either a
built-in function of the Corvette itself or one of the airlocks.

This matters because a previous session tried to *add* a teleporter, placed it 1.73
units in front of the inner airlock, and had to roll the whole build back. See
`OUTCOME-AND-LESSONS.md`.

## The walk is real

The cockpit is at one end and both airlocks are at the other, 21 to 23 units away,
through a 1,495-part interior. A request to "move the teleporter closer to the
cockpit" is most likely about that walk.

## The standing rule still applies

`OUTCOME-AND-LESSONS.md` concluded: **do not edit a Corvette interior by writing save
files.** Three attempts, three failures, each invisible until the game was launched,
and one of the three was placing something near an airlock. Interior changes belong in
the in-game Corvette build menu, which shows collision and refuses invalid placements.

The clearance rule to respect either way: nothing within 4 units of an airlock, and
nothing in the airlock's `At` direction, which is the way the door opens. Both
airlocks here have `At` = (0, 0, 1).
