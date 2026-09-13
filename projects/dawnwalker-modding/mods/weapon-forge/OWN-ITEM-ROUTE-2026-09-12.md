# Making it count as its own item — the plugin-registry route

The user's decision: the sword must be a **genuinely new inventory item**, not a
repurposed one. That rules out the package-override shortcut and makes registry
discovery mandatory. This is the route that looks right, and why it beats
rewriting the shipped registry.

## Why not rewrite AssetRegistry.bin

It is a 5.4 MB fixed-tag-store format. Progress so far (`assetregistry.py`):

- Header and name table parse **byte-exactly** — 40,908 names, 2,090,524 of
  2,090,524 string bytes.
- The tag store header decodes to sensible counts:

  ```
  NumberlessNames 3153   Names 148    NumberlessExportPaths 6607
  ExportPaths 834        Texts 0      AnsiStringOffsets 10370
  WideStringOffsets 2    AnsiStrings 1,113,039 bytes
  WideStrings 7,154      NumberlessPairs 110,769   Pairs 0
  ```

- **But the layout is not yet exact.** Summing those arrays ends at 4,660,621,
  which lands *inside* 8-byte pair records rather than at a section boundary, so
  at least one array size or field is still wrong. Not close enough to write.

Even once solved, a rewritten registry is **build-specific** — the game has
patched three times in a week, and each patch replaces it. And a malformed
registry breaks asset discovery globally rather than failing quietly.

## The better route

**Ship the item as a mounted UE plugin with its own asset registry.**

When the engine mounts a plugin at runtime it appends that plugin's
`AssetRegistry.bin` to the live registry state. New assets then become
discoverable through the normal primary-asset scan — which is exactly the gate
that blocks the current test package. No edit to the shipped registry at all.

### What is verified

| Check | Result |
| --- | --- |
| `uplugin` present in `Dawnwalker.exe` (UTF-16) | **yes** — plugin support is compiled in |
| `Mods/` path string in the exe | **yes** |
| AssetRegistry files in the base pak | **exactly one** — a single merged cook, so shipped plugins do not carry their own |
| Registry is the discovery gate | **confirmed** — see `REGISTRATION-LEAD-2026-09-12.md` |

### What is NOT verified — test these first

1. That the community loader actually mounts a plugin from
   `Dawnwalker\Mods\<ModName>\` on this build. Codex's research notes the Nexus
   "Console Enabler and Mod Loader" documents that layout
   (`<ModName>.uplugin`, `Content`, `Paks`) and expects a main actor prefixed
   `MOD_`, but that was read from documentation, not observed here.
2. That mounting appends the plugin's registry rather than ignoring it.
3. That a UE 5.5.4 cook of a content-only plugin emits a usable per-plugin
   `AssetRegistry.bin`.

Point 2 is the crux. Cheapest test: cook a plugin containing **one** trivial item,
mount it, and check whether the item menu count changes at all — the same probe
Codex already used to count 827 items.

### Why this is worth the detour

- No 5.4 MB registry rewrite, and nothing in the base archive is touched.
- **Patch-resilient** — a plugin survives a game update far better than a
  registry rebuilt against one specific build.
- It is the route the game itself is built for, rather than one worked around it.
- Failure mode is bounded: the plugin does not mount, and nothing happens.

## Status

**Not built. Nothing installed.** The registry parser and the route analysis are
saved; the next action is test 1 above, which is cheap and decides everything.
