# Mesh override build pipeline — what works, step by step

Everything here is verified on build 25232147. Follow it exactly; several
plausible-looking shortcuts do not work and are listed at the end.

## 1. Project setup (once)

`Config/DefaultGame.ini` must force-cook the override tree, or UAT cooks **none**
of it and you get a container full of engine content and nothing of yours:

```ini
[/Script/UnrealEd.ProjectPackagingSettings]
+DirectoriesToAlwaysCook=(Path="/Game/_Dawnwalker")
UsePakFile=True
bUseIoStore=True
```

The project's `Content/` maps to `/Game/`, so an asset at
`Content/_Dawnwalker/Characters/Swords/<Name>/<Name>.uasset` publishes as
`/Game/_Dawnwalker/Characters/Swords/<Name>/<Name>` — the same package name the
game uses, which is what makes the override land.

## 2. Author the asset

`tools/import_override_mesh.py` — imports an OBJ at the target package path,
creates a material at a **new** path (additive, so it does not add a collision),
assigns it to every slot, and enables collision generation.

## 3. Cook only your directory

```bash
UnrealEditor-Cmd.exe <project>.uproject -run=cook -targetplatform=Windows \
  -CookDir="<project>\Content\_Dawnwalker" -unattended -nopause -nosplash
```

## 4. Prune, or you ship 176 MB of engine content

```bash
rm -rf Saved/Cooked/Windows/Engine
rm -rf Saved/Cooked/Windows/<Project>/Content/Maps
rm -rf Saved/StagedBuilds
```

**This is not optional.** Skipping it takes collisions from 1 to 465 — the exact
fault the original audit rejected Codex's build for. The engine directory comes
back on every cook, so prune every time.

## 5. Stage into real containers

```bash
RunUAT.bat BuildCookRun -project=<project>.uproject -noP4 -platform=Win64 \
  -clientconfig=Shipping -skipcook -stage -pak -iostore -skipbuild \
  -nocompileeditor -nocompile -unattended
```

## 6. Verify before installing

```bash
python verify_container.py <staged>.utoc
```

Must report **1 of N chunks** colliding — the package you meant to replace and
nothing else. Also confirm the chunk id matches:

```python
from cityhash64 import package_id
package_id("/Game/_Dawnwalker/Characters/Swords/L_Sword_Vampiric_01/L_Sword_Vampiric_01")
# -> 0x6c6099d243341712, which must appear in the container
```

## 7. Install

Copy the three staged files into `Content\Paks\~mods\` renamed to a common stem,
e.g. `zzz_<Name>_P.{pak,ucas,utoc}`. Game must be closed. Uninstall is deleting
those three files.

## Things that look right and are not

| Attempt | Result |
| --- | --- |
| Legacy `.pak` only | **Never overrides.** IoStore resolves by chunk id; a lone pak is not consulted. Verified in game. |
| `UnrealPak out.pak -create=… -iostore` | Legacy pak, no containers |
| `UnrealPak out.utoc -create=… -iostore` | A pak with a `.utoc` name, byte-identical to the above |
| Hand-splitting an IoStore package into `.uasset`/`.uexp` at the header offset | Malformed package — loads without crashing but renders **nothing**. IoStore uses a Zen summary, not the legacy layout. |
| `StaticMeshEditorSubsystem.set_nanite_settings` | Subsystem is **unavailable in a commandlet**; the call silently does nothing |
| `mesh.build()` | No such method on StaticMesh |
| `get_editor_property("nanite_settings")` then mutating it | Returns a **copy**; assign a fresh `MeshNaniteSettings` back instead |
| Enabling Nanite at all | Cook output **byte-identical** — not the differentiator |

## Debugging notes

`unreal.log` and `print` do not survive the commandlet's stdout pipe reliably.
**Write diagnostics to a file** — that is how the Nanite question finally got a
straight answer (`tools/nanite_probe.py`).
