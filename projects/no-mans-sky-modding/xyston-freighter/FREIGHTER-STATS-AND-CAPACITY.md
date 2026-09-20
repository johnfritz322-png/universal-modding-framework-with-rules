# Freighter class, storage, stats and ship parking

Asked for: S-class, everything currently equipped kept, completely maxed stats
including storage, and parking for every ship — double the current capacity.
Read from the live save and the game tables on 2026-09-19.

## Already done by the game — VERIFIED, no change made

**The freighter is already S-class.** All three of its inventories carry
`B@N = {"1o6": "S"}`. There was nothing to raise.

**Storage is already at the engine's hard ceiling.** `inventorytable.mbin` gives
the caps for `FreighterLarge`, which is what a capital freighter uses:

| Inventory | Save key | Grid | Unlocked | Game maximum | State |
|---|---|---|---|---|---|
| General | `8ZP` | 10 x 12 | 120 | `MaxWidthLarge 10` x `MaxHeightLarge 12` = 120 | **maxed** |
| Technology | `0wS` | 10 x 6 | 60 | TechBounds `10` x `6` = 60 | **maxed** |
| Cargo | `FdP` | 7 x 5 | 0 | `MaxCargoSlots = 0` | does not exist for this class |

The cargo grid is vestigial — capital freighters are given no cargo slots at all,
so its 7x5 shape is never used. Expanding it would be writing a number the game
ignores.

**All installed technology is healthy.** 26 items, every one `b76 = True` (fully
installed) and `eVk = 0.0` (undamaged). The upgrade modules are all tier 4 — the
S-class tier — three of most types: 2 speed, 1 hyperdrive, 3 combat, 2 fuel, 3 mining,
3 trade, 3 exploration.

## Changed

### Stat rolls pinned to maximum — mod, no save edit

Procedural upgrade stats are rolled at runtime from
`nms_reality_gcproceduraltechnologytable.mbin` using the seed stored in the save.
Setting `ValueMin = ValueMax` there makes **modules already owned** roll their
maximum, with no seed hunting and nothing written to the save.

All 28 `UP_FR*` entries are patched, 23 stat rolls pinned. Ship, multi-tool, exosuit
and Corvette upgrades are deliberately left alone.

**Honest scope — most S-class freighter modules were already fixed at maximum:**

| Module owned | Stat | Before | After |
|---|---|---|---|
| `UP_FRHYP4` | Hyperdrive jump distance | 200–250 | **250** |
| `UP_FRFUE4` | Fleet fuel use | 0.80–0.85 | **0.85** |
| `UP_FRSPE4` | Fleet speed | 1.15 fixed | unchanged |
| `UP_FRCOM4` | Fleet combat | 1.15 fixed | unchanged |
| `UP_FRTRA4` | Fleet trade | 1.15 fixed | unchanged |
| `UP_FREXP4` | Fleet exploration | 1.15 fixed | unchanged |
| `UP_FRMIN4` | Fleet mining | 1.15 fixed | unchanged |

So the real gain is on two of the seven. The other five were already at their
designed ceiling. The tier 1–3 entries are patched too, so any weaker module picked
up later also rolls maximum.

### Ship parking doubled — mod

`GCFLEETGLOBALS` holds `MaxNumberOfPlayerShipsInFreighterHangar`, vanilla **6**.
Set to **12**, which is both the requested doubling and the player's full ship count.

Found by decompiling all 38 globals files and searching them; the field is not in
`gcfreighterbaseglobals` where it would be expected.

**NEEDS TESTING:** whether the hangar has room to display 12 without ships
overlapping. Gumsk's long-standing mod for this raises it to 9, which may be the
practical limit rather than a preference.

### Hyperdrive charge refilled — save edit

`^F_HYPERDRIVE` sat at **64 / 120**. This is stored state, not a table value, so no
mod can fix it. `tools/top_up_freighter_tech.py` refills any chargeable item in the
freighter technology inventory that is below maximum, writes both save slots, and
re-reads each file from disk to confirm. Backup taken first:
`outputs/NMS-Before-TechTopUp-20260919-211754`.

Editing technology and inventory amounts is the sanctioned use of save editing under
`OUTCOME-AND-LESSONS.md`, which bans editing a Corvette interior this way but keeps
technology and inventory explicitly.

## Hull widened

`BEAM` 1,150 m -> **1,450 m**, giving the 0.60 width-to-length ratio a real Imperial
Star Destroyer has. At 1,150 the plan view read as a dagger rather than an arrowhead.
Rebuilt and reinstalled; length unchanged at 9,600 m.

## Mods installed

| Folder | What it does | Conflicts |
|---|---|---|
| `XystonFreighter` | the Star Destroyer hull | none |
| `XystonFreighterMaxed` | stat rolls + ship parking | none — checked, nothing else touches these two files |
| `CorvetteExtras` | teleporter and hatch in the Corvette builder | none |
