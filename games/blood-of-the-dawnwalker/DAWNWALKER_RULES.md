# The Blood of Dawnwalker — verified modding rules

Game: **The Blood of Dawnwalker** (Rebel Wolves). Internal codename **Dogwood**.
Platform inspected: Windows / Steam.
Analysis date: **2026-09-04**.

Every claim on this page is labelled on the evidence ladder. "VERIFIED" here means
*parsed out of the shipped files on disk and internally checksum- or
structure-validated* — it does **not** mean tested in game unless it says so.

---

## 1. Environment

| Item | Value | Evidence |
|---|---|---|
| Steam app / build | **3751260 / build `25129649`** | VERIFIED (Steam manifest) — installed 2026-09-04, likely Hotfix 1.0.2. Fingerprint: `projects/dawnwalker-modding/GAME_VERSION.md` |
| Engine | Unreal Engine 5 | VERIFIED (IoStore magic + Zen packages) |
| Engine minor version | likely 5.5 | **ASSUMPTION** — inferred from a build path `UE5\Engine\Source\ThirdParty\libcurl\8.4.0\` in the exe (libcurl 8.4.0 ships with 5.5) plus container-header v4 and TOC v8. No `++UE5+Release-5.x` string exists in the binary. |
| Game root | `<steam>\steamapps\common\The Blood of Dawnwalker\` | VERIFIED |
| Paks dir | `Dawnwalker\Content\Paks\` | VERIFIED |
| Binaries | `Dawnwalker\Binaries\Win64\Dawnwalker.exe` (176 MB) | VERIFIED |
| Engine dir | `<game root>\Engine\` — **at the game root, NOT under `Dawnwalker\`** | VERIFIED |
| Oodle | statically linked; no `oo2core*.dll` anywhere in the install | VERIFIED |
| Content root mapping | `/Game/…` ⇒ `Dawnwalker/Content/…` | VERIFIED (package name in Zen header vs. TOC directory index) |

### Shipped containers

| File | Size | Notes |
|---|---|---|
| `Dawnwalker-Windows.utoc` | 70,109,154 | 778,643 chunks |
| `Dawnwalker-Windows.ucas` | 43,527,831,216 | ~43.5 GB |
| `Dawnwalker-Windows.pak` | 10,732,400,370 | ~10.7 GB |
| `global.utoc` / `global.ucas` | 374 / 3,837,488 | engine script-object table |

---

## 2. Container formats — VERIFIED

### 2.1 Base game container (`Dawnwalker-Windows.utoc`)

```
TOC version      : 8  (ReplaceIoChunkHashWithIoHash)
Chunk entries    : 778,643
Compression block: 262,144 bytes (256 KiB)
Compression      : ['None', 'Oodle']
Container flags  : 0x0b = Compressed | Encrypted | Indexed
Encryption GUID  : all-zero  (default key)
Meta entry size  : 24 bytes
```

**The base game container is AES-encrypted AND Oodle-compressed.**
Proof of encryption: the directory index region is high-entropy and its declared
size is a multiple of 16 (AES block size); parsing it as a plain `FString` mount
point yields a nonsense length of ~1.05 billion. An unencrypted index begins
`0a 00 00 00 2e 2e 2f 2e 2e 2f 2e 2e 2f 00` (`"../../../"`).

Consequence: **reading base game assets requires the AES-256 key.** See
`KNOWN_LIMITATIONS.md`.

### 2.2 `global.utoc` — NOT encrypted, NOT compressed

```
Container flags : 0x00 = None
Chunks          : 1  (ScriptObjects, 3,837,478 bytes)
```

This is fully readable with no key. It contains:

* **54,880 names** (`FNameMap`: count, byte-count, hash version `0xc1640000`,
  8-byte hashes, 2-byte length headers, then packed strings)
* **58,720 script objects** (32 bytes each: `FMappedName ObjectName`,
  `FPackageObjectIndex GlobalIndex`, `OuterIndex`, `CDOClassIndex`)

Parsing consumes exactly 3,837,478 bytes — the declared chunk size — which is the
structural proof the layout above is correct.

**`FMappedName` packs a 2-bit type in the high bits. Mask the index with
`0x3FFFFFFF` before using it.** Without the mask every name resolves to garbage.

---

## 3. The three container/mod shapes — VERIFIED

Three mods were present on this install. They are three *different* techniques.

### 3.1 IoStore asset mod, modern (`00000000_SkillsNoTimeCost_P`)

```
.pak  = 347 bytes  (stub, 0 files — same as the DualSense mod)
.utoc = TOC version 8, flags 0x08 = Indexed  (NOT compressed, NOT encrypted)
.ucas = 313,683 bytes, compression ['None']
chunks = 113  →  112 ExportBundleData + 1 ContainerHeader
```

> **Correction (2026-09-04).** An earlier revision of this page said this mod ships
> no `.pak`. That was a misread of the directory listing — the 347-byte stub **is**
> present. **Both** IoStore mods on this install ship a 347-byte 0-file `.pak`
> stub alongside the `.utoc`/`.ucas`, so treat the stub as required until something
> demonstrates otherwise.

Contents: 112 `DA_Trait_*.uasset` trait data assets
(`/Game/_Dawnwalker/Player/CharacterDevelopment/Traits/DataAssets/…`).

**Key insight — mods do not have to match the base game's flags.** The base game is
Oodle+AES; this mod is plain, uncompressed, unencrypted, and the engine loads it
anyway. Container flags are per-container. You never need to *write* Oodle or AES.

### 3.2 IoStore asset mod, legacy tooling (`zzz_DualSenseAtlas_v1_1_P`)

```
.pak  = 347 bytes, pak version 11, 0 files  (a stub)
.utoc = TOC version 3 (PartitionSize), flags 0x09 = Compressed | Indexed
.ucas = 158,128 bytes, compression ['None','Zlib']
chunks = 5 → 1 ContainerHeader + 3 ExportBundleData + 1 BulkData
```

Replaces the Xbox controller glyph atlas with DualSense glyphs:

| chunk | path |
|---|---|
| 1 | `…/UI/_Unified/Settings/Atlas/Frames/T_Image_Controller_Generic.uasset` |
| 2 | `…/UI/_Unified/Settings/Atlas/Frames/T_Image_Controller_XBOX.uasset` |
| 3 | `…/UI/_Unified/SharedTextures/Controls/Microsoft_Xbox/Textures/Atlas_0.uasset` |
| 4 | `…/UI/_Unified/SharedTextures/Controls/Microsoft_Xbox/Textures/Atlas_0.ubulk` (2,785,280 B) |

The texture is `PF_B8G8R8A8` (read from the package name map) — **uncompressed
BGRA8, not BC7**. The bulk payload declares a 2,097,152-byte first mip = 1024×512×4.

Note this mod does not *add* PlayStation support; it overwrites the Xbox atlas in
place. That is the cheap way to reskin a glyph set.

This mod also proves **Zlib is accepted** for mod containers, which matters a lot:
Zlib is in the Python standard library, so mod containers can be produced and read
with no proprietary codec.

### 3.3 Legacy `.pak` config mod (`~TBODoptimizedTweaksBASE_P.pak`)

```
pak version : 3   (footer is only 44 bytes: magic, version, index off/size, sha1)
index       : offset 8,228, size 210, SHA-1 VALIDATES
mount point : ../../../
files       : 2
```

| file | size |
|---|---|
| `Dawnwalker/A message from VynnGfx.txt` | 365 |
| `Engine/Config/Windows/WindowsEngine.ini` | 7,757 |

The INI is a large `[ConsoleVariables]` / `[/Script/Engine.RendererSettings]` block
(Niagara, streaming, D3D12, Lumen, Nanite, shadow, pak-cache and async-loading
CVars). Author credits Nexus mod `thebloodofdawnwalker/mods/42` (VynnGfx).

This is a cheap mod path: no assets, no key, no IoStore. A plain file-based pak
mounted at `../../../` that drops an INI into `Engine/Config/Windows/`.

### 3.4 Loose user-config override — the cheapest path of all

Not a pak at all. The installed *Better Story Timer* mod is a single file:

```
%LOCALAPPDATA%\Dawnwalker\Saved\Config\Windows\Game.ini
```

```ini
[/Script/Quest.QuestSettings]
DaysToPass=91
```

VERIFIED on disk. `/Script/Quest/QuestSettings` **is present in the shipped
`global.ucas` script-object table** (global index `0x5b782aa1c565ff82`), which is
why that section resolves. The property name `DaysToPass` is **not** verifiable from
`global.ucas` — property names are not stored in the object table — so it rests on
the mod working in practice, not on shipped-data evidence.

Observed detail: that `Game.ini` is marked **read-only** (`-r--r--r--`) on this
install. **HIGH CONFIDENCE** this is deliberate, to stop the game rewriting the file
and discarding the override — standard practice for UE user-config edits.
**NEEDS TESTING** whether it is actually required here.

**This technique is the single biggest opportunity on this game**, because it needs
no key, no tooling, and no assets. See **`CONFIG_SURFACE.md`** for the full list of
**67 settings classes** that shipped in the build and are addressable this way.

### 3.5 Which technique to reach for

| Want to change | Technique | Blocked? |
|---|---|---|
| A gameplay value exposed as a `config` property | §3.4 loose `Game.ini` | No |
| An engine CVar / performance setting | §3.3 pak with `WindowsEngine.ini` | No |
| A texture, mesh, sound, or UI asset | §3.1/§3.2 IoStore container | Yes — needs AES key |
| A cooked data-asset value with no config route | §3.1 IoStore container | Yes — needs AES key **and** a `.usmap` |

---

## 4. File-format reference (all VERIFIED by parsing shipped data)

### 4.1 `FIoStoreTocHeader` — 144 bytes

| off | type | field |
|---|---|---|
| 0 | u8[16] | magic `-==--==--==--==-` |
| 16 | u8 | Version |
| 20 | u32 | TocHeaderSize |
| 24 | u32 | TocEntryCount |
| 28 | u32 | TocCompressedBlockEntryCount |
| 32 | u32 | TocCompressedBlockEntrySize |
| 36 | u32 | CompressionMethodNameCount |
| 40 | u32 | CompressionMethodNameLength |
| 44 | u32 | CompressionBlockSize |
| 48 | u32 | DirectoryIndexSize |
| 52 | u32 | PartitionCount |
| 56 | u64 | ContainerId |
| 64 | u8[16] | EncryptionKeyGuid |
| 80 | u8 | ContainerFlags |
| **84** | u32 | **TocChunkPerfectHashSeedsCount** |
| 88 | u64 | PartitionSize |
| **96** | u32 | **TocChunksWithoutPerfectHashCount** |

> **Trap that cost real time:** the perfect-hash seed count lives at offset **84**,
> not 52. Getting it wrong silently misaligns everything after the compression
> blocks and the directory index parses as garbage — which looks exactly like
> encryption. Verify against a container you *know* is unencrypted (`global.utoc`)
> before concluding a container is encrypted.

Section order after the header:

```
ChunkIds            EntryCount × 12   (u64 id, u16 index BE, u8 pad, u8 type)
OffsetAndLengths    EntryCount × 10   (5-byte BE offset, 5-byte BE length)
PerfectHashSeeds    (version >= 4)    seeds×4 + without×4
CompressionBlocks   BlockCount × 12   (5B offset LE, 3B csize, 3B usize, 1B method)
CompressionMethods  Count × NameLength
SignatureData       only if flags & Signed
DirectoryIndex      DirectoryIndexSize bytes
ChunkMetas          EntryCount × (33 for TOC v3, 24 for TOC v8)
```

`ContainerFlags`: `1=Compressed 2=Encrypted 4=Signed 8=Indexed 16=OnDemand`.

Chunk offsets are in the **uncompressed** address space, so
`first_block = offset // CompressionBlockSize`.

