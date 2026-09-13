# retoc attempt — still crashes. Stopping.

`retoc to-zen` produced a structurally correct container and the game still
crashed on equip. Fifth failure. Recording where this stands rather than trying a
sixth.

## What retoc got right

| Check | Result |
| --- | --- |
| Download integrity | SHA256 matched the publisher's published checksum exactly |
| Output shape | `.pak`/`.ucas`/`.utoc` trio |
| Stub pak size | **347 bytes — identical to `SkillsNoTimeCost`'s and `DualSenseAtlas`'s** |
| Collisions | **1 of 1038** — The Vrakhir's blade, nothing else |
| Chunk id | `0x6c6099d243341712` — the exact id for that blade |
| Custom material | rides along additively, no extra collision |

Structurally this is the closest any build has come to matching a mod that
demonstrably works on this install. It still crashed.

## The remaining suspect: script objects

retoc exposes `gen-script-objects` and `print-script-objects`, and its help notes
script-object resolution for imports. A cooked package references classes like
`/Script/Engine.StaticMesh` through indices into a **script object table** that
lives in the global container. Ours was converted without reference to *this
game's* table — `global.ucas` here defines **58,720** script objects, and a stock
UE 5.5 project's set is different.

If those indices do not line up, the package resolves its class references to the
wrong objects, which would fault exactly like this.

**Untested.** The concrete next step would be:

1. `retoc print-script-objects` on the game's `global.utoc` to dump its table.
2. Compare against what our converted package expects.
3. If they differ, regenerate with the game's table (this may need
   `gen-script-objects` and reflection data from the running game, via
   [jmap](https://github.com/trumank/jmap), which is a further dependency).

That is a real lead, not a guess — but it is another substantial piece of work
with no guarantee, and it is where I would stop and hand over.

## Honest tally

Five in-game attempts, five failures, every one reverted within a minute. No save,
base archive or executable was ever modified, and the game is currently running
only the user's own two mods.

What was actually established, and is worth keeping:

- **The override route works** — the game loads our package over its own.
- **Mesh content is not the cause** — a stock engine cube fails identically.
- **Stock-UE-cooked packages are not loadable by this game**, which is the real
  wall and was only found by running a proper control.
- retoc alone does not bridge that gap.

## What I would tell the next person

Do not start by building a custom asset. Start by taking **one of the two mods
that already works on this install**, unpacking it with `retoc to-legacy`,
changing one trivial thing, repacking it with `retoc to-zen`, and confirming it
still works. That establishes a known-good round trip before any new content
exists. Everything above went the other way round, and that is why it took five
failures to learn where the wall is.
