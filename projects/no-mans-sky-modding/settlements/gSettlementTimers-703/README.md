# gSettlement Timers on 7.03.1 - works unmodified

Original by Gumsk, nexusmods.com/nomanssky/mods/2067, file
`gSettlement Timers Instant-2067-5-7-1-0a`, built with MBINCompiler 5.71.0.1.
Kept here as `ORIGINAL-gumsk-unmodified.exml.txt`.

**It needs no changes for 7.03.1.** Confirmed working in game.

Install exactly as shipped:

    MODS\gSettlementTimers\GLOBALS\GCSETTLEMENTGLOBALS.EXML

Nothing else in that folder. No second copy at the folder root, no readme.

## Why it looked broken before

Two unrelated install faults, neither of them the mod's fault:

1. `DisableAllMods` was `true` in `Binaries\SETTINGS\GCMODSETTINGS.MXML`, so no
   mod on the machine had ever loaded.
2. A different settlement mod had been dropped loose at `MODS\` root instead of
   inside a folder, so it was never registered.

See `../MOD-LOADING-RULE.md`.

## A rewrite was attempted and should not be repeated

A 63-row rebuild of `SettlementBuildingTimes` was written on the mistaken belief
that the shipped 14-row list could not work. It crashed the game and has been
deleted. See `../BUILDING-TIMES-LIST-GREW.md` for why the reasoning was wrong.

## Genuine improvements still available, untested

Gumsk's file covers `BuildingUpgradeTimeInSeconds`,
`BuildingFreeUpgradeTimeInSeconds`, `JudgementWaitTimeMin`/`Max` and the
building list. These vanilla timers are **not** covered and could be added as
plain scalar properties, the same shape as the ones already in the file:

| Property | vanilla |
|---|---|
| `ProductionCycleDurationInSeconds` | 72000 |
| `ProductionSlotTimerOffsetInSeconds` | 30000 |
| `SettlementMiniExpeditionTime` | 3000 |
| `TowerRechargeTime` | 86400 |
| `TowerPowerRechargeTime` (4 named scan types) | 86400 each |

Add them **one at a time**, testing between each.

Never shorten `AlertCycleDurationInSeconds` (3400) or
`BugAttackCycleDurationInSeconds` (9000). They control how often the settlement
is raided, not how long work takes.
