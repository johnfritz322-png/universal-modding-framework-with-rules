# Runtime attachment evidence plan — 2026-09-25

## Purpose

Establish the one missing fact that static assets cannot provide: which active
hangar scene attaches to Mothership's capital-freighter root, at which root,
and with which world transform. This is an evidence-gathering plan, **not** an
instruction to alter the save or install the current visual prototype.

## Preconditions

- Start from the known Mothership save record: resource
  `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN`, seed
  `0x89D78FF0C1755CDC`.
- Take and retain a fresh, timestamped backup of the complete target save
  before any in-game or mod-folder experiment.
- Keep the stage-3 shell out of the game. Its aperture is visual-only and has
  no verified collision, attachment, or docking behavior.
- Change one variable per test and preserve the exact package, log, and
  screenshot/video evidence for any test that is run.

## Minimal evidence target

The target result is a captured runtime view or instrumented trace that ties
all three facts together:

1. The stock capital root used by Mothership.
2. The active hangar scene selected by the running game.
3. Its attached root, position, and orientation relative to that capital root.

Static inspection has already verified both candidate engine-configured scene
paths and the capital `HANGARROOTA`/`HANGARROOTB` locators. It has **not**
verified their runtime bridge, so a result that only re-reads scene files does
not clear this gate.

## Safe test order

1. Launch the unmodified game with the backed-up save and capture an approach
   and landing sequence for Mothership. Record game build, save timestamp, and
   whether the interior/loading transition uses the current hangar module.
2. If an asset-inspection or debug-overlay method is available, make it
   identify only the active root/module pair. Do not replace geometry, change
   seed values, or ship a Death Star package in this test.
3. Repeat the same approach once with that single diagnostic change. Compare
   the captured result to step 1 and retain the log/screenshots together.
4. Only after the attached transform is measured may a shell opening be sized
   against the verified approach grid with explicit clearance. Then create a
   separate backup before a first installable package test.

## Pass / fail interpretation

- **Pass:** evidence names one active module and one root and permits a
  reproducible transform from module-local approach points to capital-root
  space.
- **Fail / inconclusive:** the module or transform is absent, ambiguous, or
  differs between loads. Keep the current shell prototype scratch-only; do not
  infer clearance from locator names or a visual render.

## Current status

Two runtime exterior screenshots were captured on 2026-09-25 with Mothership
summoned. Together they visibly confirm the expected stock dorsal spine,
bridge area, tall fin structures, long wedge envelope, and stern engine bank,
consistent with the verified industrial capital donor. The hangar mouth is not
visible in either frame, and the screenshots have no transform, module-name,
collision, or docking data. They therefore do not clear the attachment gate.

Consequently, selection mapping, docking, collision, interior transition, and
an installable hangar opening remain unverified.
