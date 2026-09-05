# Dawnwalker Modding

Local modding notes and reference files for The Blood of Dawnwalker.

## Game Paths

- Game install: `D:\steam\steamapps\common\The Blood of Dawnwalker`
- Pak folder: `D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks`
- Loose mod folder: `D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Content\Paks\~mods`
- User config folder: `C:\Users\johnf\AppData\Local\Dawnwalker\Saved\Config\Windows`

## Current Scope

This repo is for planning, notes, extracted reference config, and custom mod source.
It should not store the full game files or large copied game archives.

## Custom Profiles

- `profiles/john-rtx5080-quality`: active quality-and-smoothness profile tuned
  for John's RTX 5080, Ryzen 9 5900X, 32 GB RAM, and 4K display.

## Installed Mod References

See `Dawnwalker-Modding-Map.md` for the installed mod list, what each mod appears to change, and the workflow rules for Nexus downloads.

## Where things live

| File | What it is |
|---|---|
| `PROJECT_MANIFEST.md` | **Start here.** Project state, verified vs. unverified, open handoff items |
| `Dawnwalker-Modding-Map.md` | Installed mods, what each one actually changes, install workflow |
| `profiles/john-rtx5080-quality/` | The active performance profile: source, `build.ps1`, `verify.py` |
| `reference/mod42_optimized_tweaks_base/` | Extracted VynnGfx reference mod |
| `../../games/blood-of-the-dawnwalker/` | **Game-level format reference** — see below |

## Game-level format reference

Engine-level facts live under `games/blood-of-the-dawnwalker/`, per the repository
structure in `AGENTS.md` (`games/<game>/` = verified game rules,
`projects/` = individual mod projects):

| File | What it answers |
|---|---|
| `DAWNWALKER_RULES.md` | How the pak / IoStore / Zen formats work, and which of the 5 mod techniques to use |
| `CONFIG_SURFACE.md` | **The 67 shipped settings classes you can mod with no AES key** |
| `KNOWN_LIMITATIONS.md` | What is blocked (AES key, Oodle, `.usmap`) and what is not |
| `SOURCES.md` | How every claim was validated |
| `tools/` | Six dependency-free Python readers for `.utoc`/`.ucas`/Zen/pak |

## Verifying a build

`build.ps1` verifies with repak and UnrealPak — but repak also built the file.
`verify.py` re-parses the package from first principles, recomputes the index
SHA-1, and compares the **installed** package against this repo's source to catch
drift:

```bash
python profiles/john-rtx5080-quality/verify.py
```

Exit code 0 means every check passed.