`EIoChunkType`: `1=ExportBundleData 2=BulkData 3=OptionalBulkData
4=MemoryMappedBulkData 5=ScriptObjects 6=ContainerHeader`.

### 4.2 Directory index

```
FString MountPoint
TArray<FIoDirectoryIndexEntry>  {u32 Name, FirstChildEntry, NextSiblingEntry, FirstFileEntry}
TArray<FIoFileIndexEntry>       {u32 Name, NextFileEntry, UserData}
TArray<FString> StringTable
```

`0xFFFFFFFF` is the null link. `UserData` is the **chunk index**.

**The directory index is cosmetic.** In `00000000_SkillsNoTimeCost_P` the index has
exactly one directory (the root) and stores bare filenames like
`DA_Trait_CombatFocus_Kick.uasset` with no path at all — yet the mod works, because
**the engine resolves packages by chunk ID (the package ID hash), not by path.**
Getting the chunk ID right is what matters; the directory index is for tooling.

### 4.3 `FIoContainerHeader` — VERIFIED, tiling-validated

```
u32 Signature = 0x496F436E ('nCoI')
u32 Version                      (2 = OptionalSegmentPackages, 4 = SoftPackageReferences)
u64 ContainerId
TArray<FPackageId> PackageIds    (u32 count, then count × u64)
TArray<u8> StoreEntries          (u32 byte-count, then raw bytes)
…
```

