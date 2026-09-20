# What the Falcon's entrance actually is, and the alternatives

Asked to swap the drop-down elevator for stairs, or something tucked away and less
visible. Answered from game data on 2026-09-19, game 7.03.1.

## The entrance fitted to the Falcon is the lift — VERIFIED

The save has `B_ALK_C` at (0, 3, -6). Each airlock variant's mechanism is given away
by the entity files shipped beside its model in
`models/common/spacecraft/biggs/modules/parts/`:

| Part | Entities present | Mechanism |
|---|---|---|
| `B_ALK_A` | `rampdata`, `shipaccesswaydata` | plain ramp |
| `B_ALK_B` | `rampdata`, `rampphysics`, `rampcontrols`, `shipaccesswaydata` | powered ramp with controls |
| **`B_ALK_C`** | **`liftdata`**, `shipaccesswaydata` | **lift — the drop-down elevator** |
| `B_ALK_D` | **none at all** | flush hatch, no moving part |

So the thing being complained about is `liftdata` on `B_ALK_C`.

## Three ways out of it

### 1. Swap to `B_ALK_A` — no mod needed

`B_ALK_A` is a plain ramp with no physics and no control panel, the simplest of the
three working entrances. It is already category `Access`, so it is already in the
ship builder. This is a straight in-game part swap and carries no risk.

### 2. `B_STAIRS0` — already available

A Corvette interior stairs part, category `Interior`, `IsCraftable` true, icon
`BIG_STAIRS0.DDS`. Already buildable. This is interior deck-to-deck stairs, not an
exterior entrance, so it complements an entrance rather than replacing one.

### 3. `B_ALK_D` — the flush hatch Hello Games did not expose

`B_ALK_D` and `B_ALK_Z_D` have a complete model, geometry, animation, materials and
a placement scene, but their `CorvettePartCategory` is `None`, so the build menu
never lists them. Setting it to `Access` unlocks them.

**Risk, stated plainly: `airlock_nesw_d` has no `entities` folder at all.** A, B and
C each ship `shipaccesswaydata.entity.mbin`, which is almost certainly what registers
a part as a working way in. D has no such file. It may therefore be a decorative or
unfinished hatch that looks right and cannot be entered through. Its material list
includes `hangermat`, which hints it belongs to a hangar door rather than a personal
airlock.

**Try it, but keep `B_ALK_A` as the fallback.**

## The mod — BUILT AND INSTALLED, NOT TESTED

`mods/CorvetteExtras/` replaces the earlier `CorvetteTeleporter` folder; both edit
the same table, so only one may be installed. It now makes three changes, all of them
the same single field:

| Part | Was | Now | Purpose |
|---|---|---|---|
| `TELEPORTER` | `None` | `Interior` | build a teleporter aboard |
| `B_ALK_D` | `None` | `Access` | unlock the flush hatch |
| `B_ALK_Z_D` | `None` | `Access` | unlock its Z variant |

EXML partial patch, 900 bytes. Readback of the equivalent full rebuild confirms all
1,820 products intact, the three changes applied, and the controls untouched
(`B_ALK_C` still `Access`, `BUILDSAVE` still `None`).

Every change reuses a vanilla part id, so uninstalling the mod cannot orphan anything
already placed.
