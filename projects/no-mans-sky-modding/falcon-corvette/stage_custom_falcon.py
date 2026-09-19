"""Saved rejected stage-only Falcon attempt.

This file is retained for audit and reference. It creates a loose saucer shape
and must not be reinstalled unchanged: the user rejected its appearance and
reported a boarding problem. It never writes a live save by itself.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path


SOURCE_SLOT = 8
TARGET_SLOT = 7
TARGET_NAME = "Falcon Courier"
EXPECTED_BOX = {"width": 36.0, "length": 48.0, "height": 8.0}


def is_empty_ship(ship: dict) -> bool:
    resource = ship.get("Resource", {})
    return resource.get("Filename") == "" and resource.get("Seed") == [False, "0x0"]


def find_ship_base(bases: list[dict], slot: int) -> dict | None:
    found = [
        base for base in bases
        if base.get("BaseType", {}).get("PersistentBaseTypes") == "PlayerShipBase"
        and base.get("UserData") == slot
    ]
    if len(found) > 1:
        raise RuntimeError(f"More than one PlayerShipBase points to slot {slot}.")
    return found[0] if found else None


def object_template(objects: list[dict], object_id: str) -> dict:
    item = next((entry for entry in objects if entry.get("ObjectID") == object_id), None)
    if item is None:
        raise RuntimeError(f"Working Corvette is missing required verified part {object_id}.")
    return item


def place(template: dict, x: float, y: float, z: float) -> dict:
    item = copy.deepcopy(template)
    item["Position"] = [float(x), float(y), float(z)]
    return item


def build_falcon_shell(core: list[dict]) -> tuple[list[dict], dict]:
    """Rejected 36x48x8 saucer approximation; kept only for audit."""
    q_right = object_template(core, "^B_WNG_Q")
    q_left = object_template(core, "^B_WNG_Q_R")
    p_right = object_template(core, "^B_WNG_P")
    p_left = object_template(core, "^B_WNG_P_R")
    strut_right = object_template(core, "^B_STR_K_NW")
    strut_left = object_template(core, "^B_STR_K_NE")
    turret = object_template(core, "^B_TUR_E")
    generator = object_template(core, "^B_GEN_1")
    additions: list[dict] = []
    for z in range(-21, 22, 3):
        for x in range(-15, 16, 3):
            ellipse = (x / 18.0) ** 2 + (z / 24.0) ** 2
            if 0.34 <= ellipse <= 1.0:
                additions.append(place(q_left if x < 0 else q_right, x, 4.5, z))
                if 0.62 <= ellipse <= 1.0 and z <= 9:
                    additions.append(place(p_left if x < 0 else p_right, x, 7.5, z))
    additions.extend([
        place(strut_left, -15, 6.0, 9), place(strut_left, -12, 6.0, 12),
        place(strut_right, 15, 6.0, 9), place(strut_right, 12, 6.0, 12),
        place(turret, -12, 7.5, -6), place(turret, 12, 7.5, -6),
        place(turret, 0, 7.5, 12),
        place(generator, -4.5, 6.0, -21), place(generator, 4.5, 6.0, -21),
        place(generator, -4.5, 6.0, -18), place(generator, 4.5, 6.0, -18),
    ])
    all_objects = copy.deepcopy(core) + additions
    return all_objects, {"added_parts": len(additions), "total_parts": len(all_objects)}


def main(current_path: Path, pre_removal_path: Path, destination: Path, audit: Path) -> None:
    root = json.loads(current_path.read_text(encoding="utf-8"))
    backup = json.loads(pre_removal_path.read_text(encoding="utf-8"))
    state = root["BaseContext"]["PlayerStateData"]
    backup_state = backup["BaseContext"]["PlayerStateData"]
    ships = state["ShipOwnership"]
    bases = state["PersistentPlayerBases"]
    if state.get("PrimaryShip") != SOURCE_SLOT or not is_empty_ship(ships[TARGET_SLOT]):
        raise RuntimeError("Unexpected source or target slot; refusing to write.")
    core_source = find_ship_base(bases, SOURCE_SLOT)
    old_target_base = find_ship_base(backup_state["PersistentPlayerBases"], TARGET_SLOT)
    if core_source is None or old_target_base is None:
        raise RuntimeError("Required source or target base is unavailable.")
    ship = copy.deepcopy(backup_state["ShipOwnership"][TARGET_SLOT])
    ship["Name"] = TARGET_NAME
    target_base = copy.deepcopy(old_target_base)
    target_base["Name"] = TARGET_NAME
    target_base["UserData"] = TARGET_SLOT
    target_base["Objects"], counts = build_falcon_shell(core_source["Objects"])
    ships[TARGET_SLOT] = ship
    bases.append(target_base)
    destination.write_text(json.dumps(root, indent=2, ensure_ascii=False), encoding="utf-8")
    audit.write_text(json.dumps({"live_save_modified": False, **counts}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("Usage: stage_custom_falcon.py CURRENT_JSON PRE_REMOVAL_JSON OUTPUT_JSON AUDIT_JSON")
    main(*(Path(argument) for argument in sys.argv[1:]))
