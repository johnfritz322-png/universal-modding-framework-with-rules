#!/usr/bin/env python3
"""
Independent verification for the John RTX 5080 profile package.

Why this exists alongside build.ps1: build.ps1 verifies with repak and UnrealPak,
but repak also *built* the file. This script shares no code with either tool -- it
re-parses the pak from first principles and recomputes the index SHA-1 -- so it is
a genuine second opinion rather than a tool checking its own work.

It also does the thing build.ps1 cannot: compare what is ACTUALLY INSTALLED in the
game folder against the source in this repo, and report drift. That check caught a
real desync on 2026-09-04 (installed revision 1.1 vs. repo source revision 1.0).

Usage:
    python verify.py                     # verify the installed package
    python verify.py path\\to\\some.pak    # verify a specific package

Exit code 0 = all checks passed, 1 = something failed.
"""
import sys, os, hashlib, difflib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TOOLS = os.path.join(REPO, "games", "blood-of-the-dawnwalker", "tools")
sys.path.insert(0, TOOLS)

try:
    import pak as pakmod
except ImportError:
    sys.exit(f"could not import pak.py from {TOOLS}")

INSTALLED = (r"D:\steam\steamapps\common\The Blood of Dawnwalker\Dawnwalker"
             r"\Content\Paks\~mods\~JohnRTX5080Quality_P.pak")
SOURCE_INI = os.path.join(HERE, "pak-root", "Engine", "Config", "Windows",
                          "WindowsEngine.ini")

EXPECTED_MOUNT = "../../../"
EXPECTED_VERSION = 3
EXPECTED_FILES = {
    "Engine/Config/Windows/WindowsEngine.ini",
    "Dawnwalker/John RTX 5080 Profile.txt",
}

failures = []


def check(label, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + (f"  -- {detail}" if detail else ""))
    if not ok:
        failures.append(label)


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else INSTALLED
    if not os.path.isfile(target):
        sys.exit(f"package not found: {target}")

    print(f"Verifying: {target}")
    data = open(target, "rb").read()
    print(f"  size      : {len(data):,} bytes")
    print(f"  sha256    : {hashlib.sha256(data).hexdigest().upper()}")
    print()

    print("Structure:")
    info = pakmod.read_pak(target)     # prints its own detail + validates index SHA-1
    print()

    print("Assertions:")
    check("pak version is 3", info["version"] == EXPECTED_VERSION,
          f"got {info['version']}")
    check("mount point is ../../../", info["mount"] == EXPECTED_MOUNT,
          f"got {info['mount']!r}")

    names = {e["name"].replace("\\", "/") for e in info["entries"]}
    check("expected file set", names == EXPECTED_FILES,
          f"got {sorted(names)}" if names != EXPECTED_FILES else "")
    check("nothing is encrypted", not any(e["encrypted"] for e in info["entries"]))
    check("nothing is compressed", all(e["method"] == 0 for e in info["entries"]))

    # Drift check: does the packed INI match this repo's source?
    print()
    print("Drift check (installed package vs. repo source):")
    if not os.path.isfile(SOURCE_INI):
        check("repo source INI present", False, SOURCE_INI)
        return
    entry = next((e for e in info["entries"]
                  if e["name"].replace("\\", "/").endswith("WindowsEngine.ini")), None)
    if entry is None:
        check("packaged WindowsEngine.ini found", False)
        return

    o = entry["offset"]
    import struct
    h_cm = struct.unpack_from("<I", data, o + 24)[0]
    hdr = 24 + 4 + 20
    if h_cm != 0:
        nb = struct.unpack_from("<i", data, o + hdr)[0]
        hdr += 4 + nb * 16
    hdr += 1 + 4
    packed = data[o + hdr: o + hdr + entry["size"]]
    source = open(SOURCE_INI, "rb").read()

    same = packed.replace(b"\r\n", b"\n") == source.replace(b"\r\n", b"\n")
    check("packaged INI matches repo source", same)
    if not same:
        print()
        print("  DRIFT -- the installed package was NOT built from this repo source.")
        print(f"  packed: {len(packed):,} B  sha256 {hashlib.sha256(packed).hexdigest()[:16]}...")
        print(f"  source: {len(source):,} B  sha256 {hashlib.sha256(source).hexdigest()[:16]}...")
        print()
        a = source.decode("utf-8", "replace").splitlines()
        b = packed.decode("utf-8", "replace").splitlines()
        for line in list(difflib.unified_diff(a, b, "repo-source", "installed",
                                              lineterm="", n=1))[:60]:
            print("   " + line)
        print()
        print("  Resolve by rebuilding from source, or by committing the newer")
        print("  installed configuration back into pak-root/ -- whichever is correct.")

    print()
    if failures:
        print(f"FAILED {len(failures)} check(s): {', '.join(failures)}")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
