# Where this went wrong, against the project's own rules

Five in-game tests were spent on guesses. Recording the failure honestly, because
the rules that would have prevented it were already written down.

## The rule that was skipped first, and cost the most

> **Look for a working example over an explanation. A mod that demonstrably runs
> outranks any tutorial.** — `feedback_research_gaps_before_guessing`

> **Find something in the shipped game that already does it. If nothing does, treat
> that as evidence the engine cannot.** — `feedback_validate_mechanical_feasibility`

At the very start, a Nexus search for custom-model mods returned **only 2019-era
results**. That was written into `FEASIBILITY-AND-TOOLCHAIN.md` as "custom meshes are
currently a frontier and not a solved path" — and then built on for hours anyway.

**The maintainer's own export documentation was never read.** It sat on disk the
entire time at `work/NMSDK/docs/exporting/exporting.md`, and it names the exact
symptom:

> "When exporting an object it may be exported with edges and faces messed up. This
> happens when the mesh is improperly triangulated. Whilst NMSDK should triangulate
> a mesh properly it sometimes doesn't work as well as it should."

Every face this project builds is a quad. The fix — triangulate before export — is
in that document, with a picture of the failure that matches the in-game screenshot.

## The other rules broken

| Rule | What was done instead |
|---|---|
| **74 / 14 — one variable at a time** | Normals, texture tile and ship scale all changed in a single build. When it still failed, nothing could be attributed |
| **81 — diagnose before fixing** | Fixes were shipped on theories formed from screenshots, then tested by the user |
| **76 — do not repeat a failed action without changing approach** | "Try this, launch the game" five times |
| **64 / 65 — do the work rather than handing the user steps** | The user ran every test. A round-trip check was possible the whole time and was only written at the end |
| **Evidence ladder** | Ran on AI inference when maintainer docs — one rung below shipped game files — were sitting unread on disk |

## What changed

`tools/verify_export.py` imports the installed scene back through NMSDK and reports
mesh count, face count, non-triangular faces, zero-area faces and bounds. It reads
the same files the game reads.

It cannot prove the game renders something. It can prove the file is not obviously
broken — which is a cheaper question, and one that does not cost a launch.

First run caught 48 zero-area faces from the cylinder cap fans. Those are now
dissolved before triangulation.

## Verified state of the current build

| Check | Result |
|---|---|
| Meshes imported | 20 of 20 |
| Faces | 11,204, matching the build exactly |
| Non-triangular faces | 0 |
| Zero-area faces | 0 |
| Bounds | 2,900 x 1,476 x 5,148 — correct for a 4,800 m hull |
| Scene `Name` | identical to vanilla |
| `GEOMETRY` path | identical to vanilla, file present at that path |
| Template GUID | identical to vanilla |
| Normals | every mesh positive signed volume |
| Forward slashes | none |

**This is still not proof it renders.** It is proof that every fault found so far is
absent, which no previous build could claim.
