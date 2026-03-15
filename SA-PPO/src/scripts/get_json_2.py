import os
import json
import numpy as np


def get_stats(dir_path):
    json_path = os.path.join(dir_path, "_attack_rewards.json")
    out_path = os.path.join(dir_path, "_attack_mean_std.txt")

    if not os.path.isfile(json_path):
        print(f"[SKIP] {json_path} not found")
        return

    with open(json_path, "r") as f:
        data = json.load(f)

    # 🔑 flatten ALL rewards into one list
    all_rewards = []
    for rewards in data.values():
        all_rewards.extend(rewards)

    all_rewards = np.asarray(all_rewards, dtype=np.float64)

    mean = all_rewards.mean()
    std = all_rewards.std()

    with open(out_path, "w") as f:
        f.write(f"mean: {mean:.6f}\n")
        f.write(f"std:  {std:.6f}\n")
        f.write(f"n:    {len(all_rewards)}\n")

    print(f"[OK] {dir_path} → mean={mean:.3f}, std={std:.3f}, n={len(all_rewards)}")


def get_stats_all(parent_dir):
    for subdir in sorted(os.listdir(parent_dir)):
        path = os.path.join(parent_dir, subdir)
        if os.path.isdir(path):
            get_stats(path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python get_json_2.py <parent_dir>")
        sys.exit(1)

    get_stats_all(sys.argv[1])
