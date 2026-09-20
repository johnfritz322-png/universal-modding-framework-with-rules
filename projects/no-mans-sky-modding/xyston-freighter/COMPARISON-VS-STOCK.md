# Xyston hull vs the stock capital freighter

Both measured in Blender at true relative scale on 2026-09-19, by importing the live
vanilla scene with NMSDK and building the Xyston in the same scene.
`tools/compare_against_vanilla.py` reproduces it.

## Numbers

| | Stock capital freighter | Xyston hull | Ratio |
|---|---|---|---|
| Length | 4,301 m | 10,032 m | **2.33x** |
| Width | 2,624 m | 5,800 m | **2.21x** |
| Height | 2,259 m | 2,808 m | **1.24x** |
| Meshes | 334 | 12 | |
| Faces | 76,996 | 503 | **0.0007x** |

The Xyston is a little over twice the stock ship in both length and beam, but barely
taller. That is correct for the subject: a Star Destroyer is a flat wedge, while the
stock NMS freighter is a tall spine with wings hanging off it.

The length figure of 10,032 m rather than the intended 9,600 is the axial cannon
muzzle projecting past the bow. Height 2,808 m rather than 1,200 is the
superstructure, bridge tower and shield globes stacked above the hull.

## The honest weakness: 503 faces against 76,996

The stock freighter is a detailed model — greebling, antennae, panel lines, recessed
bays. The Xyston is flat planes and primitives. Side by side at close range that gap
is obvious, and no amount of scaling hides it.

It will read well at distance, in silhouette, and against a planet. It will read as
blocky up close, especially where the superstructure meets the hull.

Improving it means adding surface detail: panel insets along the flanks, a trench
line, the stepped tiers of the command block, and hangar bays under the stern.

## Two measurement traps found while doing this

Both would have produced badly wrong numbers if taken at face value.

1. **`FXSphere` effect volumes.** The scene contains six of them, the largest
   3,012 x 6,083 x 2,074, wrapping the whole ship. Including them makes the stock
   freighter measure 6,083 m long and render as a smooth pill. They are effects, not
   hull.
2. **Every LOD level imports at once.** `_HullWings_CLOD0` through `LOD3` are four
   copies of the same wing in the same place at descending detail. Counting them
   inflates the face count roughly fourfold and changes nothing about the size.

Filtering `FXSphere*` and `LOD[1-9]` dropped 398 of 732 meshes and gave the real
hull: **4,301 x 2,624 x 2,259 m at 76,996 faces**.

An earlier estimate in this project of "about 708 m" came from reading the root
node's own geometry bounds only, which misses every referenced sub-scene. That
figure was wrong and this supersedes it.

## Two more NMSDK fixes needed to import at all

Both in the installed add-on, both about missing textures — the unpacked tree here
has geometry and scenes but no DDS files:

- `utils/io.py`, `realize_path`: `op.join(base, fpath)` throws when `get_NMS_dir("")`
  returns `None`. Return `None` instead, and catch `TypeError` alongside `ValueError`.
- `NMS/material_node.py`: two `img.colorspace_settings.name = ...` lines run even when
  `img` is `None`. Guard both.

With those, the import goes from 3 meshes and an aborted recursion to the full 732.
