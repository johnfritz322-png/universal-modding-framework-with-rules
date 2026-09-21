# Settlement building timers: array entries are matched by NAME, not position

**This file previously claimed the opposite and was wrong.** It is kept, corrected,
because the wrong version was acted on and caused a crash.

## What is true

Vanilla 7.03.1 `GCSETTLEMENTGLOBALS.MBIN`, decompiled with MBINCompiler
7.03.2-pre1, has **63** children under `SettlementBuildingTimes`. Fourteen of
them are non-zero; the rest are padding.

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

A Farm Module renovation displayed `1:33:12` in game. 5600 seconds is
`1:33:20`. So the displayed duration does come from row 48.

## The wrong inference

From that, this file concluded: a mod supplying a **14**-entry list lands on
indices 0-13, which are padding, therefore every pre-7.0 settlement mod is
dead. That does not follow, and it is false.

Gumsk's gSettlement Timers ships fourteen entries named `Settlement_LandingZone`
through `Settlement_Builders_RoboArm`. Installed unmodified on 7.03.1, **it
works.** Confirmed in game by the user.

So the loose-EXML patcher matches array children **by name**. Position is
irrelevant, and an entry count that differs from vanilla is not a defect.

## Why the decompiler misled

MBINCompiler 7.03.2-pre1 prints all 63 children as `<Property name="None" .../>`.
That is the tool failing to resolve the enum member names, **not** the game
having nameless rows. Treating decompiler output as ground truth for names is
what produced the error above.

**Rule: a decompiler's inability to name something is a fact about the
decompiler.** Check it against a mod known to work before building on it.

## The crash, and what is NOT known about it

A rebuilt file was installed that changed three things at once:

1. the same EXML placed at both the mod folder root and inside `GLOBALS\`
2. a stray `.txt` file dropped in the mod folder
3. `SettlementBuildingTimes` replaced with 63 rows all named `"None"`

The game crashed on launch with "Potential mod incompatibilities have been
detected". All three were reverted together, so **which one caused it was never
isolated.** Item 3 is the strongest suspect given that names turn out to matter,
but that is a suspicion, not a finding.

The process error is the point: three simultaneous untested changes meant the
crash taught us nothing. One change at a time.
