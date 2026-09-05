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
