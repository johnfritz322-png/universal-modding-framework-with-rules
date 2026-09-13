# Control result: the pipeline is the fault, not the mesh

**An `/Engine/BasicShapes/Cube`, duplicated to The Vrakhir's blade path and cooked
through the ordinary pipeline, crashes the game exactly like the custom sword.**

That is the answer the control existed to get, and it redirects everything.

## What it rules out

Every mesh-content hypothesis, all three of which were tested and are now moot:

- null material slot
- missing collision / `BodySetup`
- missing Nanite

A stock engine cube has a material, has collision, and is as ordinary as a mesh
gets. It still crashes. **The problem is not what is in the mesh.**

## What it points to

Our packages are cooked against **our project's** global container and dropped
into a game that loads them with **its own**:

| | ours (staged) | the game's |
| --- | --- | --- |
| `global.ucas` | 2,406,096 B | 3,837,472 B |
| `global.utoc` | 638 B | 374 B |
| script objects | our project's set | **58,720** |

A cooked IoStore package does not carry its dependencies by name — it references
script objects and imports through indices and hashes resolved against the global
container present at cook time. We install only the three mod files and never our
global, so every one of those references is resolved against a table that was
never built for them. For a trivial cube that is still enough to fault.

This also explains why `SkillsNoTimeCost` and `DualSenseAtlas` work: whoever built
them produced packages compatible with **this game's** global data, not a stock
UE 5.5 project's.

**Status: STRONGLY INDICATED, not proven.** The size and script-object mismatch is
concrete; that it is the specific cause of the access violation is inference. What
*is* proven is that mesh content is not the cause.

## What would actually be needed

Cooking in a stock UE 5.5 project and dropping the result into this game does not
produce loadable packages. Closing that gap means one of:

1. **A package rewriter** — convert a cooked package so its imports and script
   references match the game's global container. This is what community tools like
   `retoc` / ZenTools exist for. The earlier note that "retoc has UE5.5 Blueprint
   reserialization risk" was about Blueprints; a static mesh is a far softer case.
2. **Cooking against the game's own data** — feed the game's `global.utoc`/`.ucas`
   and asset registry into the cook so references resolve identically. Hard
   without the game's engine build.
3. **Reusing only assets the game already ships** — no new packages at all, which
   sidesteps the problem entirely but rules out custom geometry.

## Cost of finding this out

Four in-game tests, four failures, all reverted within a minute and none touching
a save or a base archive. Three of them were spent on mesh features that the
control would have eliminated in one run.

**The control should have been the first test, not the fifth.** It is cheap, it
is decisive, and it fails loudly in a way that cannot be misread. That is the
lesson worth carrying more than any of the format details.

## Still true and still valuable

The override *route* is proven — chunk id matches, container collides with exactly
the one intended package, and the game demonstrably loads our file over its own.
The delivery mechanism works. Only the package contents are incompatible.
