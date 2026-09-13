# Mesh override: mechanism works, mesh crashes — where it stands

Two in-game tests, two crashes, both fully reverted. Stopping here rather than
iterating further on a live install.

## PROVEN: the override mechanism works

This is the significant result. A container in `~mods` publishing a package at an
existing game path **does** replace the game's asset:

- Computed chunk id for `/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01/L_Sword_Vampiric_01`
  **matches the container's chunk id exactly** (`0x6c6099d243341712`).
- `verify_container.py` reports **1 of 519 chunks** colliding — that one, nothing else.
- The game demonstrably loaded our mesh: it crashed *on equipping The Vrakhir*,
  which it does not do without the mod.

So the delivery route is solved. What is not solved is producing a mesh the game
will accept.

## VERIFIED along the way

| Finding | Status |
| --- | --- |
| A legacy `.pak` cannot override an IoStore package | VERIFIED — blade unchanged |
| `UnrealPak -iostore` does not emit containers (either output name) | VERIFIED |
| UAT `-stage -pak -iostore` does emit real containers | VERIFIED |
| UAT drags in ~437 engine packages unless the cook tree is pruned | VERIFIED — pruning `Saved/Cooked/Windows/Engine` drops collisions 465 → 1 |
| The project needs `DirectoriesToAlwaysCook` or UAT cooks none of our content | VERIFIED |

## The crashes

Both `EXCEPTION_ACCESS_VIOLATION` on equip.

**Attempt 1** — mesh imported with no material and no collision. Hypothesis: null
material slot. The original package does reference `MI_L_Sword_Vampiric_01` and
carries `BodySetup`/`NavCollision`, so the reasoning was sound.

**Attempt 2** — shipped our own material (additive, new path) and generated
collision. **Crashed identically.** So the null material was not the cause, or not
the only one.

## The strongest remaining lead: render data, probably Nanite

The size comparison is stark:

```text
game's mesh package : 570,479 bytes  (export only 2,520 - the rest is bulk render data)
our mesh package    :  51,737 bytes  cooked
```

Over half a megabyte of bulk data in the original versus essentially none in ours.
`MeshNaniteSettings` is present in the game's mappings, so this build uses Nanite,
and handing a non-Nanite mesh to a Nanite render path is the best remaining
explanation for an access violation during rendering.

**Not yet tested.** Enabling Nanite from UE Python did not stick — the cook logged
no Nanite activity and the cooked mesh got *smaller*. `nanite_settings` appears to
return a copy, so setting a property on it does not persist to the asset.

## Next step

Enable Nanite so it actually applies, then retest. Options in rough order of
reliability:

1. Set it in the editor UI and re-save the asset, rather than via Python.
2. Find the correct Python call that writes back (possibly
   `set_editor_property` on the whole struct after building a fresh
   `MeshNaniteSettings`, or an `EditorStaticMeshLibrary` helper).
3. Compare a cooked Nanite mesh against a cooked non-Nanite one to confirm the
   bulk-data signature before touching the game again.

Confirm the cooked package size is in the same order as the game's ~570 KB
**before** installing. That is a cheap, offline check and it would have caught
both of the crashes above.

## Safety record

Nothing persists. Both installs were removed within a minute of the crash report,
`~mods` holds only `SkillsNoTimeCost` and the RTX 5080 profile, and no base
archive, executable or save was ever modified. The crashes were on equip, not on
load, and no save was harmed.
