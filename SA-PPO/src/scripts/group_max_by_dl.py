import os
import re

ROOT_TXT = "_attack_mean_std.txt"
DIR_RE = re.compile(r"r(\d+)_d(\d+)_l(\d+)")


def parse_mean_std(txt_path):
    mean = std = None
    with open(txt_path, "r") as f:
        for line in f:
            if line.startswith("mean"):
                mean = float(line.split(":")[1])
            elif line.startswith("std"):
                std = float(line.split(":")[1])
    return mean, std


def collect_by_mode(parent_dir, mode="d"):
    """
    mode = 'd' or 'l'
    """
    assert mode in ("d", "l")

    groups = {}  # groups[key] = list of (r, d, l, mean, std)

    for subdir in os.listdir(parent_dir):
        m = DIR_RE.fullmatch(subdir)
        if not m:
            continue

        r, d, l = map(int, m.groups())
        txt_path = os.path.join(parent_dir, subdir, ROOT_TXT)

        if not os.path.isfile(txt_path):
            continue

        mean, std = parse_mean_std(txt_path)
        if mean is None:
            continue

        key = d if mode == "d" else l
        groups.setdefault(key, []).append((r, d, l, mean, std))

    return groups


def summarize_max(groups, mode="d"):
    """
    For each group key (d or l), select max mean
    """
    summary = {}

    for key, entries in groups.items():
        best = max(entries, key=lambda x: x[3])  # max mean
        summary[key] = best

    return summary


def main(parent_dir, mode):
    groups = collect_by_mode(parent_dir, mode)
    summary = summarize_max(groups, mode)

    print(f"\n===== BEST RESULT PER {mode.upper()} =====")
    for key in sorted(summary):
        r, d, l, mean, std = summary[key]
        if mode == "d":
            print(
                f"d={key} → best (r={r}, l={l}), "
                f"mean={mean:.3f}, std={std:.3f}"
            )
        else:
            print(
                f"l={key} → best (r={r}, d={d}), "
                f"mean={mean:.3f}, std={std:.3f}"
            )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python group_max.py <parent_dir> <d|l>")
        sys.exit(1)

    parent_dir = sys.argv[1]
    mode = sys.argv[2]
    main(parent_dir, mode)
