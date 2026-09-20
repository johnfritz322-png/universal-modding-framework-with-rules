# First time in game — it loads, and it looked bad

2026-09-19. With `DisableAllMods` set to false, the Star Destroyer **rendered in
game** and the game labelled it `YOUR CAPITAL SHIP`. The wedge, the bow blade and
the dorsal greebling were all visible.

It also looked terrible. Three causes, all found by reading the numbers rather than
guessing at the screenshot.

## 1. The texture was stretched about fifty-fold — the big one

UVs are generated in model units and the mesh is then multiplied by `HULL_SCALE`.
`TILE` was a flat `60.0` with no compensation:

    60 model units x HULL_SCALE 4 = 240 m per texture repeat

The borrowed texture is hull *plating*. Plating that repeats every 240 m is not
plating, it is flat grey with a smear on it. That is why the hull read as
featureless despite carrying 5,723 faces of detail.

Now expressed as metres of finished ship and divided by the scale, so the plating
stays the same physical size whatever the ship is set to:

```python
TILE_WORLD_METRES = 5.0
TILE = TILE_WORLD_METRES / HULL_SCALE
```

## 2. 9,600 m was too big to look at

The stock capital freighter is 4,301 m. At 9,600 m the ship fills the whole screen
from any normal viewing distance, so the silhouette — the entire point of a Star
Destroyer — is never visible.

Default dropped to `HULL_SCALE = 2.0`, **4,800 m**, a shade larger than stock.
Variants for 1.0x, 2.0x and 4.0x are staged under `variants/` and swapping is a
folder copy.

## 3. Two build bugs that silently produced broken output

Both failed quietly, which is the dangerous kind.

- **`OUT_DIR` only accepted a path ending in `nmsexport`** and otherwise fell back to
  a home directory. Variant builds therefore wrote nothing where they were expected
  and only failed later, at the copy step. Now reads whatever follows `--`.
- **The staging glob `*.GEOMETRY.*.MBIN.PC` does not match
  `CAPITALFREIGHTER_PROC.GEOMETRY.MBIN.PC`** — the pattern needs a component between
  `GEOMETRY.` and `.MBIN.PC`, and that file has none. So the geometry *index* was
  left out of all three variants while the much larger `.DATA.` file was copied,
  which looks right at a glance. Both files are now copied by name.

## State

Installed: 4,800 m, correct scene GUID, all four files present, mods enabled.

**Not yet seen with any of these fixes applied.** The only thing confirmed is that
the model loads and renders at all.

---

## Second in-game look: normals were inside out

The ship rendered as a near-black silhouette with parts that looked detached.
Testing rather than guessing found the cause.

### 16 of 20 meshes had inward-facing normals

Signed volume is the orientation test that actually works — positive means outward:

| Mesh | Signed volume | Verdict |
|---|---|---|
| `XystonHull` | +326,180,400 | fine |
| `Superstructure`, `BridgeTower`, `AxialCannonHousing` | positive | fine |
| `ShieldGlobePort` / `Starboard` | **-425,544** | every face inward |
| `Engine0`–`Engine4` | **-1,440,267** each | every face inward |
| `AxialCannonMuzzleGlow` | **-204,583** | every face inward |

So `make_sphere` and `make_cylinder` had their winding backwards — the shield
globes, all five engine bells and the cannon muzzle were built inside out. The
hull and every box-built part were correct.

### Why no render ever showed it

**Blender's Workbench engine does not backface cull.** An inside-out mesh renders
exactly like a correct one in every preview produced so far. The game does cull, so
those parts showed their interiors — which is what makes a hull read as black.

### The wrong test, and the right one

Counting faces whose normal points away from the mesh centroid **is not a valid
test** for these meshes. A greeble field is hundreds of separate islands, and
roughly half of any island's faces correctly point towards the middle of the ship.
That test flagged `DorsalGreebles` as 910 of 1,932 "inward" when it was perfectly
fine, and it would have sent the fix in the wrong direction.

Signed volume via the divergence theorem is orientation-correct regardless of
island layout.

### Fixed

`recalculate_normals()` runs `bmesh.ops.recalc_face_normals` on every mesh at
creation, and the build now **asserts positive signed volume per part and aborts**
if any mesh comes out inward. All 20 parts report positive.
