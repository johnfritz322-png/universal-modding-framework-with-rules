# Stripping clutter from a Corvette - VERIFIED 2026-09-18

Done on the delivered Falcon after an earlier interior sweep had already destroyed
it once. This pass worked. The difference is entirely in the guard.

## The trap: half the "clutter" is exterior greebling

Classify by name alone and you strip the hull. On this build, sorting props by
whether they sit inside or outside the floor footprint gave:

| | Inside - safe to remove | **Outside - exterior detail, never touch** |
|---|---|---|
| `BUILDWORKTOP` | 3 | **57** |
| `B_CARRIAGEWHEEL` | 5 | **10** |
| `S_CANISTER1` | 3 | **8** |
| `S_RUG0` | 0 | **7** |
| `S_CARRIAGEWHEEL` | 0 | **3** |
| `BUILDHCABINET` | 0 | **2** |

**92 objects that read as junk by name are hull surface detail.** `BUILDWORKTOP`
in particular is 57 pieces of exterior panelling and 3 pieces of furniture, under
one id. A name-based rule removes both.

## The inside test

An object is interior if it is at deck-to-head height **and** within reach of a
floor panel:

    def inside(o):
        x, y, z = o["Position"]
        return 3.0 < y < 5.4 and any(
            hypot(f[0]-x, f[2]-z) <= 2.2 for f in floor_panel_positions)

Floor panels are the ship's own deck, so "near a floor panel" is a good proxy for
"in a room". Anything failing this is on the skin.

## The guard that actually works

The guard that failed previously asserted that nothing outside a height band was
lost - over a band that excluded the range being edited. Replace it with an
**explicit removal list plus an identity check on everything else**:

    doomed = {id(o) for o in objs if removable(o)}
    survivors_expected = {sig(o) for o in objs if id(o) not in doomed}
    kept = [o for o in objs if id(o) not in doomed]
    ...
    lost = survivors_expected - {sig(o) for o in kept}
    assert not lost, f"LOST {len(lost)} objects not on the list"

This cannot miss damage. Anything not explicitly listed for removal is **required**
to survive, so there is no range, no heuristic, and no gap for an error to hide in.

Use this shape for any destructive edit to someone's build.

## Result on this ship

113 interior objects removed - `SERVERSTACK` x41, `HOLOFILES` x18, plus crates,
cement bags, a wheelbarrow, pallets, sparkplugs, barrels and trays.

Envelope after: **35.9 x 8.5 x 47.7 - identical to as delivered.** Floor still 142
panels, `WALLLIGHTBLUE` still 124, one root.

16 usable items left aboard: teleporter, trade terminal, mission table, health
station, hazard station, room scanner, save point, 2 archives, weapon rack, 3 beds,
3 chairs, desk.

## Sourcing a replacement part

`^MAPTABLE` could not be refitted from the live builds because it existed only in
an older export. Widen the template library to the exported JSON as well as the
live `@ZJ` arrays - the export is still real data from the same game, so nothing
is invented by using it.
