# Registry probe — installed 2026-09-13

First time anything from this project has been put into the game. Read-only test;
every change is listed below and every one is reversible.

## What was added

```text
Dawnwalker\Mods\ForgeRegistryProbe\
    ForgeRegistryProbe.uplugin            401 B    (ExplicitlyLoaded = true)
    AssetRegistry.bin                 126,790 B
    Content\M_ForgeRegistryProbe0001.uasset   2,388 B
    Content\M_ForgeRegistryProbe0001.uexp     9,481 B

Dawnwalker\Binaries\Win64\ue4ss\Mods\ForgeRegistryProbe\Scripts\main.lua   3,321 B
```

`Dawnwalker\Mods\` did not previously exist and was created for this.

## What was modified

One line added to the UE4SS mod list:

```text
ue4ss\Mods\mods.txt     + "ForgeRegistryProbe : 1"
```

Backed up first, unchanged, at `mods.txt.bak-before-registryprobe-20260913`.

**Nothing else was touched.** No base `.pak`/`.utoc`/`.ucas`, no executable, no
save, no existing mod. `~mods` still holds only `SkillsNoTimeCost` and the RTX
5080 profile.

## Running it

1. Launch on a **disposable save** — a throwaway manual slot, never the main run.
2. Press **F10**.
3. Read `ue4ss\Mods\ForgeRegistryProbe\status.txt`.

| RESULT | Meaning |
| --- | --- |
| `REGISTERED` | Mounting appends the plugin registry. **Route proven** — build the real item this way. |
| `NOT_REGISTERED` | Mounting does not append. Fall back to rewriting `AssetRegistry.bin`. |
| `PROBE_BROKEN` | Positive control failed; the probe is wrong and the run says nothing. |

If the plugin does not mount at all, the expected outcome is `NOT_REGISTERED`
with a healthy control — the same signal as "mounted but not appended". Those two
cannot be told apart from the status file alone; `UE4SS.log` is the tiebreaker.

## Uninstall

Delete the two added folders and restore the backed-up `mods.txt`:

```text
rmdir /s  Dawnwalker\Mods\ForgeRegistryProbe
rmdir /s  Dawnwalker\Binaries\Win64\ue4ss\Mods\ForgeRegistryProbe
copy      ue4ss\Mods\mods.txt.bak-before-registryprobe-20260913  ue4ss\Mods\mods.txt
```

`Dawnwalker\Mods\` itself can also go if empty.

## Note

Codex's earlier `ForgeItemLoadProbe` is still enabled in `mods.txt`. It is
read-only too, but it may add its own log noise during this test.
