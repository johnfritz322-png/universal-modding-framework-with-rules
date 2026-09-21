# Instant settlement upgrades and production

Mod: BetterSettlements by TwistedViking, edited. One file:

    MODS\BetterSettlements\GCSETTLEMENTGLOBALS.EXML

Patches `cGcSettlementGlobals`. Values changed from the shipped mod:

| Property | vanilla | shipped mod | now |
|---|---|---|---|
| `ProductionCycleDurationInSeconds` | 72000 | 30000 | 1 |
| `BuildingUpgradeTimeInSeconds` | 46800 | 23400 | 1 |
| `BuildingFreeUpgradeTimeInSeconds` | 10 | 5 | 1 |
| `JudgementWaitTimeMin` | 900 | 450 | 1 |
| `JudgementWaitTimeMax` | 7200 | 3600 | 5 |
| all 14 `SettlementBuildingTimes` | varies | varies | 1 |

`JudgementWaitTimeMax` is 5 on purpose — Min/Max is a random range, so
settlement decisions arrive 1–5 seconds apart rather than all at once.

The 14 building types: LandingZone, Bar, Tower, Market, Small,
SmallIndustrial, Medium, Large, SheriffsOffice, Double, Farm, Factory,
FishPond, Builders_RoboArm.

## Vanilla timers this mod does NOT override

If something still feels slow, it is one of these:

`AlertCycleDurationInSeconds` 3400, `BugAttackCycleDurationInSeconds` 9000,
`ProductionSlotTimerOffsetInSeconds` 30000, `SettlementMiniExpeditionTime`
3000, `TowerRechargeTime` 86400, and `ProductionTimeMultiplier`
(0.1 / 0.15 / 0.2 / 0.25 / 0.3 / 0.9 / 1.0 / 3.0 / 15.0).

## Status

- File contents: **verified** by reading back off disk — valid XML, 62
  properties, every timer at its intended value.
- Location: **was wrong.** It sat loose at `MODS\` root, so the game never
  loaded it. See `../MOD-LOADING-RULE.md`. Now moved into a folder.
- Effect in game: **not yet tested.**

## Open question

A renovation already counting down when the file was fixed may have its end
time stored in the save rather than recomputed from this table. Unknown which.
Test by watching an in-progress timer first, then starting a fresh upgrade.
