#!/usr/bin/env python3
"""Create a same-length, read-only test clone of a legacy weapon asset.

This is deliberately limited to a same-byte-length replacement in an extracted
legacy ``.uasset/.uexp`` pair.  It does not touch the game, save data, or an
installed mod folder.  A same-length identifier keeps every cooked offset valid
while testing only the discovery/registration question.

The output still uses the retail weapon actor, texture, localization table, and
stats.  It is not a finished custom sword and must not be installed unless the
separate container and discovery gates pass.
"""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_exact(data, old, new):
    count = data.count(old)
    if not count:
        return data, 0
    return data.replace(old, new), count


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="source legacy .uasset")
    ap.add_argument("destination", type=Path, help="new legacy .uasset")
    ap.add_argument("--old-id", required=True)
    ap.add_argument("--new-id", required=True)
    args = ap.parse_args()

    old = args.old_id.encode("ascii")
    new = args.new_id.encode("ascii")
    if len(old) != len(new):
        ap.error("--old-id and --new-id must have identical ASCII byte lengths")
    if not args.source.name.endswith(".uasset"):
        ap.error("source must be a .uasset file")
    source_uexp = args.source.with_suffix(".uexp")
    dest_uexp = args.destination.with_suffix(".uexp")
    if not source_uexp.is_file():
        ap.error("matching source .uexp is required")
    if args.destination.exists() or dest_uexp.exists():
        ap.error("destination already exists; refusing to overwrite it")

    args.destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = {"source": str(args.source), "destination": str(args.destination),
                "old_id": args.old_id, "new_id": args.new_id, "files": []}
    for source, dest in ((args.source, args.destination), (source_uexp, dest_uexp)):
        source_data = source.read_bytes()
        output_data, occurrences = replace_exact(source_data, old, new)
        if not occurrences:
            raise RuntimeError("%s contains no occurrence of %r" % (source, args.old_id))
        dest.write_bytes(output_data)
        if dest.stat().st_size != source.stat().st_size:
            raise RuntimeError("size changed while cloning %s" % source.name)
        manifest["files"].append({"source": source.name, "destination": dest.name,
                                  "occurrences": occurrences,
                                  "source_sha256": digest(source),
                                  "destination_sha256": digest(dest)})

    manifest_path = args.destination.with_suffix(".clone-manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
