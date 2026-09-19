# Editing a Corvette interior

> ## READ THIS FIRST - THE METHOD BELOW FAILED
>
> An earlier version of this file recommended a test for telling internal walls
> from hull. **That test was wrong and it destroyed a working ship.** Three sweeps
> using it removed 141 panels; the user ended up unable to board at all, with
> visible holes in the exterior. The build had to be restored from backup.
>
> The wrong technique and why it failed are written out below, because the failure
> is more useful than the recipe was. **Do not open a Corvette interior by bulk
> rule.** Sections 1, 3, 5, 6, 7 and 8 are still sound.

## 1. Objects sit ON the deck, not AT it - STILL VALID

Six amenities placed at the same Y as the floor panels were buried in the deck.
The game still offered its "press E" prompt, so it read as a phantom object - the
user saw the prompt but never the item.

| | Height |
|---|---|
| L_FLOOR_Q floor panels | 3.10 - 3.15 |
| the creator's floor-standing items | **3.23 - 3.28** |
| what was placed wrongly | 3.10 |

Place floor-standing items at the height of the floor panel beneath them plus
about **0.13**, and snap to a real floor panel's X/Z. This build is not on a grid,
so grid coordinates can land an item where there is no floor at all.

## 2. Telling an internal wall from hull - THE FAILED METHOD

The rule used was:

> a panel with floor on BOTH sides is an internal partition;
> floor on only one side means hull.

**This is wrong.** On a hull that curves - and a Falcon saucer curves everywhere -
outer skin panels frequently have floor on both sides of them. The rule classifies
the ship's own shell as interior partition and deletes it.

Damage, in three sweeps that each looked successful at the time:

| Pass | Removed | Justification given |
|---|---|---|
| open-plan | 90 panels | "internal partitions in interior cells" |
| full-open | 40 panels | "partitions, floor on both sides" |
| variation | 11 floor panels | bay over the hab |

Result: holes in the exterior, and the ship could not be boarded at all.

### Why the safety assertion did not catch it

The guard was:

    ext_before = {sig(o) for o in objs
                  if o["Position"][1] < 3.0 or o["Position"][1] > 5.35}
    assert not (ext_before - ext_after)

It asserts nothing OUTSIDE the band 3.0-5.35 was lost. But 3.35-5.35 is **exactly
the band being edited**. The assertion was structurally incapable of detecting the
damage, and it passed on every run while the ship was being taken apart.

**A guard whose range excludes the range you are modifying proves nothing.** It is
worse than no guard, because it manufactures confidence.

### What to do instead

Do not classify by floor adjacency. A panel is hull if **nothing lies outboard of
it** - cast outward from the ship centre through the panel and check for geometry
beyond it. Anything with open space outside is skin.

And regardless of the test: **work in small batches with an in-game check between
each one.** The three sweeps above were 90, 40 and 11 objects with no verification
between them, so three rounds of damage accumulated before anything surfaced.

## 3. The ceiling starts lower than it looks - STILL VALID

A band of deck+2.8 (to 5.9) cut 40 ceiling panels, 23 of them at y=5.7, and the
user reported holes in the roof.

| Band | Contents |
|---|---|
| 3.10 - 3.15 | floor |
| 3.35 - 5.35 | walking space |
| **5.4 and up** | **ceiling and upper hull - never cut** |

## 4. Removing walls orphans their fittings - VALID BUT MOOT

After the first sweep, 43 wall lights, hangings and posters were left floating in
mid-air where their walls had been. If walls are ever removed, sweep fittings too.
WALLLIGHTBLUE on this build is all exterior glow - keep it.

## 5. Prove access by flood fill - STILL VALID

Flood-fill the deck from the airlock across cells that have floor and no solid
object at body height (tools/connectivity.py). It found the cockpit cut off when
inspection by eye had not.

## 6. Assertions worth keeping - WITH THE CAVEAT ABOVE

    assert exactly one ^U_PARAGON        # two roots blocks boarding entirely
    assert floor count unchanged         # never cut the deck out
    assert objects above 5.4 >= 660      # never hole the roof
    assert ^WALLLIGHTBLUE count > 100    # keep the exterior glow
    assert cockpit, gear, airlock, hab present
    assert slot 8 still 163 parts        # never touch the other ship
    assert slot 7 base identity J=S unchanged

These caught real mistakes. Note what they share: each names a **specific,
countable invariant**. The one that failed was the one that tried to generalise,
and generalised over the wrong range.

## 7. A hab's built-in fittings cannot be moved - STILL VALID

B_HAB1_C sits at y=0 while the creator's deck is at y=3.1, so the hab's own floor -
and the **Refiner Unit built into that part** - are sealed under the deck, with no
stairs anywhere in the build.

A hab's fittings are part of its **mesh**, not separate save objects. They cannot
be re-seated. Reaching them means opening the deck above, which after the failure
above should only be attempted in small, individually verified steps.

## 8. Restoring after a bad edit - STILL VALID

Restore **only the build**, not the whole save file, or the player loses every bit
of progress since the backup was taken:

    live save  <-  copy @ZJ from the backup's slot-7 PlayerShipBase
                   leave @Cs[7].PMT (ship technology) alone
                   leave everything else in the save alone

tools/restore_build.py does exactly this. It restored 1495 objects while keeping 38
fitted technology items and the rest of the save intact.

**Take a fresh four-file backup before every single write.** Twenty-one were taken
during this session, and the last one is what saved the ship.
