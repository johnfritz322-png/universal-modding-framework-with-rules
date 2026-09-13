# Dawnwalker — installed build fingerprint

**Checked 2026-09-04.** Regenerate any time with:

```bash
python ../../games/blood-of-the-dawnwalker/tools/gameversion.py
```

If the values below still match, every format finding in
`games/blood-of-the-dawnwalker/` still applies to the installed game.
**If they do not, the game was patched — re-verify before trusting anything.**

---

## Steam manifest — VERIFIED (read from `appmanifest_3751260.acf`)

| Field | Value |
|---|---|
| App ID | **3751260** |
| Build ID | **25129649** |
| LastUpdated | `1788565754` → **2026-09-04 23:49:14 UTC** (17:49 local) |
| Size on disk | 58,343,195,713 B (~58.3 GB) |
| Bytes downloaded (last patch) | 2,188,520,288 B (~2.19 GB) |
| StateFlags | `4` — fully installed |
| UpdateResult | `0` — last update succeeded, no error |
| ScheduledAutoUpdate | `0` — **nothing queued** |

## Content hashes — VERIFIED

| File | Bytes | SHA-256 |
|---|---:|---|
| `global.utoc` | 374 | `5c861dd91c94a4c8e07daae921e881ff272046eeba55eebf3990e4a4704b8cee` |
| `global.ucas` | 3,837,488 | `0ecfc5f66e6f52733787c85c9bba237b626b730623dd64b361e42515e0ad1cd5` |
| `Dawnwalker-Windows.utoc` | 70,109,154 | `7cf811c2a52e0f56ed9dc385168d1d871519ba99664eb18ced895c9ce14bc614` |
| `Dawnwalker.exe` | 176,196,472 | `7ad7d09645b0589dc0ff78b53aa1a7b18eca79b1b7f888b403ab41d88ac7e853` |

The 43.5 GB `Dawnwalker-Windows.ucas` is intentionally not hashed — the `.utoc`
changes whenever the `.ucas` does, so hashing the small file is sufficient.

## Container structure — VERIFIED

| Container | TOC ver | Chunks | Blocks | Flags | Container ID |
|---|---|---:|---:|---|---|
| `Dawnwalker-Windows.utoc` | 8 | 778,643 | 1,056,336 | `0x0b` Compressed \| Encrypted \| Indexed | `0x8fc20dab729a0600` |
| `global.utoc` | 8 | 1 | 15 | `0x00` None | `0xffffffffffffffff` |

---

## Is this the newest update?

**Almost certainly yes — HIGH CONFIDENCE, not VERIFIED.**

Evidence for:

* Steam reports **nothing queued** (`ScheduledAutoUpdate 0`), the install is
  **complete** (`StateFlags 4`), and the last update **succeeded** (`UpdateResult 0`).
* The install updated **2026-09-04**, pulling ~2.19 GB.
* The newest publicly documented patch is **Hotfix 1.0.2** (console update
  **1.004**), rolled out **2026-09-03**, described as ~2.4 GB on PS5. Date and
  download size both line up with what landed here.
* The game only released **2026-09-03**, so there is very little patch history to
  be behind on.

Why it is not VERIFIED: **Steam build IDs are not published in any patch-notes
source I could find**, so build `25129649` could not be matched to
"Hotfix 1.0.2" by a citable record. The match rests on date and size agreeing.

Hotfix 1.0.2 contents, per the public notes (third-party reporting, not
first-party): quest-progression fixes (Coen/Farkas dialogue, Lunka getting lost in
the tutorial), Intel CPU stability improvements, and the Dawnstar Blade blueprint.

Sources:
- [Hotfix 1.0.2 Patch Notes — Game8](https://game8.co/games/The-Blood-of-Dawnwalker/archives/618451)
- [First Update 1.004 released as Hotfix 1.0.2 — MP1st](https://mp1st.com/title-updates-and-patches/the-blood-of-dawnwalker-first-update-1-004-released-hotfix-1-0-2)
- [Update 1.004 patch notes — AsumeTech](https://asumetech.com/2026/09/04/blood-of-dawnwalker-update-1-004-patch-notes-quest-pc-fixes/)

## Does the patch affect our work?

**No.** All format research in `games/blood-of-the-dawnwalker/` was carried out on
**2026-09-04 from ~21:00 local — after** this build installed at 17:49. So the
research was done against the current build, not a stale one.

Re-verified 2026-09-04 after the update check: base container ID, TOC version,
chunk count, block count and flags are **identical** to the values recorded in
`DAWNWALKER_RULES.md`, and `global.ucas` still parses to exactly 54,880 names and
58,720 script objects. Nothing in `CONFIG_SURFACE.md` needs revisiting.

## What a future patch would break

| If this changes | Consequence |
|---|---|
| `global.ucas` hash | Re-run `globals.py`; `CONFIG_SURFACE.md` may gain or lose classes |
| Base container ID or chunk count | Base assets moved; any asset mod needs rebuilding |
| Base container **flags** | If `Encrypted` ever clears, KNOWN_LIMITATIONS L1 is lifted |
| `Dawnwalker.exe` hash | Any recovered AES key must be re-checked |
| Nothing above | Config mods are almost always safe across patches |

---

## Update 2026-09-09 — the game patched, every hash above is stale

Steam updated the install at **2026-09-09 18:43 local**. The fingerprint recorded
above belongs to the previous build and no longer matches anything on disk.

| | Recorded above | Current |
| --- | --- | --- |
| Steam build id | 25129649 | **25191761** |
| Internal build | `dw1-pc-257186` | **`dw1-pc-258042`** |
| `Dawnwalker.exe` | `7ad7d096…`, 176,196,472 B | `02d424ed…`, 176,487,800 B |
| `Dawnwalker-Windows.utoc` | `7cf811c2…`, 70,109,154 B | `b2b250de…`, 70,109,952 B |
| `global.utoc` | `5c861dd9…` | `3f6fe4c1…` |

Full current hashes, from `tools/gameversion.py`:

```text
global.utoc              374 B  3f6fe4c1281d72ed6266108d5ec424b67db153568494a89301166f381e7f6e54
global.ucas        3,837,472 B  a7583a85e4799183247c1e46c1f6ba20856e53cc8b4cfd63d4264341527ef2e1
Dawnwalker-Windows.utoc
                  70,109,952 B  b2b250de50fee81c6dd9de76e5583b25c3708922044e35ab57ab59ccda73deb6
Dawnwalker.exe   176,487,800 B  02d424eddbd364ed25f3777a7a2fa1b0dfe84690ae18f84ec9eb2997b0828c33
```

**The format research survives this patch.** Container structure is unchanged —
`Dawnwalker-Windows.utoc` is still TOC v8, flags `0x0b`, container id
`0x8fc20dab729a0600`, and the chunk count moved only 778,643 → 778,650. The base
encryption GUID is still all-zero/default. So the parsers and findings in
`games/blood-of-the-dawnwalker/` still apply; only the identity hashes changed.

**What this breaks.** Anything pinned to the old exe hash now refuses to run — that
includes Codex's `Grant-Dawnwalker-*.ps1` helpers, which pin `7AD7D096…`. That is
the safety check doing its job; update the pin deliberately rather than bypassing
it. Both usmap dumps on the machine predate the patch (2026-09-02 and 2026-09-03),
so FModel property mappings need re-checking against 258042 before being trusted.

Whether the AES key survived the patch is **UNVERIFIED** — the all-zero GUID is
suggestive, not proof. FModel loading the base archives is the test.