`StoreEntries` for **version 4** is `PackageIds.Num()` structs of **16 bytes**:

```
FFilePackageStoreEntry {
    TFilePackageStoreEntryCArrayView<FPackageId> ImportedPackages;  // b+0  {u32 Num; u32 OffsetToDataFromThis;}
    TFilePackageStoreEntryCArrayView<FSHAHash>   ShaderMapHashes;   // b+8
}
```

> **`OffsetToDataFromThis` is relative to the address of the array-view member
> itself** — so `ImportedPackages` data is at `entry_start + Offset`, and
> `ShaderMapHashes` data is at `entry_start + 8 + Offset`. It is *not* relative to
> the offset field, and not relative to the container header start.

Validation on the shipped `SkillsNoTimeCost` header (112 packages): the imported-
package arrays tile the data region **contiguously and exactly**, 528 refs × 8 B =
4,224 B, ending precisely on the declared `StoreEntries` end offset `0x1b18`. That
exact landing is the proof the layout is right.

Container header **version 2** (used by the older DualSense mod) has a different,
larger entry that still carries export info. Not decoded — not needed, since new
mods should be written as version 4.

### 4.4 Zen package (`.uasset` inside IoStore)

`FZenPackageSummary` — 13 × `uint32` = 52 bytes:

```
bHasVersioningInfo, HeaderSize, Name.Index, Name.Number, PackageFlags,
CookedHeaderSize, ImportedPublicExportHashesOffset, ImportMapOffset,
ExportMapOffset, ExportBundleEntriesOffset, DependencyBundleHeadersOffset,
DependencyBundleEntriesOffset, ImportedPackageNamesOffset
```

