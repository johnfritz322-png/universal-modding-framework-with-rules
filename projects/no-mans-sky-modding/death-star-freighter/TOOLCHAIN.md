# Death Star freighter — current toolchain state

Updated 2026-09-25 UTC. Resume from [WHATS-NEXT.md](WHATS-NEXT.md).
Detailed evidence: [NMSDK repair](NMSDK-REPAIR-2026-09-25.md),
[freighter selection findings](FREIGHTER-SELECTION-FINDINGS.md), and the
[earlier sample round trip](TOOLCHAIN-RESULTS-2026-09-25.md).

## Environment

| Item | Observed value | Verified scope |
|---|---|---|
| Game | Steam app 275850, build 25441199; project target Cosmos 7.04 | Installed manifest reread locally |
| Blender 4.5.14 LTS | Python 3.11.15 | Launch and NMSDK registration pass after dependency repair |
| Blender 5.0.1 | Python 3.11.13 | Native NMSDK extension starts enabled in a new process |
| NMSDK | cosmos_fixes at 548bfe1766a7506e1e0321323bbf5aaa8b0b97a7; manifest 0.10.0-alpha14 | Load, operator/preferences registration, unregister pass |
| HGPAKtool | 1.1.3 | Standalone extraction and Blender Python archive access pass |
| MBINCompiler | release-labelled v7.03.2-pre1, MXML version 7.03.2.1 | Same executable hash as earlier check; three specific no-edit round trips pass |

The SDK README says Blender >=4.2, but this branch's extension manifest
requires >=5.0.0. Use the dedicated 5.0.1 profile for further model work;
passing 4.5 registration does not settle general API compatibility.

## Step 1 — installed build: complete

Local manifest: D:\Steam\steamapps\appmanifest_275850.acf, build 25441199.
The earlier game executable timestamp was 2026-09-21 11:17:49 MDT.
Recheck the manifest before future asset work if Steam has updated.

## Step 2 — loading/dependencies: repaired and verified

Blender 4.5.14's bundled Python now has hgpaktool 1.1.3 and lz4 4.4.5.
Existing zstandard 0.23.0 was retained. Pip check passes.

The native extension was also installed into a dedicated Blender 5.0.1
profile. Fresh-process startup enables bl_ext.nmsdk_local.nmsdk, registers
import/export operators and preferences, and decodes a copied Windows
archive asset with the expected hash. The deliberately invalid archive
control fails with InvalidFileException and exit 1.

Exact commands, profile paths, source pins, and hashes are in
NMSDK-REPAIR-2026-09-25.md. No further repair is required for these tested
operations. Actual current-build geometry import/export remains NEEDS TESTING.

## Step 3 — archive reader: verified for tested files

HGPAKtool 1.1.3 extracted copied globals and selected current-build assets.
A fresh filename inventory covers all 97 installed .pak archives. The
freighter descriptor is in NMSARC.Precache.pak, which the earlier narrow
search omitted. No game archive was rewritten.

## Step 4 — no-edit round trips: pass for three named assets

MBIN -> MXML -> MBIN -> MXML produced identical initial and final MXML
hashes for:

- gcscratchpadglobals.global.mbin
- MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.DESCRIPTOR.MBIN
- METADATA/SIMULATION/SPACE/AISPACESHIPMANAGER.MBIN

The capital scene was also decompiled and parsed. Scene export, geometry
export and in-game behavior have not been established by these checks.
A passing sample does not prove every schema in this game build is supported.

## Step 5 — freighter assets: concrete progress, selection unresolved

Verified current-data mapping:

- BIGGS is ShipClass=Corvette.
- The literal ID FREIGHTER_CAPTIAL maps to
  MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN.
- Its descriptor uses nested hull choices. No direct Seed-named property
  was found in the two inspected manager/descriptor files.
- HANGARROOTA and HANGARROOTB are locators in the capital scene. Their
  local transforms and ancestry are recorded in the findings report;
  they are not established docking-mouth world positions.

The exact owned-freighter resource/seed relationship and a personal-only
custom-hull registration mechanism remain UNVERIFIED. Do not implement a
hypothetical seed table merely because the earlier plan named one.

## Step 6 — target save: not started

Identify Mothership's actual save/profile, resource filename and seed fields
read-only. Do not infer this target from Corvette ship slots. Record evidence
locally and avoid publishing private save contents. No save write is part of
this toolchain checkpoint.

## Next validation gate

Use the 5.0.1 profile to prove a minimal scene import/export on copies while
preserving functional nodes. Establish selection behavior and the exact
target before building or installing the Death Star exterior. Backups and
controlled in-game tests remain required before any install/save mutation.
