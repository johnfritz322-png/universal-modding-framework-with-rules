# John DLSS Safe Lab for Dawnwalker

This is the safe version of the DLSS 5 one-click idea.

It intentionally does not install leaked DLSS 5 Neural Rendering files:

- `renodx-dlss5.addon64`
- `nvngx_dlssnr.dll`

Those files are closed-source/community-distributed and cannot be guaranteed
safe. This package keeps the useful parts of the approach: audit, backup,
version tracking, and official-only NVIDIA DLSS Super Resolution updates.

## What This Can Do

- Audit DW's active graphics/runtime folder.
- Hash and version the NVIDIA/ReShade/UE4SS/upscaler files already present.
- Flag unofficial DLSS 5 Neural Rendering files if they appear.
- Back up the current DW DLSS runtime before changing it.
- Install only `nvngx_dlss.dll` from NVIDIA's public DLSS SDK demo archive.

## What This Cannot Do

- It cannot create real native DLSS 5 Neural Rendering support by itself.
- It cannot make leaked binaries safe.
- It cannot guarantee more FPS than the current performance profile.

## Paths

DW game:

```text
D:\steam\steamapps\common\The Blood of Dawnwalker
```

DW DLSS Super Resolution DLL:

```text
D:\steam\steamapps\common\The Blood of Dawnwalker\Engine\Plugins\Runtime\Nvidia\DLSS\Binaries\ThirdParty\Win64\nvngx_dlss.dll
```

Official NVIDIA SDK archive downloaded during research:

```text
C:\Users\johnf\Documents\Codex\Dawnwalker-Modding\tools\nvidia-dlss-sdk\ngx_dlss_demo_windows_v310.7.0.zip
```

## Use

Audit first:

```powershell
powershell -ExecutionPolicy Bypass -File .\audit-dw-dlss.ps1
```

Official DLSS Super Resolution update test:

```powershell
powershell -ExecutionPolicy Bypass -File .\install-official-dlss-sr.ps1 -OfficialDlssSdkZip "C:\Users\johnf\Documents\Codex\Dawnwalker-Modding\tools\nvidia-dlss-sdk\ngx_dlss_demo_windows_v310.7.0.zip"
```

If the game crashes or looks worse, restore the backup named by the installer.
