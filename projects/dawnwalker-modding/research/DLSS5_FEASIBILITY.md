# DLSS 5 Feasibility for The Blood of Dawnwalker

Checked: 2026-09-05

## Verdict

Do not force DLSS 5 Neural Rendering into DW right now.

DW is a good candidate for official DLSS 4.5 tuning, but not for a clean DLSS 5
Neural Rendering mod yet. NVIDIA's current DLSS 5 feature is 3D-Guided Neural
Rendering, and it is exposed to players as a game option when the developer has
integrated it. NVIDIA lists NBA 2K27 as the debut title.

For DW specifically, NVIDIA lists support for DLSS Super Resolution and says it
can be upgraded to DLSS 4.5 through NVIDIA App. NVIDIA does not list DW as a DLSS
5 Neural Rendering title.

## Local DW Findings

Installed game:

`D:\steam\steamapps\common\The Blood of Dawnwalker`

Executable:

`D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker\Binaries\Win64\Dawnwalker.exe`

Version:

`dw1-pc-257186-shipping-patch2-all-CL-257186`

Bundled NVIDIA runtime files:

| File | Installed version |
|---|---|
| `nvngx_dlss.dll` | `310.2.1.0` |
| `nvngx_dlssd.dll` | `310.2.1.0` |
| `nvngx_dlssg.dll` | `310.2.1.0` |
| `sl.common.dll` | `2.7.30.0` |
| `sl.dlss_g.dll` | `2.7.30.0` |
| `sl.reflex.dll` | `2.7.30.0` |

No local `nvngx_dlssnr.dll` or obvious DLSS Neural Rendering runtime file was
found in the DW install.

User config has:

`C:\Users\johnf\AppData\Local\Dawnwalker\Saved\Config\Windows\GameUserFramegen.ini`

Current values:

```ini
[/Script/RebelFramegenInitModule.RebelFramegenSettings]
Provider=2
Mode=0
```

## What Is Practical

1. Clean path: use NVIDIA App's DLSS 4.5 overrides for DW.
   - This is the safest path.
   - It should upgrade Super Resolution model behavior without editing game
     binaries.

2. Controlled experiment: update DLSS/Streamline DLLs from NVIDIA's public SDK
   package with backups.
   - DW currently has NGX `310.2.1` and Streamline `2.7.30`.
   - NVIDIA's July 2026 UE plugin package lists DLSS 4.5 with SL `2.11.1` and
     NGX `310.6.0`.
   - The public NVIDIA DLSS GitHub has newer SDK tags, including `310.7.0`.
   - This might improve DLSS behavior, but it cannot add true DLSS 5 Neural
     Rendering if the game does not call that feature.

3. Risky path: community injection / OptiScaler-style Neural Rendering hooks.
   - Not recommended yet for this game.
   - It would be experimental, could crash, and may not use proper game-side
     masks/material data.
   - It is not a clean "install DLSS 5" mod.

## Sources

- NVIDIA DLSS 5 launch article: https://www.nvidia.com/en-us/geforce/news/dlss-5-3d-guided-neural-rendering/
- NVIDIA article listing DW DLSS support: https://www.nvidia.com/en-us/geforce/news/star-wars-zero-company-aliens-fireteam-elite-blood-of-dawnwalker-dlss/
- NVIDIA DLSS technology page: https://www.nvidia.com/en-us/geforce/technologies/dlss/
- NVIDIA App DLSS overrides: https://nvidia.custhelp.com/app/answers/detail/a_id/5620/
- NVIDIA DLSS developer page: https://developer.nvidia.com/rtx/dlss
- NVIDIA DLSS SDK releases: https://github.com/NVIDIA/DLSS/releases
