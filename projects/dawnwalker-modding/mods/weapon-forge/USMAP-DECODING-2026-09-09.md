# usmap decoding — the archive is now fully readable from this toolchain

Follow-up to `DT_WEAPONAPPEARANCES-2026-09-09.md`, which stopped at "row values
need the usmap schema". They no longer do.

## What now works

`usmap.py` + `unversioned.py` decode UE5 unversioned property serialization, so
cooked property **values** are readable, not just name and import maps. Combined
with `iostore_read.py` (AES + Oodle), nothing in the base archive is closed.

**The result: `weapon_appearances.csv` — all 206 rows of `DT_WeaponAppearances`,
mapping every weapon item to its blade and scabbard mesh.**

## Two things the published .usmap format docs do not cover

Both were found by probing this file and confirmed by round-trip, not assumed.

**1. usmap v4 enum entries are 12 bytes, not 4.** v3 wrote a bare int32 name
index per entry. v4 writes `int64 value` followed by `int32 name index`. The
stride was recovered by testing all nine combinations of count width (1/2/4) and
entry size (4/8/12); exactly one lets the struct section that follows parse at
all, and it reads back `ACLCL_Lowest .. ACLCL_MAX` in order. With it the parser
consumes **2,223,873 of 2,223,873 bytes** — no drift anywhere in the file.

**2. `FFragment` packs `bIsLast` at bit 8, and `ValueNum` shifts by 9.** Several
descriptions put IsLast at bit 15 and ValueNum at bit 8. Against this data that
silently produces plausible-looking headers with wildly wrong property counts.
The correct masks are `SkipNum 0x007F`, `HasZero 0x0080`, `IsLast 0x0100`,
`ValueNum >> 9`.

## Two traps worth writing down

**Schema indices are global across the inheritance chain**, not per struct. Each
struct stores indices local to itself; the header numbers them base-class-first,
each level offset by the running total of its ancestors' `prop_count`. Simple row
structs whose parents declare nothing decode correctly either way, so this stays
hidden until a deep class like `ItemWeaponDataAsset` (offset 25) hits it.

**`GameplayTag` is not a bare FName.** It writes a normal unversioned property
header, and in these rows an empty tag is 3 bytes (header + zero mask), not 8.
Treating it as an FName consumed 8 bytes and desynchronised every row after the
first. Only structs with a genuine C++ binary serializer — Guid, Vector, Rotator,
Color and friends — write raw fields; the list lives in `unversioned.py`.

## Verification

Byte-exactness is the check used throughout, because a misaligned decode still
produces confident-looking output:

| Check | Result |
| --- | --- |
| usmap parse | 2,223,873 / 2,223,873 bytes — exact |
| `DT_WeaponAppearances` rows | 206 / 206 |
| DataTable export consumption | 10,939 / 10,939 bytes — exact |
| Spot check | `ITM_Weapon_AxeTest` → the axe mesh |
| Spot check | `ITM_Weapon_SwordVampiric1a` → `L_Sword_Vampiric_01` |

## What this settles about the sword prefixes

`ATTACHMENT-FINDINGS` flagged the `S_`/`L_`/`M_` prefixes as UNVERIFIED and warned
against assuming they meant Shortsword/Longsword/Greatsword. **They do not.**
`ITM_Weapon_SwordVampiric1a` — The Vrakhir, a Greatsword — uses
`L_Sword_Vampiric_01`, and `ITM_Weapon_SwordGreatMaster1a` uses `L_Sword_NPC_07`.
The prefix is not the weapon class. Use the CSV, never the name.

## Still not decoded: item data assets

`ItemWeaponDataAsset` does **not** decode correctly yet. Its `Text` properties
(`ItemName`, `ItemDescription`) do not match the standard FText layouts tried
(history `-1` with culture-invariant flag, or history `0` with
namespace/key/source), and item exports carry trailing data past their property
block, so whole-export byte-exactness cannot be used as the validator. Decoding
attempts produced garbage — an `ItemId` reading as a blueprint path, a denormal
float for damage — and are **not** recorded anywhere as fact.

This matters because Codex's current goal is authoring **new inventory items**,
which needs this asset type readable. It is the next thing to solve.

## Tools

- `usmap.py` — .usmap parser, including the v4 layout
- `unversioned.py` — unversioned property decoder
- `dump_weapon_appearances.py` — produces `weapon_appearances.csv`
- `weapon_appearances.csv` — the 206-row mapping

Nothing was installed and no game file or save was modified.
