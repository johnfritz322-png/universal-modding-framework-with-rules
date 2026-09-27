# Claude review handoff — Death Star freighter

Recorded 2026-09-25, America/Denver. This file is a review map, not a claim
that the mod is ready to install.

## Primary project checkout

`C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-nmsdk-fix`

Review branch: `claude/death-star-freighter-mod-iteration`.

Latest pushed checkpoint: `58703b0 Validate original Death Star shell export
path`. The preceding related checkpoints are `abd1e3d`, `3941f85`, and
`48ebbb0`.

Start with:

- `projects/no-mans-sky-modding/death-star-freighter/BLENDER-ROUNDTRIP-2026-09-25.md`
  — full tested evidence, boundaries, donor measurements, and local fixes.
- `projects/no-mans-sky-modding/death-star-freighter/PROJECT_MANIFEST.md`
  — current status and explicitly unverified areas.
- `projects/no-mans-sky-modding/death-star-freighter/WHATS-NEXT.md`
  — next bounded work.
- `projects/no-mans-sky-modding/death-star-freighter/SAVE-READONLY-FINDINGS-2026-09-25.md`
  — read-only current owned-freighter evidence.

## Local NMSDK patch checkout

`C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work\NMSDK`

Local branch: `codex/cosmos-instance-transforms`, clean at `390ef27`.
These commits are local only and were not pushed upstream:

1. `2d8c239 Provide empty instance transforms during scene export`
2. `19f467a Retain regular mesh indexes during export`
3. `390ef27 Use final triangle indexes in export metadata`

The rebuilt extension is installed only in this dedicated profile:

`C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-blender-profile`

## Reproducible scratch evidence

All paths below are disposable scratch work; none is a mod package, game
archive, or save.

- Capital dependency closure:
  `C:\Users\johnf\Documents\Codex\2026-09-25\sav\work\capital-dependency-closure`
- Capital root round-trip export:
  `C:\Users\johnf\Documents\Codex\2026-09-25\sav\work\capital-roundtrip-industrial`
- Final original-shell export:
  `C:\Users\johnf\Documents\Codex\2026-09-25\sav\work\death-star-shell-probe-final`
- Scratch scripts:
  `C:\Users\johnf\Documents\Codex\2026-09-25\sav\work\measure-capital-root.py`,
  `build-death-star-shell-probe.py`, and `debug-exported-shell-import.py`.

## Verified state

- The owned `Mothership` save record was read only; no save was changed.
- The current capital-freighter root imports and exports under Blender 5.0.1
  with the local NMSDK compatibility fixes.
- A new, original low-poly spherical shell exports and loads back through
  NMSDK after the exporter metadata repairs.

## Still not done

No dish, trench, hangar opening, custom material, collision, mod package,
selection-table registration, game installation, or in-game test exists.
Do not infer boardability or save safety from the mesh-pipeline checks.
