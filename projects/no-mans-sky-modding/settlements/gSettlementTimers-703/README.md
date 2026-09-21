# gSettlement Timers - Instant, rebuilt for 7.03.1

Original by Gumsk, nexusmods.com/nomanssky/mods/2067, file
`gSettlement Timers Instant-2067-5-7-1-0a`, built with MBINCompiler 5.71.0.1.
The unmodified original is kept here as `ORIGINAL-gumsk-unmodified.exml.txt`.

## What was wrong with it on 7.03

Nothing, for its own game version. It sets four flat timers and then supplies a
**14-entry** `SettlementBuildingTimes` list. On 7.03 that list has **63**
entries and the real buildings live at rows 36-59, so those fourteen values
land on unused padding. See `../BUILDING-TIMES-LIST-GREW.md`.

Net effect of the original on 7.03: judgements and the flat upgrade timers
change, **building renovations do not**.

## What this version changes

| Property | vanilla 7.03 | here |
|---|---|---|
| `BuildingUpgradeTimeInSeconds` | 46800 | 1 |
| `BuildingFreeUpgradeTimeInSeconds` | 10 | 1 |
| `JudgementWaitTimeMin` / `Max` | 900 / 7200 | 1 / 1 |
| `ProductionCycleDurationInSeconds` | 72000 | 1 |
| `ProductionSlotTimerOffsetInSeconds` | 30000 | 1 |
| `SettlementMiniExpeditionTime` | 3000 | 1 |
| `TowerRechargeTime` | 86400 | 1 |
| `TowerPowerRechargeTime` (4 scan types) | 86400 each | 1 each |
| `SettlementBuildingTimes` | 63 rows | **63 rows**, the 14 non-zero ones set to 1 |

The 63 rows are copied from the game's own current table, so the row count and
ordering cannot drift. Rows that vanilla sets to `0` are left at `0`.

## Deliberately not changed

- `AlertCycleDurationInSeconds` (3400) and `BugAttackCycleDurationInSeconds`
  (9000) set how often the settlement is **attacked**. Shortening them causes
  constant raids.
- `ProductUnitsPerCycleRateModifier` (5) and
  `SubstanceUnitsPerCycleRateModifier` (500) change **yields**, not timers.
  Out of scope for a timer mod.

## Install

    MODS\gSettlementTimers\GCSETTLEMENTGLOBALS.EXML
    MODS\gSettlementTimers\GLOBALS\GCSETTLEMENTGLOBALS.EXML

Both, deliberately - see the correction in `../MOD-LOADING-RULE.md`.

## Status

- Contents: **verified** by reading both installed copies back off disk. Valid
  XML, 63 rows, row 48 (Farm) reads 1.
- Effect in game: **not yet tested.**
