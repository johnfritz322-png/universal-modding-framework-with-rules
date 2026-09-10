# FText cracked; item-asset decode still misaligned — handoff

> **Superseded for `ItemWeaponDataAsset` by
> [`ITEM-WEAPON-DECODE-2026-09-10.md`](ITEM-WEAPON-DECODE-2026-09-10.md).**
> The measured byte offsets and FText work below remain useful history, but the
> decode problem was caused by a reversed inheritance lookup, not an unknown
> preamble.

Picks up from `USMAP-DECODING-2026-09-09.md`. **Read this before touching
`ItemWeaponDataAsset`.** Stopped mid-investigation on a context budget, so the
open question is written out with the exact offsets rather than summarised.

## SOLVED: the FText layout

Dawnwalker's cooked item text is **not** the Base history that the standard
layouts assume. It is `FTextHistory_StringTableEntry`, **history type 11
(`0x0b`)**:

```
uint32  Flags
int8    HistoryType        == 11
FName   TableId            (8 bytes: uint32 index, uint32 number)
FString Key
```

Confirmed on `ITM_Weapon_SwordGreatMaster1a`: the TableId resolves to
`/Game/_Dawnwalker/Inventory/Items/ST_Content_Items.ST_Content_Items` — a string
table that is right there in the package name map — and the keys read
`SwordGreatMaster1a_ItemName` and `SwordGreatMaster1a_ItemDescription`.

That means **item display names live in a string table, not in the item asset**.
Anyone authoring a new item needs a localization entry too, or the name renders
blank. Implemented in `unversioned.py` (`Decoder.text`).

## SOLVED: the class really is ItemWeaponDataAsset

The export's ClassIndex is `0x7594865ce717ee6d`, which
`games/blood-of-the-dawnwalker/tools/scriptobjects.json` resolves to
`/Script/DogwoodInventory/ItemWeaponDataAsset`. Codex's claim is independently
confirmed. Note script-object hashes are **not** plain CityHash64 of the path —
FPackageObjectIndex packs a 2-bit type in the top bits, so match against
`scriptobjects.json` rather than recomputing.

## OPEN: 53 unexplained bytes before the first property

The property *values* do not start where the unversioned header says they should.

Facts, all measured on `ITM_Weapon_SwordGreatMaster1a` (export offset 0, size 214,
header size 1221 in the chunk):

- The unversioned header occupies `+0..+14` and is parsed **correctly**: 7
  fragments, 15 properties, indices `0,1,2,3,4,7,9,10,12,13,23,25,26,28,29`. These
  map cleanly onto the usmap schema (`NativeClass`, `ItemId`, `ItemProperties`,
  `ItemName`, `ItemDescription`, `ItemMaterial`, … `Weapon_Damage_Min/Max`).
- **`ItemId` is demonstrably at `+67`**, not `+18`. Bytes `+67..+75` are
  `06 00 00 00 | 00 00 00 00` = FName(index 6, number 0), and name 6 in this
  package is `SwordGreatMaster1a` — unambiguously the ItemId.
- **`ItemName` starts at `+75`**: flags `+75..+79` are zero, history byte `0x0b`
  sits at `+79`, the string-table FName follows, then the key.
- So **`+14..+67` — 53 bytes — is unaccounted for**, when the header implies only
  `NativeClass` (a 4-byte FPackageIndex) precedes ItemId.
- Inside that gap sit two clean float32s: **37.0 at `+35` and 53.0 at `+39`**.
  A Master greatsword in the scraped catalogue is in the 36–58 band, so these look
  like real damage values — but `Weapon_Damage_Min/Max` are schema indices 28/29,
  i.e. the *last* two properties, and the final 8 bytes of the export are zeros.

So either the values are not serialized in header order, or something is
serialized ahead of the property block that the schema does not describe.

### Hypotheses worth testing, cheapest first

1. **`UPrimaryDataAsset` writes `AssetBundleData` before its properties.** That is
   an editor-only `FAssetBundleData` and could plausibly account for a fixed
   preamble. Test: does the gap have a consistent size across several items?
2. **A second, nested unversioned block.** Try parsing `+14` as another
   `FUnversionedHeader` rather than as values.
3. **The DataTable path is the control.** `DT_WeaponAppearances` decodes
   byte-exactly (206/206 rows, 10,939/10,939 bytes) with the same code, so the
   header parser, name resolution, SoftObject and struct handling are all sound.
   The bug is specific to this asset shape, not to the decoder.

### Do not repeat these dead ends

Text widths of 5, 6, 9 and 13 bytes were all tried before the string-table layout
was found. **Width 6 does not error** — it decodes 85 of 214 bytes and yields an
`ItemId` that reads as a blueprint path and a denormal float for damage. It is
wrong. Any result that is not byte-exact against the export map's declared size
should be treated as garbage, because this asset produces plausible-looking
nonsense when misaligned.

## What is already trustworthy

| Capability | Status |
| --- | --- |
| AES + Oodle package reads | working, `iostore_read.py` |
| usmap v4 parse | exact, 2,223,873/2,223,873 bytes |
| Unversioned property decode | working — proven on DataTable |
| FText incl. string tables | working |
| `DT_WeaponAppearances` | **206/206 rows, byte-exact** → `weapon_appearances.csv` |
| `ItemWeaponDataAsset` | **misaligned — do not trust any output** |

Nothing was installed and no game file or save was modified.
