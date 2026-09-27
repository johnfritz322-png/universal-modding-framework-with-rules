# Combined Death Star freighter progress

Updated 2026-09-26, America/Denver.

This is a consolidated reading of the Claude review handoff and the later
Codex checkpoints in this checkout. Where older notes conflict with later
tested evidence, the later evidence controls.

## Current overall state

**Designed; original exterior geometry pipeline verified; not yet an
installable or in-game-tested mod.**

The intended result is an exterior-only Death Star-style reskin of the
existing S-class freighter **Mothership**. Its class, stats, crew, name,
interior, and functional hangar must remain unchanged.

## Combined progress

- **Target identified, read-only:** Both live save records identify
  Mothership as the industrial capital-freighter scene
  `CAPITALFREIGHTER_PROC.SCENE.MBIN`, with seed `0x89D78FF0C1755CDC`. No save
  was changed.
- **Design completed:** The shell is specified as a full spherical envelope
  around the long wedge donor, with an offset concave dish, an equatorial
  trench, dense panel treatment, and a hangar opening within the trench.
- **Toolchain repaired and checked:** Blender 5.0.1 with the isolated NMSDK
  profile loads the extension and supports the tested import/export workflow.
  The actual capital-freighter root imports and exports from a read-only
  dependency closure.
- **Original model path verified:** A custom spherical shell successfully
  exports through NMSDK and re-imports. Later scratch stages add the dish and
  trench (stage 1), panel relief (stage 2), and a visual-only aperture aligned
  to the measured hangar direction (stage 3).
- **Scratch archive path verified:** The stage-3 custom-model files were
  packed and byte-for-byte revalidated after extraction. This archive does
  not contain selection mapping, collision, stock-scene integration, or
  runtime hangar integration, so it is not installable as a mod.
- **Live stock-freighter evidence captured:** Runtime screenshots verify the
  visible forward bay is on Mothership's live docking approach and that the
  existing stock hangar interior remains present and functional.
- **Diagnostic marker asset verified:** A scratch-only scene with markers at
  the two measured capital-root hangar locations exports and directly reloads
  through NMSDK. It is an observation aid only; it does not establish the
  live hangar attachment transform.

## Reconciled timeline

The Claude review checkpoint established the repaired toolchain, actual
capital-root round trip, and custom-shell export/re-import path. Later Codex
checkpoints then added the staged visual geometry, archive validation, hangar
asset inspection, and runtime screenshots. Earlier wording that said no dish,
trench, or aperture existed is superseded only for the **scratch visual
prototype**; it does not mean those features are game-ready.

## Remaining gates

1. Measure the live runtime attachment: identify the active hangar module,
   its attachment root, and its transform relative to the capital root.
2. Use that measurement to make a docking-safe, collision-aware exterior
   opening. The current stage-3 aperture is visual-only.
3. Prove an architecture for registering/selecting a custom hull, ideally
   without affecting other freighters. A seed-to-custom-hull mechanism has
   not been established.
4. Add materials/collision and build a real mod package only after the above
   evidence is in place.
5. With a fresh verified backup, test one variable at a time in game:
   docking, walking, exit, reload, summon, warp, base behavior, and unchanged
   class/stats/crew.

## Important safety boundary

No game archive, mod installation, or save edit has been performed as part of
this work. Do not treat the scratch mesh or asset-only archive as safe to
install.

## Source records reviewed

- `CLAUDE-REVIEW-HANDOFF-2026-09-25.md`
- `WHATS-NEXT.md`
- `BLENDER-ROUNDTRIP-2026-09-25.md`
- `RUNTIME-ATTACHMENT-EVIDENCE-PLAN.md`
- `SAVE-READONLY-FINDINGS-2026-09-25.md`
- `HANGAR-APPROACH-FINDINGS-2026-09-25.md`
- `HANGAR-ROOT-MARKERS-2026-09-26.md`
