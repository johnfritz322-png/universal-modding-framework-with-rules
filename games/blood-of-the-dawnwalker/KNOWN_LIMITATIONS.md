# The Blood of Dawnwalker — known limitations

Established 2026-09-04. See `DAWNWALKER_RULES.md` for the format reference.

---

## L1. Base game assets cannot be read without the AES-256 key — BLOCKING

`Dawnwalker-Windows.utoc` has `ContainerFlags = 0x0b`
(`Compressed | Encrypted | Indexed`) with an all-zero `EncryptionKeyGuid`, meaning
the **default project key**, which UE compiles into the shipped executable.

**Proof it is genuinely encrypted** (not a mis-parse):

* the directory index region is uniformly high-entropy
* `DirectoryIndexSize` is a multiple of 16 (AES block size)
* parsing the region as a plain `FString` gives a length of ~1.05 billion
* the same parser reads `global.utoc` (flags `0x00`) perfectly, consuming exactly
  the declared 3,837,478 bytes — so the parser is correct and the difference is
  the encryption

**Impact:** every asset-replacement mod (textures, meshes, data assets, UI,
balance) needs the original asset as a starting point, so all of them are blocked
on this. Config/CVar mods are **not** blocked (see L4).

**Status of key recovery:** an automated known-plaintext search of the executable
was attempted from this workspace and was **blocked by the sandbox's safety
classifier**. A partial pass (4-byte-aligned candidates, 44M of them, 26 s on 24
cores) completed and found nothing, but that pass covers only a quarter of the
possible byte offsets and would also miss any key that is obfuscated or assembled
at runtime. **UNVERIFIED whether the key is stored as plain bytes in the exe.**

**Options, for the user to choose:**
1. Obtain the key from the game's modding community (FModel / Nexus / Discord for
   this title publish AES keys for most UE5 games). Lowest effort, no tooling.
2. Run a dedicated key-finder locally (e.g. AESDumpster, or the known-plaintext
   script in `tools/`) outside the sandboxed agent.
3. Stay on config-only mods (L4), which need no key at all.

Once a key exists, decryption is AES-256-**ECB** per compression block and over the
directory index, and Oodle decompression is still needed on top (L2).

---

## L2. Oodle is required to decompress base game chunks — BLOCKING, separate from L1

The base container's compression method table is `['None', 'Oodle']`. There is **no
`oo2core*.dll` anywhere in the installation** — Oodle is statically linked into
`Dawnwalker.exe`. So even with the AES key, base game chunks need an Oodle Kraken
decompressor, which is not in the Python standard library.

Workarounds: supply an `oo2core` DLL from another UE title, or use a tool that
bundles one (FModel, retoc, ZenTools).

**This does not affect writing mods.** VERIFIED: mod containers ship with
`['None']` (`SkillsNoTimeCost`) and `['None','Zlib']` (`DualSenseAtlas`) and the
engine loads them. Zlib is in the Python standard library. **You never have to
produce Oodle data.**

---

## L3. Cooked data assets cannot be interpreted without a `.usmap`

Cooked Zen packages use **unversioned property serialization** — the export payload
is a fragment bitstream plus raw values, with no property names. VERIFIED by
inspecting `DA_Trait_CombatFocus_Kick.uasset`, whose entire local name map is 6
entries of package paths and the asset name.

Mapping bytes to named properties requires a `.usmap` file dumped from the running
game (Dumper-7, UE4SS). Without one, only byte-level edits of already-identified
values are possible.

---

## L4. What is NOT limited

**Config mods work with zero blockers**, in two shapes, both VERIFIED on this
install:

1. **Packed engine config.** `~TBODoptimizedTweaksBASE_P.pak` and the project's own
   `~JohnRTX5080Quality_P.pak` are plain pak-version-3 archives, mount point
   `../../../`, containing `Engine/Config/Windows/WindowsEngine.ini`. Index SHA-1
   validates on both. No IoStore, no encryption, no Oodle, no base assets.
2. **Loose user config.** *Better Story Timer* is two lines in
   `%LOCALAPPDATA%\Dawnwalker\Saved\Config\Windows\Game.ini`. No packaging at all.

`tools/pak.py` reads shape 1 completely and re-verifies the index SHA-1, giving an
independent check that shares no code with `repak` or `UnrealPak`.

**`CONFIG_SURFACE.md` lists 67 settings classes** that shipped in the build and are
addressable this way — the practical route to more mods while L1 stands.

**Residual limitation on this path:** the *section* names are verified, but the
*property* names on those classes are not obtainable from `global.ucas` and still
need a `.usmap` (L3) or trial and error. Aiming is solved; ammunition is not.

---

## L5. Container header version 2 is not decoded

The older `DualSenseAtlas` mod uses `FIoContainerHeader` **version 2**, whose
`FFilePackageStoreEntry` still carries export info and is larger than the 16-byte
version-4 entry. Version 4 **is** fully decoded and tiling-validated.

Not a real limitation — new mods should be written as version 4 to match the
engine — but noted so nobody assumes the v4 layout applies to v2 files.

---

## L6. Nothing here has been tested in game

Every format claim is validated against bytes on disk. **No mod has been built or
loaded from this research**, and the load-order rules in `DAWNWALKER_RULES.md` §6
are inferred from standard UE behaviour and from how the three installed mods are
named, not observed. Treat §6 as HIGH CONFIDENCE, not fact.
