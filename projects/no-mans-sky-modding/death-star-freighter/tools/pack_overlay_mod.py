"""Package and byte-verify the reversible Death Star overlay mod.

The input tree must contain the compiled stock-scene overlay and the exported
custom shell assets. MXML source is deliberately excluded from the archive.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from hgpaktool.api import HGPAKFile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staging", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--shell-name", default="DEATH_STAR_SILHOUETTE_STAGE3")
    assert "--" in sys.argv, "Pass script arguments after Blender's -- separator"
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1:])
    staging = args.staging.resolve()
    archive = args.archive.resolve()
    shell_name = args.shell_name.upper()
    required = {
        "MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN",
        f"CUSTOMMODELS/{shell_name}/{shell_name}.SCENE.MBIN",
        f"CUSTOMMODELS/{shell_name}/{shell_name}.GEOMETRY.MBIN.PC",
        f"CUSTOMMODELS/{shell_name}/{shell_name}.GEOMETRY.DATA.MBIN.PC",
        f"CUSTOMMODELS/{shell_name}/DEATHSTARHULLMAT.MATERIAL.MBIN",
    }
    assert staging.is_dir(), staging
    assert not archive.exists(), f"Refusing to overwrite archive: {archive}"

    files = sorted(
        path.relative_to(staging).as_posix()
        for path in staging.rglob("*")
        if path.is_file() and path.suffix.lower() not in {".mxml", ".manifest"}
    )
    assert set(files) == required, (set(files), required)
    archive.parent.mkdir(parents=True, exist_ok=True)
    # HGPAKtool resolves manifest entries relative to the manifest itself.
    manifest = staging / "DEATH_STAR_FREIGHTER_OVERLAY.manifest"
    manifest.write_text("\r\n".join(files) + "\r\n", encoding="utf-8", newline="")
    HGPAKFile.repack(str(manifest), str(archive), compress=True, platform="windows")
    assert archive.is_file() and archive.stat().st_size > 0, "Archive was not created"

    extraction = archive.with_name(archive.stem + "-roundtrip")
    assert not extraction.exists(), f"Refusing to overwrite extraction: {extraction}"
    with HGPAKFile(str(archive), platform="windows") as packed:
        assert len(packed.files) == len(files), (len(packed.files), len(files))
        extracted = packed.unpack(str(extraction))
    assert extracted == len(files), (extracted, len(files))
    for relative in files:
        source = staging / relative
        restored = extraction / relative.lower()
        assert restored.is_file(), restored
        assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(restored.read_bytes()).digest()
    print(f"OVERLAY_ARCHIVE=passed files={len(files)} bytes={archive.stat().st_size} byte_identical=true")


if __name__ == "__main__":
    main()
