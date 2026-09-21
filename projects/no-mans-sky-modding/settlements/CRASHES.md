# No Man's Sky 7.03.1 crashes seen while modded, and what each one means

The **"Disable Mods"** dialog is generic. No Man's Sky shows it after *any*
crash when mods are present. It is not the game naming a culprit. Always
answer **No** - answering Yes sets `DisableAllMods = true` and switches off
every mod on the machine, which is the state that wasted days previously.

## Crash A - on launch, address `0x41FC98`, seen twice

Both times the installed `GCSETTLEMENTGLOBALS.EXML` listed properties in an
order that ran **backwards** through the game's own struct.

`cGcSettlementGlobals` field positions:

| property | index |
|---|---|
| `BuildingUpgradeTimeInSeconds` | 3 |
| `BuildingFreeUpgradeTimeInSeconds` | 4 |
| `JudgementWaitTimeMin` | 5 |
| `JudgementWaitTimeMax` | 6 |
| `TowerRechargeTime` | 11 |
| `TowerPowerRechargeTime` | 12 |
| `SettlementMiniExpeditionTime` | 15 |
| `SettlementBuildingTimes` | 23 |
| `ProductionCycleDurationInSeconds` | 54 |

- Gumsk's working file: `3 -> 4 -> 5 -> 6 -> 23`, strictly ascending.
- Both crashing files: `... 6 -> 54 -> 15 -> 11 -> 12 -> 23`, jumping backwards.

**Hypothesis, not yet confirmed: the loose-EXML patcher walks the struct once,
top to bottom, so properties must appear in struct order.** The identical fault
address across two otherwise very different files supports it. A correctly
ordered file is in `gSettlementTimers-703/untested/` and has never been run.

This also clears three things previously blamed for the first crash: the 63-row
rewrite, a duplicate file at two paths, and a stray `.txt` in the mod folder.
None of those existed in the second crash.

## Crash B - mid-session, address `0x40DB6F`, seen once

Roughly 25 minutes into play, in the **freighter build menu** (Stellar Extractor
Room), with Gumsk's unmodified file installed - the configuration that had
already been confirmed working.

Different address, different circumstance, **unexplained**. One occurrence is
not a pattern; NMS crashes unaided. Do not start removing mods over it.

No diagnostic artefacts exist: no minidump, and `FullLog.txt` stays at 145 bytes
containing only a missing-`DISABLEMODS`-cache line, which is normal.

## Bisecting without deleting anything

`Binaries\SETTINGS\GCMODSETTINGS.MXML` carries a per-mod `Enabled` flag:

```
GSETTLEMENTTIMERS        Enabled=true
BUY ALL CORVETTE PARTS   Enabled=true
CORVETTEEXTRAS           Enabled=true
GLOBALS                  Enabled=true      (CorvetteOverhaul_Ultimate)
```

Flip one to `false` with the game closed and relaunch. That isolates a mod in a
few launches without touching mod files. Three of these four touch ship or
Corvette building, which is where crash B happened.

## Process note

Crash A happened twice because four untested property changes were bundled into
one launch after agreeing to add one at a time. The first crash taught nothing.
Only the matching fault address salvaged any information from the second.
