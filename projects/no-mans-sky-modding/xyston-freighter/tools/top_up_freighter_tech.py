"""Refill every chargeable item in the freighter's technology inventory.

This is the one thing on the freighter that a mod cannot fix, because it is stored
state rather than a table value: `^F_HYPERDRIVE` holds a charge amount that sits
below its maximum.

Editing technology and inventory amounts is the sanctioned use of save editing —
see OUTCOME-AND-LESSONS.md in the falcon-corvette project, which bans editing a
Corvette *interior* this way but explicitly keeps technology and inventory.

Only items where amount < max are touched, and only in the freighter's technology
inventory (`0wS`). Nothing is added or removed. Both save slots are written,
because the game alternates between save.hg and save2.hg and loads the newer.

Usage:
    python top_up_freighter_tech.py            # report only, writes nothing
    python top_up_freighter_tech.py --apply    # take a backup, then write
"""
import shutil
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hgsave

SAVE_DIR = Path(r"C:\Users\johnf\AppData\Roaming\HelloGames\NMS\st_76561199262233576")
BACKUP_ROOT = Path(r"C:\Users\johnf\Documents\Codex\2026-09-07"
                   r"\referenced-chatgpt-conversation-this-is-an\outputs")
SAVE_FILES = ("save.hg", "save2.hg", "mf_save.hg", "mf_save2.hg")

FREIGHTER_TECH = "0wS"
AMOUNT, MAX_AMOUNT = "1o9", "F9q"


def freighter_tech(data):
    return data["vLc"]["6f="][FREIGHTER_TECH][":No"]


def find_low(items):
    low = []
    for item in items:
        amount, maximum = item.get(AMOUNT), item.get(MAX_AMOUNT)
        if not isinstance(amount, int) or not isinstance(maximum, int):
            continue
        if amount < 0:          # -1 means the item has no charge to fill
            continue
        if amount < maximum:
            low.append((item, amount, maximum))
    return low


def backup():
    stamp = time.strftime("%Y%m%d-%H%M%S")
    target = BACKUP_ROOT / ("NMS-Before-TechTopUp-" + stamp)
    target.mkdir(parents=True, exist_ok=True)
    for name in SAVE_FILES:
        source = SAVE_DIR / name
        if source.exists():
            shutil.copy2(source, target / name)
    return target


def main():
    apply = "--apply" in sys.argv

    for name in ("save.hg", "save2.hg"):
        data, fmt = hgsave.read(str(SAVE_DIR / name))
        low = find_low(freighter_tech(data))
        print("%s: %d chargeable item(s) below maximum" % (name, len(low)))
        for _, amount, maximum in low:
            print("    %d / %d" % (amount, maximum))

    if not apply:
        print("\nreport only. pass --apply to take a backup and write.")
        return

    where = backup()
    print("\nbackup: %s" % where)

    for name in ("save.hg", "save2.hg"):
        path = SAVE_DIR / name
        data, fmt = hgsave.read(str(path))
        items = freighter_tech(data)
        low = find_low(items)
        for item, amount, maximum in low:
            item[AMOUNT] = maximum
        hgsave.write(str(path), data, fmt)

        # read the file back off disk rather than trusting the write
        check, _ = hgsave.read(str(path))
        still_low = find_low(freighter_tech(check))
        print("%s: topped up %d item(s), %d still below max"
              % (name, len(low), len(still_low)))
        if still_low:
            raise SystemExit("verification failed for %s" % name)


if __name__ == "__main__":
    main()
