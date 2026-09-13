# Attachment route — findings on build 258042

Follow-up to `AUDIT-2026-09-09.md`. Covers two things: an independent check of
Codex's archive-inspection claims, and the first mechanically grounded answer to
"how does a custom mesh actually get onto an equipped weapon".

## Codex's claims: verified

Checked by two independent methods, neither of which trusts Codex's tooling.

**Method 1 — chunk-id derivation, no decryption.** IoStore derives a package's
chunk id from `CityHash64` of the lowercased package name in UTF-16LE, and the
chunk-id table sits outside the encrypted directory index. So a claimed path can
be confirmed or refuted with no AES key at all. The CityHash64 implementation in
`cityhash64.py` was validated first by reproducing three chunk ids already
observed in the WeaponForge container — `/Engine/EngineResources/WhiteSquareTexture`
→ `0x20ddf459fde55eb8` and two others, all exact. Two fabricated control paths
came back absent, so the method does not produce false positives.

**Method 2 — decrypted directory index.** The AES key in FModel's config decrypts
the base container's directory index cleanly, yielding mount point `../../../`,
42,799 directories and **770,801 file paths**. Every claimed asset was then found
by direct string lookup.

| Codex's claim | Result |
| --- | --- |
| `/Game/_Dawnwalker/Player/BP_PlayerCharacter` | **FOUND** |
| `/Game/_Dawnwalker/Blueprints/Items/Equippable/BP_Weapon_GreatSword` | **FOUND** |
| `/Game/_Dawnwalker/Inventory/Items/ITM_Weapon_SwordGreatMaster1a` | **FOUND** |
| `/Game/_Dawnwalker/Environment/Megascans/3D_Assets/Sword/SM_Sword` | **FOUND** |
| `/Game/_Dawnwalker/Characters/Swords/M_Sword_NPC_06/M_Sword_NPC_06` | **FOUND** |
| fabricated control ×2 | absent, as required |

Corroborating detail: the archive holds **191 `ITM_Weapon_*` definitions**, exactly
matching the 191 `weapon_*` ids in Codex's `gear-index.json`. Two different routes
to the same number.

**The AES key is valid on build 258042.** That answers the open question from the
audit — the patch did not rotate it.

## What is NOT verified, and must not be read as verified

Path existence is not content verification. These Codex claims live *inside*
Oodle-compressed packages and were **not** independently checked here:

- that `WeaponMesh` resolves to `SM_Sword`, or its `RelativeScale3D = (1.2,1.2,1.2)`
- the `SwordTip` component at relative `(0, 0, 87)`
- the `Sheathed Weapon` component name and its attachment to `CharacterMesh0`
- inheritance from `BP_Weapon_New` — that name was not located at any probed path,
  though Codex never stated a full path for it, so this is unlocated rather than
  contradicted

They are plausible and consistent with everything visible, but they rest on
Codex's decryption alone. Reading them independently needs Oodle, which this
repo's toolchain deliberately does not implement.

One number differs: Codex reports `1,031,238` virtual files, the directory index
yields `770,801`. Almost certainly different counting (FModel counts `.uexp`/
`.ubulk` splits and chunks lacking directory entries). Not treated as an error.

## The weapon visual system

The decrypted index shows a clean, consistent structure — **173 sword folders**
under `/Game/_Dawnwalker/Characters/Swords/`, each shaped like:

```
Characters/Swords/L_Sword_NPC_06/
    L_Sword_NPC_06.uasset            + .ubulk    <- blade mesh
    L_Sword_NPC_06_Scabbard.uasset   + .ubulk    <- scabbard mesh
    Materials/MI_L_Sword_NPC_06_OPT.uasset
    Materials/T_MI_L_Sword_NPC_06_PARAM.uasset
```

Folders are prefixed `S_Sword` (54), `L_Sword` (50), `M_Sword` (43) plus named
one-offs. **Do not assume those prefixes map to the Shortsword/Longsword/Greatsword
classes** — the counts do not line up with the 185-weapon catalog, and
`M_Sword_Erka_01` corresponds to a weapon the catalog calls a Longsword. Prefix
meaning is UNVERIFIED.

There are 48 `BP_Weapon_*` actor blueprints, most of them per-NPC-sword variants.

## The route that is actually available

**Override the sword mesh package, do not add a new one.**

A container in `~mods` that supplies a package with the *same package name* as a
base-game asset produces the same chunk id, loads later, and wins. That is not
theory on this install — it is what the two mods already working here do:

| Mod | Colliding chunks | What it replaces |
| --- | --- | --- |
| `SkillsNoTimeCost` | 112 of 113 | trait assets |
| `DualSenseAtlas` | 4 of 5 | button icon textures |

So the lowest-risk custom-weapon route is a cooked `UStaticMesh` published at
exactly `/Game/_Dawnwalker/Characters/Swords/<Name>/<Name>`, replacing one sword's
blade (and optionally `_Scabbard`). That needs **no Blueprint edit, no `retoc`
reserialization, no UE4SS, and no plugin actor** — all the risky parts of the
earlier plan drop away.

### This conflicts with gates 1–3 as written

The stated gates require an *additive* plugin with **zero** collisions. The only
route proven to work on this install is a *targeted replacement*, which collides
by design. Both cannot hold. The gate should become:

> collides with **exactly** the intended package names and nothing else — verified
> by name, not just by count.

`verify_container.py` already reports the count; the intended set should be listed
explicitly in the build's README so any extra collision is obvious.

### Costs of this route, stated plainly

- It replaces a mesh **globally**. Every item using that sword visual changes, not
  just the player's. Per-item custom weapons are not achievable this way.
- Whether the game's mesh carries sockets the blueprint or VFX rely on is
  **unverified**. A replacement missing them may break trails or hit effects.
- The replacement must be a UE 5.5 IoStore-cooked package under the identical
  package path, which means the authoring project must reproduce the folder
  structure under `Content/_Dawnwalker/Characters/Swords/<Name>/`.

## The next unknown, and where it lives

Which sword folder a given item uses is still unknown. The mapping almost
certainly lives in:

```
/Game/_Dawnwalker/Inventory/Items/DT_WeaponAppearances    (FOUND, chunk 0x2b6fc8ead9260336)
```

Reading it needs Oodle decompression — FModel can, this toolchain cannot. That is
the single most valuable next read: it turns "replace some sword" into "replace
the sword this specific item uses".

## Tools added

- `cityhash64.py` — pure-Python CityHash64, validated against known chunk ids.
- `verify_asset_path.py` — confirm/refute a package path with no AES key.
  Use `--file`; a bare `/Game/...` argument is mangled by Git Bash path conversion.
- `example-paths.txt` — the paths checked above, including controls.

Nothing was installed and no game file or save was modified.
