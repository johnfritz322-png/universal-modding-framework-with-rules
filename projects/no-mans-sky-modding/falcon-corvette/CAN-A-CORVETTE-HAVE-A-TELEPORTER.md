# Can a teleporter be put inside a Corvette?

Asked: remove the second airlock from the Falcon and put a teleporter to the
freighter in its place. Answered from game data on 2026-09-19, game 7.03.1.

## There is no Corvette teleporter part — VERIFIED

The Corvette's internal codename is **`biggs`**. It appears as a ship type in
`GCSPACESHIPGLOBALS` alongside Freighter, CapitalFreighter and Frigate, and every
Corvette build part carries an icon under `TEXTURES/UI/FRONTEND/ICONS/BUILDABLE/BIGGS/`.

Listing every product in `metadata/reality/tables/nms_basepartproducts.mbin` whose
icon sits in that BIGGS folder gives **644 Corvette parts**. Filtering those for
teleport, port, beam, airlock, door or hatch returns only:

    B_ALK_A  B_ALK_B  B_ALK_C  B_ALK_D          airlocks
    B_ALK_Z_A  B_ALK_Z_B  B_ALK_Z_C  B_ALK_Z_D  airlocks, Z variants
    B_DOOR0                                      interior door

**None of the 644 is a teleporter.** So a teleporter cannot be built into a Corvette
from the Corvette part set.

## The teleporter scenes that do exist are not Corvette parts

`models/common/spacecraft/biggs/` contains `biggsteleporter.scene.mbin`,
`biggsteleporter_freighters.scene.mbin`, `biggsteleporter_frigates.scene.mbin`,
`biggsteleporter_model.scene.mbin` and `telecontrol.scene.mbin`.

These are ship-system models, not buildable products — none has an entry in the
parts products table. `biggs.scene.mbin`, the Corvette's core module, is a 6x6 block
of walls, ceiling, gun and collision, and contains no teleporter node. So the
teleporter is placed by the game, not by the player.

## But the ordinary base teleporter might still work — UNVERIFIED, worth trying

The Falcon already contains parts that are **not** Corvette parts. From the live save:
`^BUILDSAVE` at (-3.68, 3.23, -7.44) and two `^ARCHIVE`. Those are ordinary
base-building products, placed inside a Corvette.

Comparing the ordinary `TELEPORTER` product against `BUILDSAVE` in
`nms_basepartproducts`, every placement-related field is identical:

| Field | TELEPORTER | BUILDSAVE |
|---|---|---|
| `BuildableShipTechID` | empty | empty |
| `BaseValue` | 2 | 2 |
| `Cost.SpaceStationMarkup` | 0 | 0 |
| `Cost.BuyBaseMarkup` | 0 | 0 |

There is **no data-level flag** that permits `BUILDSAVE` on a ship and forbids
`TELEPORTER`. That does not prove the game allows it — the restriction could live in
code or in which categories the Corvette build menu offers. **The test is to open
build mode inside the Corvette and look for the teleporter in the list.**

## If it is not offered, the mod route

Patch a new Corvette part into `nms_basepartproducts` and `basebuildingpartstable`
pointing at `BIGGSTELEPORTER_FREIGHTERS.SCENE.MBIN`. This works, but
`OUTCOME-AND-LESSONS.md` already recorded the cost: a save that contains a modded
part **depends on that mod staying installed**. Remove the mod and the ship has a
hole where the part was.

## Removing the second airlock

The two airlocks sit 3 units apart on the same axis, both with `At` = (0, 0, 1):

    B_ALK_Z_A  (0, 3, -3)   21.63 units from the cockpit
    B_ALK_C    (0, 3, -6)   23.43 units from the cockpit

They read as an outer and inner pair forming one entrance, not two separate doors.
Removing one may break the entrance rather than simplify it. The in-game build menu
will refuse an invalid removal and show the result immediately; a save edit will not.

**The standing rule from `OUTCOME-AND-LESSONS.md` applies: interior changes go through
the in-game build menu.** Three of three save-edit interior changes failed, and one of
those three was placing a teleporter beside this very airlock.
