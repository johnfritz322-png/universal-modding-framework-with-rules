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
