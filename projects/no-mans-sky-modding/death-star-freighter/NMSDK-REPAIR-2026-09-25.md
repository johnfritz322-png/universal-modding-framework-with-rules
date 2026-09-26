# NMSDK repair and restart checkpoint

Recorded 2026-09-25 UTC (2026-09-24 evening, America/Denver).
Based on canonical project commit `2a57866`; published on
`codex/death-star-nmsdk-fix` for review and incorporation by Claude.

## Result

**PASS — the missing `hgpaktool` import is fixed.** NMSDK enables and
registers its preferences, scene properties, and import/export operators in
Blender 4.5.14. A native extension installation also starts enabled in a new
Blender 5.0.1 process, using a dedicated local profile.

This repair record establishes add-on loading and archive access. Subsequent
work has also verified scratch-only custom-model export and re-import; see
`BLENDER-ROUNDTRIP-2026-09-25.md`. No freighter installation, save edit, or
in-game test was performed. The Death Star mod itself remains **Designed /
scratch geometry verified**, not packaged or tested.

## Cause and exact fix

The standalone HGPAKtool executable does not provide the Python module to
Blender. NMSDK's own `pyproject.toml` requires `hgpaktool`, and its
`src/addon/nmsdk/blender_manifest.toml` bundles
`wheels/hgpaktool-1.1.3-py3-none-any.whl`.

The existing NMSDK checkout remains clean at
`548bfe1766a7506e1e0321323bbf5aaa8b0b97a7`. A live upstream check returned
the same `cosmos_fixes` SHA, so no source update was necessary.

Using **Blender 4.5.14's own Python**, installed that bundled wheel:

```powershell
$base = 'C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work'
$py = "$base\Blender-4.5.14\blender-4.5.14-windows-x64\4.5\python\bin\python.exe"
& $py -m pip --isolated --disable-pip-version-check install --only-binary=:all: --index-url https://pypi.org/simple "$base\NMSDK\src\addon\nmsdk\wheels\hgpaktool-1.1.3-py3-none-any.whl"
& $py -m pip check
```

Installed: `hgpaktool 1.1.3`, `lz4 4.4.5`. Existing `zstandard 0.23.0`
was retained. Pip reported no broken requirements. No system Python or
global PATH was changed. The script-directory-not-on-PATH warning is harmless
for Python imports and was not suppressed.

## Blender version discrepancy and durable setup

This exact NMSDK branch's README says Blender >=4.2, but its extension
manifest says **Blender >=5.0.0** and NMSDK `0.10.0-alpha14`.
The 4.5.14 registration check passes; this is not proof of complete 4.5
compatibility. Use the already-installed **Blender 5.0.1** for subsequent
extension/model tests.

Built the unchanged extension with Blender's `extension build` command,
added local repository `nmsdk_local`, and installed/enabled the zip using
`extension install-file --repo nmsdk_local --enable`. Blender installed the
bundled HGPAKtool wheel into its extension profile automatically. Blender
5.0.1 already had `zstandard 0.23.0`, which supports the tested Windows PAK.

Dedicated profile (preferences, extension source copy, wheel environment):

`C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-blender-profile`

The user's already-running Blender process was left running. The restart
check launched a separate background process using the dedicated profile.
The existing NMSDK source was not patched, and the manifest minimum was not
lowered.

To open this ready-to-use profile later:

```powershell
$base = 'C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work'
$profile = 'C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-blender-profile'
$env:BLENDER_USER_CONFIG = "$profile\config"
$env:BLENDER_USER_EXTENSIONS = "$profile\extensions"
$env:BLENDER_USER_SCRIPTS = "$profile\scripts"
& "$base\nms-toolchain\blender\blender-5.0.1-windows-x64\blender.exe"
```

These variables apply to that shell and its child process. NMSDK module name
in this profile is `bl_ext.nmsdk_local.nmsdk`.

## Verification evidence

Reusable check: `tools/verify_nmsdk_load.py`. Use Blender's
`--python-exit-code 1`, because Blender otherwise returned zero even after
the original Python exception.

- Before repair: `ModuleNotFoundError: No module named 'hgpaktool'`, exit 1.
- After repair, Blender 4.5.14: enable, preferences, scene properties,
  import/export operator registration, PAK access, unregister: **PASS**.
- Blender 5.0.1 with dedicated profile, fresh process and no manual enable:
  **PASS**, `fresh_startup_enabled=true`, exit 0.
- Archive enumerates 42 entries. `gcscratchpadglobals.global.mbin` extracted
  in memory matches the original asset hash from the previous round-trip.
- Deliberately invalid PAK control: rejected with
  `hgpaktool.api.InvalidFileException`, exit 1. No false pass.
- A first draft of the check incorrectly looked for the preferences class
  directly in `bpy.types`. Corrected it to inspect the actual registered
  preferences instance; direct RNA/operator checks also pass.

To repeat the native-profile check, set the profile variables above, then:

```powershell
$project = 'C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-nmsdk-fix\projects\no-mans-sky-modding\death-star-freighter'
$pak = 'C:\Users\johnf\Documents\Codex\2026-09-24\why\work\death-star-toolchain\NMSARC.globals.pak'
& "$base\nms-toolchain\blender\blender-5.0.1-windows-x64\blender.exe" --background --python-exit-code 1 --python "$project\tools\verify_nmsdk_load.py" -- "$base\NMSDK" $pak --module bl_ext.nmsdk_local.nmsdk --require-startup-enabled
```

The script disables the add-on before exiting to check cleanup but does not
save preferences, so the persisted enabled state is retained.

## SHA-256 records

| Artifact | SHA-256 |
|---|---|
| Bundled HGPAKtool 1.1.3 wheel | `9B628AB7117DDB31941FBACCC3BFC0808A93E696359FB05D47D3CEA2736FEBA4` |
| Downloaded lz4 4.4.5 CPython 3.11 Windows wheel | `8A842EAD8CA7C0EE2F396CA5D878C4C40439A527EBAD2B996B0444F0074ED004` |
| Existing Blender 5.0.1 executable | `310AA060203252A10269FF86310D2660FD91D8D6AF6DBBE20CFE1752B3349565` |
| Locally built NMSDK extension zip | `F7D0AAAD092181A718A09E78AA393A419F526F8C011469A11168C46C552CC894` |
| Copied NMSARC.globals.pak | `1D9EC23BA44F843D6CEA71C5B08CAE93AE10A2052944FE84A506B1215DAB5A62` |
| Decoded scratchpad globals asset | `324D4AF5975FA023AD06DDDCBA18A06899EC5B15D35C69341EA0DAEC25A7601D` |

The lz4 wheel hash matched PyPI's published release JSON. Other hashes above
identify the observed local files; they are not claims of publisher signatures.

## Rollback and scope

Blender 4.5.14 changes are limited to newly installed `hgpaktool` and `lz4`
packages in its bundled Python. If rollback is needed, uninstall those two
using the same Python executable; `zstandard` predates this repair and must
be preserved. The 5.0.1 extension/profile is separate and can simply be left
unused. No rollback was performed.

Game build remains `25441199` in the local Steam manifest. No game archives,
mods, saves, default Blender preferences, or source SDK files were edited.

Next steps are in `WHATS-NEXT.md`.