Then the local `FNameMap` (same layout as `global.ucas`), then
`u64 BulkDataMapSize` + `FBulkDataMapEntry[]` (32 B each), then the import map
(`u64 FPackageObjectIndex` each), then the export map (**72 bytes** per entry).

`FPackageObjectIndex` top 2 bits: `0=Export 1=ScriptImport 2=PackageImport 3=Null`.
`ScriptImport` values resolve against `global.ucas` — e.g. `0x593115e0cb25f002`
resolves to `/Script/DogwoodCharacterDevelopment/TraitAsset`.

To locate `BulkDataMapSize` robustly, scan forward 8-byte-aligned from the end of
the name map for the `u64` V where `pos + 8 + V == ImportedPublicExportHashesOffset`.

### 4.5 Legacy `.pak`

Footer versions seen: **v3 → 44-byte footer** (magic, version, index offset, index
size, 20-byte SHA-1) and **v11 → 204-byte footer** (adds EncryptionKeyGuid,
bEncryptedIndex, and the compression-method name table). Index SHA-1 validates on
both shipped paks.

Index: `FString MountPoint`, `i32 FileCount`, then per file: name, `u64` offset /
size / uncompressed size, `u32` method, 20-byte hash, (block table if compressed),
`u8` encrypted, `u32` block size. Each file's payload is preceded by a repeat of
that same entry header in the data region.

