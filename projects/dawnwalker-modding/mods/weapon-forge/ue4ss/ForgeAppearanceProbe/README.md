# Forge Appearance Probe

Answers one question: **when `DT_WeaponAppearances` is overridden, does the game
use the override?**

Read-only. It never grants, spawns, equips or writes to a save. One text file is
its only side effect.

**Untested.** It was written after the last in-game session and has not been run.
The conventions it follows are all verified; the three probe methods are not.

## Install

```text
<game>\Dawnwalker\Binaries\Win64\ue4ss\Mods\ForgeAppearanceProbe\Scripts\main.lua
```

Add to `ue4ss\Mods\mods.txt` (back that file up first):

```text
ForgeAppearanceProbe : 1
```

## Run

1. Install the appearance-repoint mod (`appearance-repoint/`) so there is
   something to detect.
2. Launch, load a **disposable save**, **equip the weapon and have it drawn**.
3. Press **F8**.
4. Read `ForgeAppearanceProbe/status.txt`.

## Reading it

| VERDICT | Meaning | Next move |
| --- | --- | --- |
| `OVERRIDE_LIVE` | `M_Sword_Gargoyle_01` is resident — our container wins | The visual comes from elsewhere. Investigate the equip path and `AppearanceSubsystem.ItemAppearanceMap` |
| `ORIGINAL_IN_USE` | Stock blade resident — our container is not winning | Load order / packaging problem |
| `INCONCLUSIVE` | Neither resident | Weapon not drawn, or meshes stream on demand. Re-equip and retry |

Section `[1]` is the most direct signal — it lists the mesh on every live sword
`StaticMeshComponent`, i.e. what is **actually rendering**. If that names a blade,
believe it over the other two sections.

## Conventions it follows — keep them in any probe for this game

These were each learned by losing a run to them:

- **F8, not F10.** `ForgeItemLoadProbe` and `ConsoleEnabler` both bind F10.
- **Forward slashes in paths.** A Windows path in a Lua literal is an invalid
  escape (`\s`) and kills the entire script at load — the keybind silently binds
  nothing and nothing appears to happen.
- **`ExecuteInGameThread` around anything touching UObjects**, or it throws
  "can only be called from within the game".
- **Write results to a file.** `print`/`unreal.log` do not reliably reach the log.
- **Carry a positive control.** A probe that reports "not found" for something
  that definitely exists is broken, and without a control that reads as a real
  negative. This cost three runs on the registry probe.

## If section [1] finds nothing

`FindAllOf("StaticMeshComponent")` may not be available in this UE4SS build, or
the weapon mesh may be a different component class. Fall back to section `[2]`,
which only needs `StaticFindObject`, and is the check that actually decides the
verdict.
