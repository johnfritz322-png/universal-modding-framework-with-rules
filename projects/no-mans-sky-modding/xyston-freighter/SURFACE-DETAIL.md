# Surface detail: 503 faces to 5,333

The hull read as a blocky primitive next to the vanilla freighter. Five procedural
detail passes fix that without turning the scene into thousands of nodes.

## Face budget

| | Before | After | Vanilla freighter |
|---|---|---|---|
| Faces | 503 | **5,333** | 76,996 |
| Meshes | 12 | 18 | 334 |

10.6x the detail for 6 extra scene nodes. Still 7% of the vanilla face count, but the
shapes that matter now exist: the eye reads clutter, not a slab.

## Why it is only 6 extra nodes

The `Greebler` class accumulates hundreds of boxes into **one** mesh with many
disconnected islands. Every detail pass emits a single mesh. A node per greeble would
have meant 400+ scene nodes for the same pixels.

| Mesh | Faces | What it is |
|---|---|---|
| `DorsalGreebles` | 1,932 | panel clutter over the top deck, thinning towards the bow |
| `FlankRidges` | 1,800 | five horizontal strakes down each flank |
| `DorsalTrenches` | 1,152 | three channels each side of the command block |
| `VentralDetail` | 288 | hangar bays plus belly plating |
| `FlankBays` | 72 | recessed bay blocks that break up the slab |
| `CommandTiers` | 54 | stepped tiers and comms clutter on the command block |

Placement uses a fixed seed (`random.Random(24601)`), so the ship is identical on
every rebuild.

## The geometry that made it sit right

Detail has to follow the hull, which tapers in two directions at once. Three helpers
do this, and getting them wrong produced visible failures:

- `dorsal_z(y)` — the top surface slopes from a thin bow to the full draught aft.
- `dorsal_half_width(y)` / `ventral_half_width(y)` — the hull narrows to nothing at
  the bow.
- `flank_x(y, frac)` — X on the sloped flank at a fraction of the way up it. The flank
  leans inward, so **interpolating between the ventral and dorsal widths** is what
  keeps strakes flush.

### Two mistakes worth recording

1. **Flank strakes placed at the ventral width** floated off the hull like railings,
   because the flank leans inward as it rises. Fixed by `flank_x`.
2. **Trenches built as one long box** rose out of the sloping deck and shot past the
   hull edge near the nose. Fixed by building them as segments that sample
   `dorsal_z(y)` and stop once the offset exceeds `dorsal_half_width(y) * 0.88`.

Both were only visible in a render. Neither would have shown up in the face count or
the export log.

## Installed

`GAMEDATA\MODS\XystonFreighter\` — scene 19,465 bytes, geometry 12,543 and 652,767.

Dimensions unchanged: 10,032 x 5,800 x 2,810 m, still 2.33x the stock freighter's
length and 2.21x its beam.

**Still never launched.** Everything above is Blender renders and file structure.
