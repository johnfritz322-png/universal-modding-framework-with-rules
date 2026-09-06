# DLSS5oneclick Source Audit

Checked: 2026-09-05

Source inspected:

`https://github.com/faisalkindi/DLSS5oneclick`

Local read-only clone:

`C:\Users\johnf\Documents\Codex\Dawnwalker-Modding\research\external\DLSS5oneclick-source`

Commit inspected:

`d6f2801 Put the window on the discrete GPU (0.11.15)`

## Bottom Line

The public installer code is useful, but its DLSS 5 payload is not acceptable for
our clean DW modding path.

The tool's own README says it sets up a leaked DLSS 5 neural-rendering build. It
also states the `renodx-dlss5.addon64` add-on is closed source and has no
published license. Because of that, we cannot make that binary "ours" or
guarantee its safety.

## What We Learned

For a game that already ships DLSS, like DW, the tool uses its native-DLSS path:

- installs ReShade as `dxgi.dll`
- installs `renodx-dlss5.addon64`
- installs `nvngx_dlssnr.dll`
- leaves the game's own `nvngx_dlss.dll` alone when it detects native DLSS
- writes/updates ReShade config
- uses markers/manifests to distinguish files the tool installed from files the
  game or user already had

For games without DLSS, it adds a feeder path:

- ReShade add-on build
- ReShade shader headers
- DLSS5-Feeder
- LumeniteFX motion-vector shaders
- DLSS 5 add-on/model files
- ReShade preset/config wiring

DW is not in that no-DLSS category. DW already has:

- native `nvngx_dlss.dll`
- native `nvngx_dlssd.dll`
- native `nvngx_dlssg.dll`
- NVIDIA Streamline `sl.*.dll` files

## Safe Version For Us

We can copy the good engineering ideas:

- audit first
- write a rollback backup before changing game files
- hash files
- track versions
- refuse unsafe/leaked component names
- only install from public official sources

We should not copy the payload strategy:

- no leaked `renodx-dlss5.addon64`
- no third-party `nvngx_dlssnr.dll`
- no "trust me" binary downloads

## Safe Lab Package

Created:

`mods/john-dlss-safe-lab`

Scripts:

- `audit-dw-dlss.ps1`: scans DW and flags leaked/community DLSS 5 files
- `install-official-dlss-sr.ps1`: backs up and installs only NVIDIA's public
  `nvngx_dlss.dll` from the official DLSS SDK demo archive

Current audit result:

No unsafe/community DLSS 5 files found in DW.

## Official-Only Experiment Available

NVIDIA public DLSS GitHub latest checked:

- `v310.7.0`
- archive: `ngx_dlss_demo_windows.zip`
- contains: `DLSS_Sample_App/bin/ngx_dlss_demo/nvngx_dlss.dll`

DW currently ships:

- `nvngx_dlss.dll` version `310.2.1.0`

So the clean experiment is updating DLSS Super Resolution from 310.2.1 to
310.7.0 with a backup, not installing DLSS 5 Neural Rendering.

## Decision

Do not install the DLSS 5 one-click payload into DW. Use the safe lab for:

1. auditing current files
2. backing up the original DLSS Super Resolution DLL
3. testing official NVIDIA DLSS SDK `nvngx_dlss.dll` only
4. reverting if the game crashes or image quality gets worse
