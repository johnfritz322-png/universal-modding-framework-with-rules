"""Build a modern NMS MODS-folder overlay tree without compiling scenes.

Current MBINCompiler guidance uses MXML renamed to EXML for scene edits in a
mod directory. This creates that layout with the stock-root overlay and the
custom scene; geometry streams remain their NMSDK-exported binary files.
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


CAPITAL_MXML = Path("MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MXML")
SHELL_TEMPLATE_DIR = Path("CUSTOMMODELS/DEATH_STAR_SILHOUETTE_STAGE3")
SHELL_TEMPLATE_MXML = SHELL_TEMPLATE_DIR / "DEATH_STAR_SILHOUETTE_STAGE3.SCENE.MXML"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--overlay-staging", type=Path, required=True)
    parser.add_argument("--shell-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--shell-name", default="DEATH_STAR_SILHOUETTE_STAGE3")
    args = parser.parse_args()
    overlay = args.overlay_staging.resolve()
    shell_root = args.shell_root.resolve()
    output = args.output.resolve()
    shell_name = args.shell_name.upper()
    shell_dir = Path("CUSTOMMODELS") / shell_name
    shell_mxml = shell_dir / f"{shell_name}.SCENE.MXML"
    assert (overlay / CAPITAL_MXML).is_file(), overlay / CAPITAL_MXML
    assert (shell_root / SHELL_TEMPLATE_MXML).is_file(), shell_root / SHELL_TEMPLATE_MXML
    assert not output.exists(), f"Refusing to overwrite {output}"

    # Scene files are critical full replacements in the current loose-file
    # loader.  They must remain MXML, not EXML patch files.
    target = output / CAPITAL_MXML
    target.parent.mkdir(parents=True)
    capital_text = (overlay / CAPITAL_MXML).read_text(encoding="utf-8")
    target.write_text(
        capital_text.replace("DEATH_STAR_SILHOUETTE_STAGE3", shell_name), encoding="utf-8"
    )
    shell_target = output / shell_mxml
    shell_target.parent.mkdir(parents=True)
    shell_text = (shell_root / SHELL_TEMPLATE_MXML).read_text(encoding="utf-8")
    shell_target.write_text(
        shell_text.replace("DEATH_STAR_SILHOUETTE_STAGE3", shell_name), encoding="utf-8"
    )
    for suffix in (".GEOMETRY.MBIN.PC", ".GEOMETRY.DATA.MBIN.PC"):
        filename = shell_name + suffix
        shutil.copy2(shell_root / shell_dir / filename, output / shell_dir / filename)
    files = sorted(path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file())
    assert len(files) == 4, files
    print("MODERN_EXML_OVERLAY=created files=" + ",".join(files))


if __name__ == "__main__":
    main()
