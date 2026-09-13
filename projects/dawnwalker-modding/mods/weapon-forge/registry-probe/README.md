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

**Nothing here is installed yet.**
