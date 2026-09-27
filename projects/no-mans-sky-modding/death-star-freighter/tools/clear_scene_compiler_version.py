"""Create an experimental unversioned scene header for the current game build.

The observed shipped capital scene and NMSDK-exported custom scenes both have
zero bytes in the compiler-version header field. This tool changes only that
four-byte field in an already compiled overlay scene; it never edits a game
archive or save.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    assert source.is_file(), source
    assert not output.exists(), f"Refusing to overwrite {output}"
    data = bytearray(source.read_bytes())
    assert data[:8] == b"\xCC" * 8, "Unexpected MBIN header magic"
    assert len(data) >= 28, "Truncated MBIN"
    prior = bytes(data[24:28])
    assert prior != b"\x00" * 4, "Source is already unversioned"
    data[24:28] = b"\x00" * 4
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    print(f"SCENE_COMPILER_VERSION=cleared prior={prior.hex().upper()} output={output}")


if __name__ == "__main__":
    main()
