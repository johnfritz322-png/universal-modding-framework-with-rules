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

- **Step 2 — PASSED** (2026-09-13 15:45). `VERDICT=OVERRIDE_ON_PLAYER`, confirmed
  **via address** rather than the name fallback. Three holders of
  `M_Sword_Gargoyle_01`: two components on the player pawn, plus
  `BP_Weapon_StraightSword_C` — the weapon actor the item references, i.e. the
  drawn blade. `L_Sword_Vampiric_01` not loaded at all.

  Worth noting the probe must be run with the weapon **drawn**; an earlier press
  with it sheathed correctly returned `INCONCLUSIVE` rather than guessing.
- **Step 5 — PASSED** (2026-09-13 15:49). With the three `zzz_VrakhirGargoyle_P`
  files deleted, the **same disposable save loaded without error**. A save made
  while the override was active does not depend on it.
- **Step 6 — PASSED**. `L_Sword_Vampiric_01 loaded=true`,
  `M_Sword_Gargoyle_01 loaded=false`, and three holders of the original blade in
  an exact mirror of the override run: two on the player pawn (via address) plus
  `BP_Weapon_StraightSword_C`. The stock blade is back.

## Conclusion — REVERSIBLE AND SAVE-SAFE

The appearance is resolved **at runtime from the table**, not written into the
save. Removing three files restores the original completely, and saves made under
the override remain loadable. The rollback file list is exactly:

```text
Content\Paks\~mods\zzz_VrakhirGargoyle_P.pak
Content\Paks\~mods\zzz_VrakhirGargoyle_P.ucas
Content\Paks\~mods\zzz_VrakhirGargoyle_P.utoc
```

Nothing else needs touching to revert. No base archive, executable or save is
modified at any point.
