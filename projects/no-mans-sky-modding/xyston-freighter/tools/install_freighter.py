"""Install a built Xyston hull into the game, laid out exactly like vanilla.

Hand-copying this got a file wrong more than once — a glob that silently missed the
geometry index, and geometry left in a subfolder where vanilla keeps it flat. So the
layout lives here instead, and every file is verified after the copy.

Vanilla layout, which this mirrors exactly:

    MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.SCENE.MBIN
    MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.GEOMETRY.MBIN.PC
    MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC.GEOMETRY.DATA.MBIN.PC
    MODELS/COMMON/SPACECRAFT/INDUSTRIAL/CAPITALFREIGHTER_PROC/<materials>

Note the geometry sits **beside** the scene, not in the subfolder. Only materials
live in the subfolder. NMSDK writes everything into the subfolder, so the geometry
has to be lifted out, and the scene's internal references corrected to match — which
`build_xyston_hull.py` does during its MBINCompiler round trip.

Usage:
    python install_freighter.py <build_dir> [--dry-run]
"""
import shutil
import sys
from pathlib import Path

GAME_MODS = Path(r"D:\steam\steamapps\common\No Man's Sky\GAMEDATA\MODS")
MOD_NAME = "XystonFreighter"
INNER = Path("MODELS/COMMON/SPACECRAFT/INDUSTRIAL")
MODEL = "CAPITALFREIGHTER_PROC"

# (filename, destination relative to INNER)
LAYOUT = [
    (MODEL + ".SCENE.MBIN", ""),
    (MODEL + ".GEOMETRY.MBIN.PC", ""),
    (MODEL + ".GEOMETRY.DATA.MBIN.PC", ""),
    ("XYSTON_CANNON_GLOW.MATERIAL.MBIN", MODEL),
]


def find(build_dir, name):
    """Locate a built file wherever NMSDK happened to put it."""
    hits = sorted(Path(build_dir).rglob(name))
    return hits[0] if hits else None


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    build_dir = sys.argv[1]
    dry = "--dry-run" in sys.argv

    target_root = GAME_MODS / MOD_NAME
    staged = []
    missing = []
    for name, sub in LAYOUT:
        src = find(build_dir, name)
        if src is None:
            missing.append(name)
            continue
        dst = target_root / INNER / sub / name
        staged.append((src, dst))

    if missing:
        raise SystemExit("not found in %s:\n  %s" % (build_dir, "\n  ".join(missing)))

    print("installing %d files into %s" % (len(staged), target_root))
    if dry:
        for src, dst in staged:
            print("  would copy %-38s -> %s" % (src.name, dst.relative_to(target_root)))
        return

    if (target_root / "MODELS").exists():
        shutil.rmtree(target_root / "MODELS")
    for src, dst in staged:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)

    print()
    ok = True
    for name, sub in LAYOUT:
        dst = target_root / INNER / sub / name
        if dst.is_file() and dst.stat().st_size > 0:
            print("  %9d bytes  %s" % (dst.stat().st_size, dst.relative_to(target_root)))
        else:
            print("  MISSING OR EMPTY        %s" % dst.relative_to(target_root))
            ok = False

    stray = [p for p in (target_root / INNER / MODEL).glob("*.GEOMETRY*")]
    if stray:
        print("\n  geometry left in the subfolder, vanilla keeps it flat:")
        for p in stray:
            print("     %s" % p.name)
        ok = False

    if not ok:
        raise SystemExit("\ninstall is not correct - see above")
    print("\ninstalled and verified.")


if __name__ == "__main__":
    main()
