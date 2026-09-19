# Correction: the game writes LZ4, not plain JSON — VERIFIED 2026-09-18

## What happened

`SAVE-FORMAT-AND-PARTS-CATALOG.md` recorded that `save.hg` is plain JSON. That was
true of the file **as the previous session left it**, but it is not how the game
writes saves. The record needs this correction.

At 20:46 the Codex session wrote `save.hg` as plain, null-padded JSON, 4,372,321
bytes. The user then launched the game. At 21:12 the game re-saved, and `save.hg`
became **1,101,046 bytes in the LZ4 block container format**.

So: a plain-JSON save is *accepted* by the game on load, but the game always writes
back its own compressed format. Any tool that reads a save must handle both.

## The container format — VERIFIED

A compressed `.hg` is a sequence of blocks. Each block is a 16-byte header followed
by one raw LZ4 block:

| Offset | Size | Field |
|---|---|---|
| 0 | 4 | magic, `0xFEEDA1E5` little-endian |
| 4 | 4 | compressed size of this block |
| 8 | 4 | uncompressed size of this block |
| 12 | 4 | padding, zero |

Decompressed chunks concatenate into the full JSON, null-terminated. The game's
chunk size is `0x80000` (524,288 bytes).

Detection is simply whether the first four bytes are the magic. If they are not, the
file is plain JSON.

A working reader/writer for both formats is `hgsave.py` beside this note. It needs
`lz4.block` (pip install lz4). The non-UTF-8 byte caveat still applies — decode and
encode with `errors="surrogateescape"` or the payload will not round-trip.

## Practical consequence

The pair are currently in **different formats**: `save.hg` is LZ4 (written by the
game at 21:12), `save2.hg` is still plain (written by the tooling at 20:46). Any
write must preserve each file's own format rather than assuming one.

There are also manifest files, `mf_save.hg` and `mf_save2.hg`, 432 bytes each. Their
role has **not** been verified. Until it is, prefer importing through the existing
`nms-corvette-build-share-tool`, which uses libNOM and handles the container and
manifests properly, over hand-writing save bytes.

## State re-verified after the game's write

Decoding both files after the 21:12 save confirms nothing was lost:

| Base | Name | Slot | Objects |
|---|---|---|---|
| 29 | `Default` (Darth Fritz) | 8 | 163 |
| 31 | `Falcon Courier` | 7 | 295 |

Fresh four-file backup taken before any further work:
`outputs/NMS-Backup-Claude-20260918-211832`.

## Standing lesson

A save read earlier in a session is stale the moment the user launches the game.
Re-read and re-verify before any write rather than trusting an earlier decode.
