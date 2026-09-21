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
  loaded it. See `../MOD-LOADING-RULE.md`. Now at
  `MODS\BetterSettlements\`.
- Loading: **confirmed.** After the move, `GCMODSETTINGS.MXML` lists
  `BETTERSETTLEMENTS`, `Enabled=true`. It had never appeared before.
- Effect in game: **not yet confirmed.**

## A renovation already running is NOT affected

Measured: a Farm Module renovation read `1:33:12`, then `1:33:11` nineteen
minutes later, across a full game restart. One second in nineteen minutes.

So the remaining time is **not** an end-timestamp compared against the clock —
if it were, it would have dropped by nineteen minutes. It is a stored
countdown, banked when the renovation started, that only advances while the
player is present. A globals table cannot reach back into it.

Searching the save confirmed the negative: no value anywhere near 5591
seconds, and every near-future timestamp in the file is a shop restock
(all landing on 21:00 or 05:00 exactly).

**So test with something new, not with a job already in flight.**

## The cheapest test that the mod is live

`JudgementWaitTimeMin`/`Max` are now 1 and 5. Settlement decisions should
arrive every few **seconds** instead of every 15-30 minutes. That costs no
resources and needs no construction - just stand in the settlement.
