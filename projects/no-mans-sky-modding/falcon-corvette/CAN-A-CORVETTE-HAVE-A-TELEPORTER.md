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

---

## Answered: `CorvettePartCategory` is the gate — VERIFIED

Diffing the `B_ALK_C` product against the `TELEPORTER` product in
`nms_basepartproducts` showed one field that decides everything:

    <Property name="CorvettePartCategory" value="GcCorvettePartCategory">
      <Property name="CorvettePartCategory" value="Access" />   B_ALK_C
      <Property name="CorvettePartCategory" value="None" />     TELEPORTER
    </Property>

Counting the whole table: 1,185 products are `None`, and the rest carry a Corvette
category — Hull 486, Engine 26, Wing 24, Connector 24, Interior 22, Decor 15, Hab 6,
Gun 6, Shield 5, Access 5, Gear 4, Reactor 4, Cockpit 3, TractorBeam 2, plus two
combined values (`Gear, Engine` and `Hab, Access`), which shows the field accepts
comma-separated flags.

**But `None` does not mean "cannot be placed in a Corvette".** Every part already
sitting inside the Falcon — `BUILDSAVE`, `ARCHIVE`, `STORAGEPANEL`, `L_FLOOR_Q`,
`WALLLIGHTBLUE`, `S_CHAIR0` — is `None`. The category marks *structural ship parts*
for the ship builder; ordinary base objects are placed through the normal build menu
while aboard. So the teleporter may already be placeable with no mod at all.

## The mod — BUILT AND INSTALLED, NOT TESTED

`tools/build_corvette_teleporter_mod.py` sets `TELEPORTER`'s category to `Interior`,
which lists it as a first-class Corvette part in the ship builder.

**It deliberately reuses the existing `TELEPORTER` id instead of adding a new part.**
`OUTCOME-AND-LESSONS.md` warned that a save holding a modded part depends on that mod
staying installed. Reusing a vanilla id removes that risk entirely: uninstall the mod
and any placed teleporter still resolves to a real vanilla object.

Two forms are built:

| Form | Path | Notes |
|---|---|---|
| EXML patch | `mods/CorvetteTeleporter/METADATA/REALITY/TABLES/NMS_BASEPARTPRODUCTS.EXML` | 436 bytes, touches one field, coexists with other mods. **Installed.** |
| MBIN replacement | built on demand by the script | 1,752,856 bytes, fallback if the patch form is not picked up |

Readback of the replacement confirms 1,820 products preserved, `TELEPORTER` now
`Interior`, and the controls unchanged (`B_ALK_C` still `Access`, `BUILDSAVE` still
`None`).

The EXML partial-patch form was copied from a working 7.03 patch already on this
machine — Corvette Overhaul Ultimate's `GCSPACESHIPGLOBALS.GLOBAL.EXML` — which uses
a `<Data template="...">` root containing only the changed properties.

No conflict: the only other installed mod edits `GCCAMERAGLOBALS` and
`GCSPACESHIPGLOBALS`, not this table.

**UNVERIFIED:** whether the game lists it, whether a teleporter aboard a Corvette
joins the teleport network, and whether setting a Corvette category removes it from
the ordinary base build menu (the base menu is driven by a separate `WikiCategory`
field, which is untouched, but that has not been confirmed in game).
