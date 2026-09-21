# Remove the "INTERSTELLAR COORDINATES RECEIVED" HUD banner

Built from the game's own files on 7.03.1 build 25351301, not downloaded.
Nexus has an equivalent (nomansmods 2190) but it is 4.x-era and Nexus cannot be
fetched without a login.

## Where the string lives

    LANGUAGE/NMS_LOC6_ENGLISH.MBIN      entry id  UI_HAIL_ALIEN_NAV_OSD
    LANGUAGE/NMS_LOC6_USENGLISH.MBIN    same entry

Root template `cTkLocalisationTable`, 10,370 entries, each a
`TkLocalisationEntry` with 18 fields in this fixed order:

    Id, English, French, Italian, German, Spanish, Russian, Polish, Dutch,
    Portuguese, LatinAmericanSpanish, BrazilianPortuguese, SimplifiedChinese,
    TraditionalChinese, TencentChinese, Korean, Japanese, USEnglish

The id name is worth noting: **`UI_HAIL_ALIEN_NAV_OSD`** - this is the on-screen
message for an alien *hailing* you with navigation data, not a mission title.

A second, longer string exists in `NMS_LOC7_*`:
`INTERSTELLAR COORDINATES RECEIVED <IMG>SLASH<> SENTINEL ACTIVITY DETECTED`.
That one is untouched; blank it too if the combined banner ever appears.

## The patch

Both files get the same one-entry partial patch: every field present, in the
game's order, `Id` kept and every text field emptied. Nothing else is changed.

Both English variants are patched because the game's `Language` setting is
`Default`, which follows the OS rather than naming a file.

## Finding a string yourself

```
hgpaktool.exe -U -f "LANGUAGE/*ENGLISH*" -O out NMSARC.MetadataEtc.pak
grep -ril "YOUR TEXT" out
MBINCompiler.exe convert out/language/nms_locN_english.mbin
grep -n -B 12 "YOUR TEXT" nms_locN_english.MXML
```

The line 12 above the text carries `_id=`, which is the entry to patch.

## Status

- Contents: **verified** by parsing both installed files off disk.
- Effect in game: **not yet tested.**
