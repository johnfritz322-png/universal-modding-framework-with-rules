"""Pack generated original geometry into a validation-only NMS archive.

This intentionally packages only generated CUSTOMMODELS files. It contains no
selection mapping or stock-scene override and is not an installable mod.
Run it through the dedicated Blender/NMSDK profile after the stage-3 generator:
    blender --background --python-exit-code 1 --python pack_asset_only_archive.py -- <output-dir>
"""
import hashlib
import sys
from pathlib import Path

from hgpaktool.api import HGPAKFile


output_dir = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
asset_root = output_dir / "CUSTOMMODELS"
assert asset_root.is_dir(), f"Missing generated asset root: {asset_root}"

files = sorted(
    path.relative_to(output_dir).as_posix()
    for path in asset_root.rglob("*")
    if path.is_file()
)
assert files, "No generated asset files to package"

manifest = output_dir / "DEATH_STAR_STAGE3_ASSET_ONLY.manifest"
# HGPAKtool requires CRLF plus a trailing line ending for repack manifests.
manifest.write_text("\r\n".join(files) + "\r\n", encoding="utf-8", newline="")
archive = output_dir / "DEATH_STAR_STAGE3_ASSET_ONLY.pak"
HGPAKFile.repack(str(manifest), str(archive), compress=True, platform="windows")
assert archive.is_file() and archive.stat().st_size > 0, "Archive was not created"

with HGPAKFile(str(archive), platform="windows") as packed:
    packaged_hashes = set(packed.files)
    extract_dir = output_dir / "asset-only-archive-roundtrip"
    assert not extract_dir.exists(), f"Refusing to overwrite extraction: {extract_dir}"
    extracted_count = packed.unpack(str(extract_dir))
assert len(packaged_hashes) == len(files), (len(packaged_hashes), len(files))
assert extracted_count == len(files), (extracted_count, len(files))
for relative_path in files:
    source = output_dir / relative_path
    extracted = extract_dir / relative_path.lower()
    assert extracted.is_file(), extracted
    assert hashlib.sha256(source.read_bytes()).digest() == hashlib.sha256(extracted.read_bytes()).digest()
print(f"ASSET_ONLY_ARCHIVE=passed files={len(files)} bytes={archive.stat().st_size} roundtrip=byte-identical")