---

## 5. Game systems (from `global.ucas`) — VERIFIED

27 game-specific `/Script/Dogwood*` modules:

| objects | module | | objects | module |
|---:|---|---|---:|---|
| 917 | DogwoodUI | | 106 | DogwoodDialogue |
| 691 | DogwoodCombat | | 81 | DogwoodAI |
| 544 | DogwoodWorld | | 62 | DogwoodUtil |
| 457 | DogwoodEditor | | 60 | DogwoodGlossary |
| 403 | DogwoodInventory | | 46 | DogwoodAbilitySystem |
| 250 | DogwoodStats | | 31 | DogwoodInventoryEditor |
| 245 | DogwoodSystem | | 28 | DogwoodVampireHunger |
| 243 | DogwoodMap | | 25 | DogwoodAudio |
| 227 | DogwoodQuest | | 22 | DogwoodAnim |
| 195 | DogwoodFocus | | 21 | DogwoodAchievements |
| 156 | DogwoodAutomatedTesting | | 16 | DogwoodAICore |
| 152 | DogwoodCharacterDevelopment | | 12 | DogwoodDialogueEditor |

(plus DogwoodAudioEditor 12, DogwoodDebug 5, DogwoodNanitePrefetch 3.)

`DogwoodEditor` / `DogwoodInventoryEditor` / `DogwoodAutomatedTesting` are present
in the **shipped** build — editor-side reflection data survived the cook. That is a
useful surface for future work.

The story-clock system that both gameplay mods target shows up as
`ETimeCostType`, `GetTimeSegmentCost`, `AddTimeSegments`, `ETimeOfDay`,
`DayNightCycle`, `TimeOfDay`, `SetTimeOfDay`.

---

## 6. Install layout and load order

VERIFIED (observed on disk **2026-09-04 21:52**; this install changes often, so
re-check rather than trusting this snapshot):

```
Dawnwalker/Content/Paks/
├─ Dawnwalker-Windows.{pak,ucas,utoc}          base game
├─ global.{ucas,utoc}                          script objects
├─ zzz_DualSenseAtlas_v1_1_P.{pak,ucas,utoc}   active
├─ BetterStoryTimer-backup-.../                (empty — that mod is a loose Game.ini, §3.4)
├─ DualSenseAtlas-backup-.../
├─ PerformanceTweaks-backup-20260904-213547/   ~TBODoptimizedTweaksBASE_P.pak (retired)
├─ PerformanceTweaks-backup-20260904-215212/   ~JohnRTX5080Quality_P-revision-1.0.pak
└─ ~mods/
   ├─ 00000000_SkillsNoTimeCost_P.{pak,ucas,utoc}   active
   └─ ~JohnRTX5080Quality_P.pak                     active (revision 1.1)

%LOCALAPPDATA%\Dawnwalker\Saved\Config\Windows\
├─ Game.ini              Better Story Timer override (read-only)
├─ GameUserSettings.ini
└─ GameUserFramegen.ini
```

* Mods load from `Content/Paks/` **and** from a `~mods/` subfolder. VERIFIED that
  both locations are in use by installed mods.
* `_P` suffix, `zzz_` / `00000000_` / `~` name prefixes are the authors steering
  alphabetical mount order. **HIGH CONFIDENCE** (standard UE `_P` patch-priority
  and name-ordering behaviour) — **not** verified against this game's loader.
* **Both** IoStore mods ship a 347-byte 0-file `.pak` stub next to the
  `.utoc`/`.ucas`. Treat the stub as required. (An earlier revision of this page
  wrongly said one of them lacked it — see the correction in §3.1.)
* Only **one** performance-tweaks pak should be active at a time; the project keeps
  retired ones in timestamped `*-backup-*` folders inside `Content/Paks/`, which is
  a good rollback pattern (AGENTS.md rule 13).

