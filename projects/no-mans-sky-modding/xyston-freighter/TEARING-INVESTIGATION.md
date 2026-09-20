# The ship renders torn — what has been ruled out, and the bisect

2026-09-20. In game the hull appears shredded: long thin triangular shards, torn
surfaces, smeared bands. Not a shading problem — geometry is being destroyed.

## Ruled out, with evidence

| Suspect | Finding | Verdict |
|---|---|---|
| Inside-out normals | 16 of 20 meshes were inward. Fixed, all now positive volume | real bug, fixed, **not the tearing** |
| Position precision | Both vanilla and ours store positions as half-float (type `5131`) | same format as vanilla |
| Model too large for half-float | Max coordinate 1,308 gives a 1.0 unit step, vanilla's 215 gives 0.125 | **shrinking would not help** — half-float is floating point, so relative precision is constant. A feature that is 0.2% of the model gets the same ~5 quantisation steps at any modelling size |
| Wrong model bounds | AABB reads -725..725, -1308..1266, -36..702 — matches the source geometry exactly | correct |
| Overlapping mesh ranges | `MeshVertRStart`/`End` are 20 contiguous non-overlapping spans ending exactly at `VertexCount - 1` | correct |
| Index width | `Indices16Bit = 1` with 27,308 vertices, well inside the 65,535 limit | fine |

## Still open

- **No LOD.** Our scene declares `NUMLODS 1`; vanilla ships four levels. ~2,000 greeble
  boxes with no LOD at 4.8 km could alias into shimmering shards.
- **Vertex layout differs from vanilla.** Ours: `normal:int_2_10_10_10`,
  `tangent:int_2_10_10_10`, stride 8. Vanilla's small layout: `blendindex:uint`,
  stride 4. NMSDK chooses this, and whether the engine is happy with it for a
  capital ship slot is unknown.
- **Mesh count.** 20 mesh nodes sharing one geometry buffer.

## The bisect, installed now

`variants/XystonHull_PLAIN/` — hull wedge, superstructure, bridge tower and cannon
housing. **4 meshes, 23 faces**, geometry data 3,319 bytes against 702,591.

No greebles, no spheres, no cylinders, no segmented strips.

| Result in game | Conclusion |
|---|---|
| Renders solid and clean | the fault is in the detail geometry — greeble density, no LOD, or the segmented strips. Reintroduce passes one at a time |
| Still tears | the fault is structural — the scene, the exporter's vertex layout, or the engine's handling of a mesh this size. Adjusting greebles would have been wasted effort |

Either answer is worth more than more guessing. Set `XYSTON_DETAIL=plain` to rebuild
it; unset for the full ship.

---

## The bisect answered it: mixed path separators

The 23-face plain hull rendered as **nothing at all**. That ruled out greeble
density, LOD and every other detail-geometry theory in one launch, and pointed
straight at something structural.

Diffing the scene's node attributes against vanilla found it immediately:

```
vanilla  GEOMETRY  MODELS\COMMON\SPACECRAFT\INDUSTRIAL\CAPITALFREIGHTER_PROC.GEOMETRY.MBIN
ours     GEOMETRY  MODELS/COMMON/SPACECRAFT/INDUSTRIAL\CAPITALFREIGHTER_PROC\CAPITALFREIGHTER_PROC.GEOMETRY.MBIN
```

**Mixed separators.** NMSDK keeps whatever separator it is handed for
`export_directory` and `NMSMesh_props.material_path`, then joins the rest with
backslashes. Both were passed with forward slashes, so every geometry and material
reference in the scene was a hybrid the engine cannot resolve.

Vanilla scenes are backslash throughout.

- **Unresolvable GEOMETRY path → the mesh data never loads → the ship is invisible.**
- **Unresolvable MATERIAL path → no texture → this is also the likely cause of the
  black, untextured hull**, which had been blamed on lighting and then on normals.

### Fixed

`_backslash_paths()` rewrites every value containing `MODELS` and a forward slash,
during the MBINCompiler round trip that was already happening for the GUID. It
reports how many it changed — 6 on the plain build, **22 on the full ship**.

### What this says about the earlier screenshots

The torn, shredded ship was most likely never a torn mesh. With the geometry
reference broken, what rendered was whatever the engine could still resolve, which
is why it looked like fragments floating in the silhouette of a Star Destroyer
rather than a damaged hull.

That also means the normals fix, the texture-tile fix and the scale change were all
made while the model could not load properly. They were real bugs and worth fixing,
but none of them could have been evaluated until this one was found.

---

## Still invisible after the path fix — the scene's own identity was wrong

Backslashes alone were not enough. Comparing the installed scene against vanilla
field by field found a second, deeper fault:

| | Scene `Name` |
|---|---|
| vanilla | `MODELS\COMMON\SPACECRAFT\INDUSTRIAL\CAPITALFREIGHTER_PROC` |
| ours | `MODELS\COMMON\SPACECRAFT\INDUSTRIAL\CAPITALFREIGHTER_PROC\CAPITALFREIGHTER_PROC` |

**NMSDK always nests its output in a folder named after the scene**, so the scene
declared itself one level deeper than it actually sits, and its `GEOMETRY` attribute
pointed into that same phantom subfolder.

The scene's `Name` is its identity to the engine. The file was at the right path on
disk, so the game found and loaded it — which is why the stock freighter never came
back — but everything it referenced internally pointed somewhere that does not exist.

### Vanilla's actual layout

    INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN
    INDUSTRIAL/CAPITALFREIGHTER_PROC.GEOMETRY.MBIN.PC        <- beside the scene
    INDUSTRIAL/CAPITALFREIGHTER_PROC.GEOMETRY.DATA.MBIN.PC   <- beside the scene
    INDUSTRIAL/CAPITALFREIGHTER_PROC/<materials>             <- only materials nest

Geometry sits **beside** the scene. Only materials live in the subfolder. Ours had
the geometry in the subfolder, matching the broken internal reference.

### Fixed

- The round trip collapses the doubled `CAPITALFREIGHTER_PROC\CAPITALFREIGHTER_PROC`
  segment, correcting both `Name` and `GEOMETRY` at once. Material paths are left
  alone — those legitimately nest, in vanilla too.
- `tools/install_freighter.py` now owns the layout, lifts the geometry out of the
  subfolder, and **verifies every file after copying**, including failing if any
  geometry is left in the subfolder.

Verified against vanilla after install: `Name` identical, `GEOMETRY` identical, the
referenced geometry file present at that exact path, no forward slashes remaining.

### Why hand-installing had to stop

Three separate install faults in this project — a glob that missed the geometry
index, geometry in the wrong folder, and a scene naming itself wrongly — none of
which were visible in a directory listing. The install step is now code that checks
itself.
