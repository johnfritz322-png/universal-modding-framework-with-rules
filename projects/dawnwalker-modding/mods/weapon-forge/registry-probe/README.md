# Registry probe — does mounting a plugin append its AssetRegistry?

One question, one asset, read-only. It decides whether a genuinely new inventory
item is reachable via a plugin, or whether the shipped `AssetRegistry.bin` has to
be rewritten after all.

## Why a Material and not an item

The probe asset is a plain `UMaterial`. It needs no source data, no geometry, and
crucially **no private `DogwoodInventory` module** — which the standalone editor
does not have, and which is exactly what blocks authoring a real
`ItemWeaponDataAsset`. Using a Material isolates the thing under test: plugin
mounting and registry appending, nothing else.

It is uniquely named (`M_ForgeRegistryProbe0001`) so a runtime hit cannot be
something the game already ships.

## The pieces

| Piece | Where |
| --- | --- |
| Plugin | `D:\Dawnwalker-Modding\Projects\DawnwalkerWeaponForge\Plugins\ForgeRegistryProbe` |
| Asset creation script | `…\Tools\create_registry_probe_asset.py` (UE Python) |
| Runtime probe | `ue4ss/ForgeRegistryProbe/Scripts/main.lua` |

A gotcha worth keeping: `"ExplicitlyLoaded": true` in the `.uplugin` stops the
editor auto-mounting it, so `/ForgeRegistryProbe/...` fails to resolve and asset
creation dies with "does not map to a root". It must be **false** while authoring.

## Reading the result

Press **F10** in game. `status.txt` appears next to the Lua script:

| RESULT | Meaning |
| --- | --- |
| `REGISTERED` | Plugin mounting appends its registry. **The route works** — build the real item this way. |
| `NOT_REGISTERED` | Mounting does not append. Fall back to rewriting `AssetRegistry.bin`. |
| `PROBE_BROKEN` | The positive control failed, so the probe itself is wrong and the run says nothing either way. |

The control is `ITM_Weapon_SwordGreatMaster1a`, an item known to be registered. If
the probe cannot see *that*, it cannot be trusted about anything.

## Safety

The Lua is read-only — it queries the asset registry and writes one text file. It
never grants, spawns or equips anything, and touches no save. Test on a disposable
save regardless.

## Cook result — the plugin registry names the asset

The cook ran in 19 seconds (scoped with `-CookDir`, so it did not drag in engine
content the way the earlier 432-package cook did) and produced:

```
Plugins/ForgeRegistryProbe/Content/M_ForgeRegistryProbe0001.uasset + .uexp
AssetRegistry.bin                                      126,790 bytes
```

That registry **contains the probe asset**, in the same three-name shape the
shipped registry uses for items:

```
[661] /ForgeRegistryProbe
[662] /ForgeRegistryProbe/M_ForgeRegistryProbe0001
[663] M_ForgeRegistryProbe0001
```

It also independently validated `assetregistry.py`: a second, unrelated registry
(1,105 names) parsed byte-exactly, same version 17, same `0x12345679` body magic.

So a cook **does** emit a registry naming plugin assets. The one remaining
unknown is whether the game loads it on mount.

## Staged, not installed

```text
D:\Dawnwalker-Modding\staged-ForgeRegistryProbe\ForgeRegistryProbe    ForgeRegistryProbe.uplugin      (ExplicitlyLoaded = true, for runtime mounting)
    AssetRegistry.bin
    Content\M_ForgeRegistryProbe0001.uasset + .uexp
```

Installing means copying that folder into `Dawnwalker\Mods\` and the Lua mod into
the UE4SS `Mods` folder, then launching on a disposable save and pressing F10.
**That step needs the user's go-ahead** — it is the first thing in this project
that would put new files into the game.