---

## 7. How to build each mod type

### 7.1 Config / CVar mod — no key, no assets needed. READY TO USE.

Two shapes, both unblocked:

* **Engine CVars / performance** — a legacy `.pak` (version 3), mount point
  `../../../`, containing `Engine/Config/Windows/WindowsEngine.ini`. This is what
  `projects/dawnwalker-modding/profiles/john-rtx5080-quality` builds, and
  `repak pack --version V3 --mount-point '../../../'` produces it.
* **Gameplay values** — a loose `Game.ini` in
  `%LOCALAPPDATA%\Dawnwalker\Saved\Config\Windows\` (§3.4). No packaging at all.

`tools/pak.py` reads and extracts both, and recomputes the index SHA-1, so a built
package can be verified with no dependency on `repak` or `UnrealPak`.

**See `CONFIG_SURFACE.md`** for the 67 shipped settings classes this path can aim
at. That file is the practical answer to "what else can we mod without the key".

### 7.2 IoStore asset mod

Requires the original asset to modify ⇒ requires the AES key ⇒ see
`KNOWN_LIMITATIONS.md`. Once the originals are in hand, the container can be
written with `None` or `Zlib` compression and no encryption (§3.1, §3.2 prove the
engine accepts that), and the container header must be written per §4.3.

### 7.3 What you additionally need to *edit* a cooked data asset

Cooked Zen packages use **unversioned property serialization**: the export payload
begins with a fragment bitstream (`u16` fragments packing SkipNum/ValueNum), and
property *names are not stored*. Decoding requires a **`.usmap` mappings file**
generated from the running game by a dumper such as Dumper-7 or UE4SS.

VERIFIED by inspection of `DA_Trait_CombatFocus_Kick.uasset`: the name map holds
only 6 entries (package paths and the asset name) — no property names — and the
export payload starts `00 02 01 02 02 02 01 02 01 04 02 02 01 05 02` followed by
raw values and localization keys like `CombatFocus_Kick_LocalizedName`.

Without a `.usmap` you can still do **byte-level edits** of known values, which is
almost certainly how `SkillsNoTimeCost` was made.

---

## 8. Reusable tooling

`tools/` in this folder — pure Python 3, standard library only (plus `pycryptodome`
only if a key ever becomes available). All of it was validated against the shipped
files described above.

| script | purpose |
|---|---|
| `utoc.py` | Parse any `.utoc`: header, chunks, compression blocks, directory index |
| `extract.py` | Extract + decompress chunks (`None` and `Zlib`) to real paths |
| `zen.py` | Parse Zen `.uasset`: summary, name map, imports, exports, bulk map |
| `globals.py` | Dump `global.ucas` → 54,880 names + 58,720 script objects as JSON |
| `containerheader.py` | Parse and tiling-validate `FIoContainerHeader` |
| `pak.py` | Read/extract legacy `.pak`, validates index SHA-1 |

---

## 9. Status

| Claim | State |
|---|---|
| Container/pak/Zen/container-header formats decoded | **VERIFIED** against shipped files |
| Mods extract correctly, hashes and tilings validate | **VERIFIED** |
| Base container is Oodle + AES encrypted | **VERIFIED** |
| `global.ucas` fully readable without a key | **VERIFIED** |
| 67 game settings classes exist in the shipped build | **VERIFIED** (`CONFIG_SURFACE.md`) |
| Property names on those settings classes | **UNVERIFIED** — needs a `.usmap` |
| Loose `Game.ini` override technique works | **VERIFIED on disk**; in-game effect reported by user, not observed here |
| Engine version 5.5 | **ASSUMPTION** |
| Load-order semantics of `~mods/`, `_P`, name prefixes | **HIGH CONFIDENCE**, not tested |
| Any mod built from *this format research* | **NONE** — the research contributed no built artifact |
| `~JohnRTX5080Quality_P.pak` rev 1.1 | built by Codex, installed, **independently re-verified here** (index SHA-1 OK, v3, mount `../../../`, 2 files) |
