# Freighter selection follow-up — 2026-09-25

## Scope and highest verified result

Read-only investigation of the installed Steam build `25441199` (confirmed in `D:\Steam\steamapps\appmanifest_275850.acf`, line 13). Repository context: `origin/claude/death-star-freighter-mod-iteration` at `2a57866`. Read `AGENTS.md` and `UNIVERSAL_MODDING_RULES.md` before investigation.

**VERIFIED — Primary:** the current game contains a capital-freighter scene, its procedural descriptor, and an AI model-ID-to-scene mapping. **UNVERIFIED:** a direct save-seed-to-custom-hull lookup table, additive custom registration, and a personal-only replacement affecting Mothership. No mod, game installation, save, or repository file was changed by this investigation. Extracted assets remain private local scratch files and must not be committed or redistributed.

## Corrected asset paths

| Game-relative path | Source archive | Evidence |
|---|---|---|
| `METADATA/SIMULATION/SPACE/AISPACESHIPMANAGER.MBIN` | `NMSARC.Precache.pak` | Extracted, decompiled, parsed, and no-edit round-trip passed |
| `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.DESCRIPTOR.MBIN` | `NMSARC.Precache.pak` | Extracted, decompiled, parsed, and no-edit round-trip passed |
| `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN` | `NMSARC.EntitySceneMBIN.pak` | Fresh extraction matched previous scratch extraction; decompiled and parsed |
| `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.GEOMETRY.MBIN.PC` | `NMSARC.MeshCommon.pak` | Verified archive inventory entry; existing scratch file also present |
| `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.GEOMETRY.DATA.MBIN.PC` | `NMSARC.MeshCommon.pak` | Verified archive inventory entry; existing scratch file also present |

The archive list was freshly generated for **all 97 `.pak` files** in the installed `PCBANKS` folder. Descriptor files were missed by the earlier narrow archive search because they reside in `NMSARC.Precache.pak`. This is a concrete example of the repository's rule that a null search is not proof of absence.

## BIGGS is explicitly a Corvette

The decompiled `AISPACESHIPMANAGER.MXML` is `cGcAISpaceshipManagerData`. Its `ShipModels` entries provide the following literal mappings:

| ID | Scene | ShipClass | AIShipRole |
|---|---|---|---|
| `BIGGS` | `MODELS/COMMON/SPACECRAFT/BIGGS/BIGGS.SCENE.MBIN` | `Corvette` | `Biggs` |
| `FREIGHTER` | `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/FREIGHTER_PROC.SCENE.MBIN` | `Freighter` | `Freighter` |
| `FREIGHTER_CAPTIAL` | `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN` | `Freighter` | `CapitalFreighter` |
| `FREIGHTER_CAPITAL_PIRATE` | `MODELS/COMMON/SPACECRAFT/INDUSTRIAL/PIRATEFREIGHTER.SCENE.MBIN` | `Freighter` | `CapitalFreighter` |

`FREIGHTER_CAPTIAL` is the game's actual spelling and must be preserved. This data identifies the capital-freighter model family; it does not identify Mothership's specific save record or visually prove which procedural branch is its Venator-shaped hull.

Local evidence: `decompiled-space/aispaceshipmanager.MXML`, lines 122–130 (BIGGS), 278–286 (ordinary freighter), 330–338 (capital), 343–351 (pirate).

## Procedural descriptors, not a demonstrated seed lookup

`CAPITALFREIGHTER_PROC.DESCRIPTOR.MXML` is a `cTkModelDescriptorList`. It contains nested `TkResourceDescriptorList` / `TkResourceDescriptorData` entries with `TypeId`, `Id`, `Name`, `ReferencePaths`, `Chance`, and `Children`.

The outer `_HULL_` group contains `_HULL_A3` / scene node `_Hull_A3`; inside are `_HULL_A1` and `_HULL_A2` branches. Evidence anchors: descriptor line 6 (`TypeId`), line 9 (`_HULL_A3`), line 21 (`_HULL_A1`), line 418 (`_HULL_A2`). The scene contains the corresponding named nodes.

An XML property-name check found zero `Seed`-named properties in the parsed capital descriptor and AI spaceship manager. This is bounded evidence about these two files, not a claim that seeds are unused or that no selection logic exists elsewhere. The exact seed interpretation, deterministic choice algorithm, custom scene registration, and isolation to an owned freighter are **UNVERIFIED**. The observed schema does not establish that adding one table row and changing a seed can select an independently added hull.

## Hangar anchors found, behavior not yet tested

The capital scene contains two empty `LOCATOR` nodes with these **local** transforms:

