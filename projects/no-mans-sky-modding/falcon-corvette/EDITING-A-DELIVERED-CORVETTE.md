# Editing a Corvette interior - MEASURED, 2026-09-18

Everything here was learned by editing the delivered Millennium Falcon in the
user's save and having them check each change in game. The build itself is not in
this repo (another creator's work, personal use only); the scripts in `tools/` are.

## 1. Objects sit ON the deck, not AT it

The single most costly mistake of the session. Six amenities were placed at the
same Y as the floor panels and were **buried in the deck**. The game still offered
its "press E" interact prompt, so it looked like a phantom object - the user could
see the prompt but never the item.

| | Height |
|---|---|
| `^L_FLOOR_Q` floor panels | 3.10 - 3.15 |
| the creator's floor-standing items | **3.23 - 3.28** |
| what was placed wrongly | 3.10 |

**Rule: place floor-standing items at the height of the floor panel beneath them
plus about 0.13.** Snap to a real floor panel's X/Z too - this build is not on a
grid, its panels sit at arbitrary positions and rotations, so grid coordinates can
land an item where there is no floor at all.

## 2. Telling an internal wall from the hull

First attempt used "is this cell surrounded by floor on all four sides". Too crude:
in narrow parts of a ship almost everything counts as perimeter, so walls across
the cockpit tube survived and the cockpit stayed unreachable.

**The test that works: a panel with floor on BOTH sides is an internal partition.
A panel with floor on only one side is the outer hull.**

```python
def is_partition(o):
    x, y, z = o["Position"]
    return any(floor_near(x+dx, z+dz) and floor_near(x-dx, z-dz)
               for dx, dz in ((2.6, 0), (0, 2.6)))
```

On the finished Falcon this leaves 146 wall panels at body height, **all of them
hull**. Removing those would open holes in the ship's flanks. That is the floor of
how open an interior can get.

## 3. The ceiling starts lower than it looks

A sweep band of deck+2.8 (to 5.9) cut **40 ceiling panels**, 23 of them at y=5.7,
and the user reported holes in the roof.

| Band | Contents |
|---|---|
| 3.10 - 3.15 | floor |
| 3.35 - 5.35 | walking space - safe to clear |
| **5.4 and up** | **ceiling and upper hull - never cut** |

Use **deck+2.25 (5.35)** as the upper limit for interior work.

## 4. Removing walls orphans their fittings

After the first sweep, 43 wall lights, hangings, decals and posters were left
**floating in mid-air** at 4.0-5.7 where their walls had been. They block nothing,
but they look broken.

**Always run a second pass** for fittings using the same partition test:
`WALLLIGHT`, `S_WALLLIGHT`, `WALLHANGING`, `DECAL`, `POSTER`, `HOLO_SMALL`,
`CEILINGLIGHT`, `WALLFAN`, `BILLBOARD`.

Note `^WALLLIGHTBLUE` on this build is all on perimeter walls - it is the exterior
glow. Keep it. An assertion that its count stays above 100 is worth having.

## 5. Prove access rather than assuming it

Flood-fill the deck from the airlock across cells that have floor and no solid
object at body height (`tools/connectivity.py`). It found the cockpit cut off when
inspection by eye had not.

Result on the finished ship: **73 of 74 walkable cells reachable**, teleporter and
hab reachable, cockpit route opened by clearing 5 panels in the tube.

## 6. Assertions that caught real mistakes

Every write in this session ran these first, and they are cheap:

```python
assert one ^U_PARAGON                      # two roots blocks boarding entirely
assert floor count unchanged (142)         # never cut the deck out
assert objects above 5.4 >= 660            # never hole the roof
assert ^WALLLIGHTBLUE count > 100          # keep the exterior glow
assert cockpit, landing gear, airlock, hab, teleporter all still present
assert slot 8 still 163 parts              # never touch the other ship
assert slot 7 base identity J=S unchanged  # keep it the same Corvette record
```

## 7. Final state of this ship

1355 parts. Zero internal partitions - verified, not assumed. All usable items on
one deck at standing height: teleporter, trade terminal, mission table, health
station, hazard station, room scanner, save point, two archives, weapon rack, desk,
chairs, beds. The weapon rack had to be brought down from a wall mount at 4.55.

Envelope unchanged from delivery at 35.9 x 8.5 x 47.7, so the exterior is intact.

---

# Making a variation while keeping someone else's exterior

The user asked for their own interior on the delivered exterior. The method that
worked:

## Assert the exterior by identity, not by count

A count is not enough. The first attempt asserted that the number of objects
outside the walking band was unchanged, and it **failed on a false positive**: four
staircase steps added at y 0.05-2.40 are below the deck, so they counted as new
"exterior" objects.

Capture a set of `(ObjectID, rounded position)` signatures for everything outside
the band before editing, then assert **none of them are missing** afterwards.
Additions are fine; losses are not.

```python
sig = lambda o: (o["ObjectID"], tuple(round(v, 2) for v in o["Position"]))
ext_before = {sig(o) for o in objs if o["Position"][1] < 3.0 or o["Position"][1] > 5.35}
...
lost = ext_before - {sig(o) for o in kept}
assert not lost
```

On the finished variation: **all 742 exterior objects still present.**

## Reaching a hab's built-in fittings

`^B_HAB1_C` on this ship sits at y=0 while the creator's deck is at y=3.1 - so the
hab's own floor, and the **Refiner Unit built into that part**, were sealed under
the deck with no stairs anywhere in the build.

A hab's fittings are **part of its mesh**, not separate save objects. They cannot
be moved or re-seated. The only way to reach them is to open the deck above and
provide a way down.

What was done: cut 11 floor panels over the hab's forward half (keeping the airlock
approach solid so you do not walk in and drop), then build a staircase out of
`^L_FLOOR_Q` panels at 2.40 / 1.60 / 0.80 / 0.05.

**Use floor panels as steps rather than a ramp part** unless the ramp's geometry
has been measured - step heights are then known exactly.
