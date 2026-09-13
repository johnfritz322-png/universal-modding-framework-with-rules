# Diagnosis: the game's StaticMesh serialization differs from stock UE 5.5.4

Two controls, run in the right order this time, isolate the fault precisely.

## Control A — retoc round trip of a working mod: PASSES

`SkillsNoTimeCost` → `to-legacy` → `to-zen` → **chunk-identical**. 113 chunks in,
113 out, same set, same `.utoc` size, same 347-byte stub pak.

This also surfaced the missing ingredient, straight from the tool:

```text
Error: container does not contain FIoChunkId { chunk_type: ScriptObjects }
```

Cooked packages resolve class references through a **script object table** in the
game's `global.utoc`. Point retoc at a directory containing `global.utoc` +
`global.ucas` and it extracts `scriptobjects.bin` (3,837,469 bytes) alongside the
assets; `to-zen` then consumes it. **Every earlier build lacked this.**

## Control B — retoc round trip of the game's own StaticMesh: PASSES

Extracted `L_Sword_Vampiric_01` (blade, scabbard, materials) from the base
container, converted straight back, installed. **Blade renders normally in game.**

So retoc is faithful for StaticMesh, and the container path is sound.

## Therefore the fault is our cook

With both controls passing, the only remaining variable is the asset body, which
is written by the cooker — not by retoc. The crash names it exactly:

```text
StaticMesh L_Sword_Vampiric_01: Serial size mismatch:
Expected read size 17488, Actual read size 18589
```

The game's reader consumed **1,101 bytes more** than our package declared. Its
engine expects fields in `UStaticMesh` that stock UE 5.5.4 does not write — the
crash path is `G:\BuildAgent\...\depot\main\...`, a custom build, and the game's
own mesh deserializes fine.

**Stock-UE-cooked StaticMesh will not load in this game.** That is the wall, now
located precisely rather than inferred.

## Routes from here

1. **Geometry swap into the game's own package.** Take the extracted legacy
   `L_Sword_Vampiric_01.uasset`/`.uexp`, replace only the vertex and index
   buffers with ours, keep every other byte. The structure stays the game's, so
   its reader stays happy. Bounded binary work on a documented layout, and the
   most likely route to actually succeed.
2. **Match the engine build.** Cook with the game's own engine. We do not have it.
3. **Avoid new StaticMesh entirely.** Reuse meshes the game already ships — no
   custom geometry, which defeats the goal.

Route 1 is the one worth attempting.

## What is now proven and reusable

- retoc works on this game **when given the global container**: point it at a
  directory holding `global.utoc`/`global.ucas` plus the target.
- The base container needs `-a <key>` **before** the subcommand, and a clean
  hardlink view of the Paks folder — `DualSenseAtlas` has a different TOC version
  (`PartitionSize` vs `ReplaceIoChunkHashWithIoHash`) and breaks the composite.
- Extraction and repacking of real game assets both work end to end.
