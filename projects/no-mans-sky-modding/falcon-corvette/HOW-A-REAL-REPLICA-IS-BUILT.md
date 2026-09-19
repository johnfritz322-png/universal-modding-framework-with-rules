# How a real Corvette replica is actually built - MEASURED FROM A WORKING ONE

Source: `Millennium Falcon 2.0 (full interior)` by **Hatrin_Gomax**, nomansapp
ID 1815 / sharing code 2931643163, 617 votes, verified. Delivered in-game to the
user 2026-09-18 and measured directly out of the save.

**The build itself is not in this repo.** It is another creator's work, personal
use only, and this repository is public. The raw export lives locally at
`outputs/NMS-Corvette-Exports-20260918/MillenniumFalcon-Hatrin_Gomax-DELIVERED.json`.
What follows is technique, measured from it.

## The headline: 46 structural, 1450 decoration

1496 objects. Only **46** are `^B_*` or the root, and most of those are cosmetic
too (`B_CARRIAGEWHEEL` x15, `B_WALLHANGING*` x13). The genuinely functional
skeleton is about a dozen parts:

`B_LND_A` x3, `B_TRU_A` x3, `B_ALK_C`, `B_ALK_Z_A`, `B_GEN_1`, `B_TUR_C`,
`B_COK_A`, `B_HAB1_C`, plus 2x `U_PARAGON`.

That matches the listing's `Basic:11`. **The ship is a dozen functional parts
wearing 1450 decorations.** Any approach that sculpts the shape out of structural
Corvette parts is working in the wrong category and against a 100-part cap.

## The plating parts that matter

| Part | Count | Role |
|---|---|---|
| `^STORAGEPANEL` | **676** | the primary hull plating - 45% of the entire build |
| `^BUILDFLATPANEL` | 177 | secondary panelling |
| `^L_FLOOR_Q` | **142** | curved quarter floor - this is how round edges are made |
| `^WALLLIGHTBLUE` | **124** | the glowing blue engine band and light runs |
| `^BUILDWORKTOP` | 60 | greebling |
| `^BUILDDECAL2` | 48 | surface decals |
| `^SERVERSTACK` | 41 | greebling |

`^STORAGEPANEL` being the number one shape part is the single most useful fact
here. `^L_FLOOR_Q` does not appear in the user's Corvette-1 at all, so it would
never have been found by mining their existing builds.

## Placement is completely free

| Property | Measurement |
|---|---|
| objects on a 1.5 or 3.0 grid | **17 of 1496 - one percent** |
| scaled objects | **1101 of 1496 - 73%** |
| scale range | 0.25 to 3.00, arbitrary values (1.31, 1.03, 0.41, 1.83, 2.29 ...) |
| distinct `At` directions | **684** |
| axis-aligned `At` | 186 of 1496 - **12%** |
| distinct `Up` directions | **410** |
| tilted (non-vertical) `Up` | **384** |

There is no grid. Rotation is free in three axes, not just yaw - a quarter of the
objects have a tilted `Up`, meaning parts are pitched and rolled to lie flush
against a curved surface. Scales are hand-tuned, not snapped.

## It is much flatter than it looks

| Axis | Range | Size |
|---|---|---|
| X | -19.8 .. 16.1 | **35.9** |
| Y | 0.0 .. 8.5 | **8.5** |
| Z | -16.5 .. 31.2 | **47.7** |

Exactly the advertised 36 x 48 x 8. Note the **height is only 8.5** - a Falcon is
a flat disc. Builds at 12-15 units tall read as a blob, not a saucer.

Note also that X is **asymmetric**: -19.8 to +16.1, not centred on zero. The real
ship is asymmetric and the builder leaned into it rather than mirroring.

## What this says about generating a replica procedurally

Sampling a mathematical surface and laying panels on it produces a smooth
silhouette, not a replica. This build's fidelity comes from ~1450 individually
placed, individually scaled, individually rotated parts - panel lines, vents,
pipes, light runs. That is authored detail, not a swept surface.

If a replica is wanted without a bot delivery, the realistic route is the one the
good builders use: model or import the real mesh in Blender and fit parts to it
with DjMonkey's extension (<https://www.nexusmods.com/nomanssky/mods/984>), which
gives exactly the free translate/rotate/scale this build demonstrates, and exports
through a save editor.

## Getting a build from nomansapp

For the record, since a previous session logged this as an open question: the
public listing returns **metadata and a base64 JPEG preview only**. Verified by
reading the page's own `CurrentCorvetteList` global - fields are Parts, ID,
SharingCode, CreatorDevice, Verified, Description, Timestamp, Name, IsPrivate,
Rating, CreatorPlatform, CreatorName, Image, Size. **No `Objects[]` reaches the
browser.** The layout only ever transfers in-game via the service bot, which needs
the player's friend code and an open multiplayer session. There is no file route.

Charon (<https://charon.gg>) does offer `.nmsship` file downloads with no bot, but
its catalogue of 308 builds contains no Falcon - all 16 of its Star Wars ships were
checked.
