# Persistence & rollback test — run before scaling

Proves the mod is reversible and save-safe. Do this on a **disposable save**, not
the main playthrough.

## Steps

| # | Action | Expected |
| --- | --- | --- |
| 1 | Launch, load the disposable save | loads normally |
| 2 | Equip The Vrakhir, draw it, press **F8** | `VERDICT=OVERRIDE_ON_PLAYER` |
| 3 | **Quit the game fully** | — |
| 4 | Delete the three `zzz_VrakhirGargoyle_P.{pak,ucas,utoc}` from `~mods` | only the user's mods remain |
| 5 | Relaunch, load the same disposable save | **loads without error** |
| 6 | Equip The Vrakhir, draw, press **F8** | `VERDICT=ORIGINAL_IN_USE` — the stock blade is back |

## What each step proves

- **5** is the one that matters: a save made while the override was active still
  loads once the override is gone. If it does not, the mod is not save-safe and
  must not be used on a real playthrough.
- **6** proves the swap is not written into the save — the appearance is resolved
  at runtime from the table, so removing the table restores the original.

## Failure handling

If step 5 fails to load, **stop**. Do not reinstall. The save format would then be
carrying mod state, which is a different and more serious problem than a visual
override, and it would need investigating before any further testing.

## Result

_(record the outcome here)_

- Step 2: 
- Step 5: 
- Step 6: 