| Node | Ancestry below model root | Translation X, Y, Z | Uniform scale | MXML line |
|---|---|---|---|---|
| `HANGARROOTA` | `_Hull_A3 / _Hull_A1 / _CargoC_A1` | `0, 37.7356262, -49.3183823` | `0.166667` | 1904 |
| `HANGARROOTB` | `_Hull_A3 / _Hull_A2` | `0, 184.557900, -61.516370` | `0.333333` | 4385 |

Both have zero local rotations and empty `Attributes` and `Children`. Their names and hierarchy make them concrete inspection targets. These values are not world coordinates or verified docking-mouth positions. Runtime attachment behavior, accumulated ancestor transforms, collision, approach paths, and which anchor Mothership uses remain untested.

## Validation and hashes

Tool versions: HGPAKtool `1.1.3`; MBINCompiler output banner/MXML header `7.03.2.1` (log formatting `7.3.2.1`). A private copy of the existing compiler executable was used in this scratch directory for conversions.

| Extracted MBIN | SHA-256 |
|---|---|
| Capital descriptor | `B95359386AB53249155F1F49436CF0271C9C912B060A725755CAB3160CAC4D8C` |
| AI spaceship manager | `D6F998F53EAADA562B2CACB513192CD9CDE3F0068669E3B51AC2C1A93A1DB65B` |
| Capital scene | `9370DC1E67589FF35190359FE9A65D5320D2B199B9E7E86E1A24A3AD0DC30A62` |

No-edit `MBIN → MXML → MBIN → MXML` checks passed for both the capital descriptor and AI spaceship manager. Initial and re-decompiled MXML SHA-256 hashes were identical:

- Capital descriptor: `6DE9CE69D672B8971D28F9B6F2DFDF13AFD8F94FBEB68E0DB3D8B998709A4D6D`
- AI spaceship manager: `66557A457E7A7FD35DDFD4B7287803C1770C1703ACE94F6953B70A3D9EFAAE30`

This validates no-edit conversion for these two files; it is not in-game or universal toolchain compatibility proof.

One exploratory extraction also requested `METADATA/REALITY/DEFAULTREALITY.MBIN`. Although listed in the Precache inventory, HGPAKtool raised `FileNotFoundError: The specified file path ('metadata/reality/defaultreality.mbin') doesn't exist in this pak` and left a zero-byte scratch file. That failed file was not used as evidence. A subsequent narrowly selected extraction of the two required files completed successfully: `Unpacked 2 files from 1 .pak's`.

## Reproduction

Run in `C:\Users\johnf\Documents\Codex\2026-09-24\why\work\freighter-selection-followup`. The executable help was inspected before extraction; conversion syntax was checked against the maintainer's [README](https://github.com/monkeyman192/MBINCompiler) and [CLI documentation](https://github.com/monkeyman192/MBINCompiler/wiki/User-Documentation). The older wiki's EXML wording does not override this installed compiler's actual MXML output.

```powershell
$freighterPakTool = 'C:\Users\johnf\Documents\Codex\2026-09-07\referenced-chatgpt-conversation-this-is-an\work\nms-toolchain\HGPAKtool-1.1.3\hgpaktool.exe'
$freighterBanks = "D:\Steam\steamapps\common\No Man's Sky\GAMEDATA\PCBANKS"
& $freighterPakTool -L $freighterBanks
& $freighterPakTool -U -O '.\verified-extract' -f 'models/common/spacecraft/industrial/capitalfreighter_proc.descriptor.mbin' -f 'metadata/simulation/space/aispaceshipmanager.mbin' "$freighterBanks\NMSARC.Precache.pak"
& $freighterPakTool -U -O '.\verified-extract' -f 'models/common/spacecraft/industrial/capitalfreighter_proc.scene.mbin' "$freighterBanks\NMSARC.EntitySceneMBIN.pak"
# Use a new output directory or the keep flag when reproducing conversions.
& '.\MBINCompiler.exe' convert -n '--output-dir=.\reproduce-mxml' '.\verified-extract'
& '.\MBINCompiler.exe' convert -n '--output-dir=.\reproduce-roundtrip' '.\reproduce-mxml'
& '.\MBINCompiler.exe' convert -n '--output-dir=.\reproduce-redecoded' '.\reproduce-roundtrip'
```

The actual successful round-trip run selected the two MXML files separately into `roundtrip`, then converted that directory into `roundtrip-redecoded`. The scene was inspected but not part of the reported two-file round-trip pass. `HGPAKtool -L` writes `filenames.json` to the working directory; its `-O` option did not relocate that listing.

## Next bounded gate

Use the actual capital scene, descriptor, and literal AI model ID above for further research. Read Mothership's existing save record to establish its resource filename and seed without editing it. Inspect how that resource and seed connect to these descriptors before selecting an additive or replacement architecture. A known-working mod demonstrating the same personalization on this build would strengthen that architecture evidence; a scene file and model mapping alone do not prove it.
