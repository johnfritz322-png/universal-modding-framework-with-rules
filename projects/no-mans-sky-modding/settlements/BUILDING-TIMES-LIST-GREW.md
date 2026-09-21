# Settlement building timers: the list grew from 14 entries to 63

This is the reason every pre-7.0 settlement timer mod appears to do nothing to
building upgrades, even when it is installed correctly and loading.

## The measurement

Vanilla 7.03.1, `GCSETTLEMENTGLOBALS.MBIN` decompiled with MBINCompiler
7.03.2-pre1. `SettlementBuildingTimes` has **63** children. The real buildings
sit at indices **36-59**; indices 0-35 and 60-62 are all `0`, unused padding.

| index | building | seconds |
|---|---|---|
| 37 | `UI_SETTLE_BUILD_PAD_SUB` | 3600 |
| 38 | `UI_SETTLE_BUILD_BAR_SUB` | 3600 |
| 39 | `UI_SETTLE_BUILD_TOWER_SUB` | 3600 |
| 40 | `UI_SETTLE_BUILD_MARKET_SUB` | 7200 |
| 41 | `UI_SETTLE_BUILD_SMALL_SUB` | 1200 |
| 42 | `UI_SETTLE_BUILD_UNIT_SUB` | 1200 |
| 43 | `UI_SETTLE_BUILD_MEDIUM_SUB` | 2800 |
| 44 | `UI_SETTLE_BUILD_LARGE_SUB` | 7200 |
| 46 | `UI_SETTLE_BUILD_SHERIFF_SUB` | 90 |
| 47 | `UI_SETTLE_BUILD_DOUBLE_SUB` | 3600 |
| 48 | `UI_SETTLE_BUILD_FARM_SUB` | **5600** |
| 49 | `UI_SETTLE_BUILD_FACT_SUB` | 5600 |
| 58 | (unnamed) | 1200 |
| 59 | `UI_SETTLE_BUILD_FACT_SUB` | 3600 |

## Why 5600 is the proof

A Farm Module renovation in game displayed `1:33:12`. Index 48 is 5600
seconds, which is `1:33:20`. The renovation was eight seconds old.

An older mod (BetterSettlements) supplied a **14**-entry list, named
`Settlement_LandingZone` through `Settlement_Builders_RoboArm`, every value set
to `1`. Those fourteen entries land at indices 0-13 - all of which are unused
padding in 7.03. **Index 48 was never touched, so the Farm still took 5600
seconds.** The mod was loading and doing exactly nothing to building upgrades.

## What this corrects

An earlier conclusion in this repo said an in-progress renovation had "banked"
its countdown and was immune to table changes. That was inferred from a timer
that moved one second in nineteen minutes, and it was the wrong explanation.
The duration comes from the table; the old mod simply never reached the row.
Whether an already-running job re-reads the table is still untested.

## The rule

Before trusting any settlement mod, **count the children of
`SettlementBuildingTimes` and compare against vanilla for the installed game
version.** A mismatch means the mod is stale, whatever its version number says.
The same check applies to the other 63-entry lists: `SettlementBuildingCosts`,
`SettlementBuildingContributions`, `BuildingUpgradePageNames`,
`BuildingProductionNotes`, `SettlementBuildingClassGenericTitle`,
`SettlementBuildingClassGenericRequirement`.

## Getting ground truth

```
hgpaktool.exe -U -f "*SETTLEMENTGLOBALS*" -O out NMSARC.globals.pak
MBINCompiler.exe convert out/gcsettlementglobals.mbin
```

Note the vanilla file is `gcsettlementglobals.mbin` - it sits at the pak root
and is the one globals file **without** `.global` in its name.
