# Outcome, and what not to do next time

Session of 2026-09-18. Goal: a Millennium Falcon Corvette in ship slot 7.

## What actually worked

**The bot delivery.** Hatrin_Gomax's 1495-part build, ordered through nomansapp's
service bot, in about a minute. It is an excellent replica and the user is happy
with the exterior.

**Technology.** All 38 items fitted, every upgrade module at S or X-class, no
system over the 3-module cap. Done entirely in `@Cs[7].PMT`, which never touched
the build and never broke anything.

## What did not work: five rebuilds of a procedural Falcon

Before the delivery, five versions were generated from surface mathematics and
installed. Every one was rejected. The reason is in `HOW-A-REAL-REPLICA-IS-BUILT.md`:
sampling a surface produces a smooth silhouette, and a replica is ~1450
individually authored details. **No amount of tuning radii closes that gap.**

That should have been said after the first rejection, not the fifth.

## Three separate times the ship became unboardable - all interior edits

| # | Cause | Fix |
|---|---|---|
| 1 | Removed hull panels misclassified as internal walls, using a floor-on-both-sides test that is wrong on a curved hull | restore from backup |
| 2 | Cut ceiling panels - the sweep band reached to 5.9, the ceiling starts at 5.4 | restore the 40 panels |
| 3 | **Placed the teleporter 1.73 units in front of the inner airlock**, and the trade terminal 3.18 | restore from backup |

The exterior was never the problem. Every failure was an edit to the inside.

### Clearance rule

Anything placed on the deck must be **at least 4 units from every airlock**, and
nothing may sit in the airlock's `At` direction, which is the way the door opens.
Measure it and assert it:

    for a in airlocks:
        for placed in new_objects:
            assert dist(a.Position, placed.Position) >= 4.0

## The honest conclusion

**Do not edit a Corvette interior by writing save files.** Three failures out of
three attempts, each from a different cause, each invisible until the player
launched the game.

The interior should be changed **in game, with the Corvette build menu**. The game
shows collision, refuses to seal a doorway, and gives immediate visual feedback.
That loop cannot be matched by editing coordinates blind.

Save editing remains the right tool for things that can be verified from the data
alone: technology and inventory, reading and auditing a build, finding what a part
is and where it sits, restoring from backup.

## The mod question, answered

Asked: could a `.pak` mod give the Falcon exterior without the interior?

**No, and it would not help.** A Corvette has no single exterior mesh - it is
assembled at runtime from shared parts. A mod could only:

- replace a part's mesh, which changes that part on **every ship using it**,
  including the user's other Corvette; or
- add a new part, which needs the parts table modded and leaves the save dependent
  on the mod staying installed.

Neither addresses the interior, which is also made of parts. The delivered build
already *is* the Falcon exterior.

## Backups

Twenty-three four-file backups were taken, one before every write. Three of them
were needed. **Take the backup every time.**

Restore only `@ZJ` from the backup, never the whole save file, or the player loses
all progress since - see `tools/restore_build.py`.
