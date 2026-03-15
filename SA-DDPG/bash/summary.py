import os
import re
import json
import statistics
from pathlib import Path

SC = {
    "ant": "ddpg_Ant-v2",
    "hopper": "ddpg_Hopper-v2",
    "reacher": "ddpg_Reacher-v2"
}

def get_attack_result(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        return None

    with file_path.open("r") as f:
        content = f.read()

    match = re.search(r"Average Reward: ([\d\.\-e]+),.*?std: ([\d\.\-e]+)", content)
    if not match:
        return None

    mean = float(match.group(1))
    std = float(match.group(2))

    try:
        filename_parts = file_path.stem.split("_")
        sarsa_eps = filename_parts[4]
        sarsa_reg = filename_parts[-1].split("-")[0]
        key = f"{sarsa_eps}_{sarsa_reg}"
        return {key: {"mean": mean, "std": std}}
    except Exception:
        return None

def get_best_result(agent_path):
    log_dir = Path(agent_path) / "log"
    results = {}
    for file in log_dir.glob("*eval*.txt"):
        res = get_attack_result(file)
        if res:
            results.update(res)

    if not results:
        return None

    # Find config with lowest mean reward
    best_key = min(results, key=lambda k: results[k]["mean"])
    best_result = results[best_key]

    # Save all + best
    out_json = Path(agent_path) / "sarsa.json"
    with out_json.open("w") as f:
        json.dump({
            "all_results": results,
            "best_config": best_key,
            "best_result": best_result
        }, f, indent=2)

    return out_json

def get_all(dir_path, agent_name):
    dir_path = Path(dir_path)
    best_agent_attack_result = {}
    means = []

    for subdir in dir_path.iterdir():
        if not subdir.is_dir():
            continue
        parts = subdir.name.split("_")
        if len(parts) != 2 or not parts[1].isdigit():
            continue

        agent_index = parts[1]
        agent_log_path = subdir / SC[agent_name]
        sarsa_json = get_best_result(agent_log_path)
        if not sarsa_json or not sarsa_json.exists():
            continue

        with sarsa_json.open("r") as f:
            data = json.load(f)
            best_agent_attack_result[agent_index] = data
            means.append((float(data["best_result"]["mean"]), agent_index))

    # Find median agent
    means.sort()
    median_agent = means[len(means) // 2][1]

    result_json = dir_path / f"{agent_name}_result.json"
    with result_json.open("w") as f:
        json.dump({
            "all_agents": best_agent_attack_result,
            "median_agent": median_agent
        }, f, indent=2)

    print(f"[INFO] Result saved to {result_json}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python parse_sarsa_results.py <dir_path> <agent_name>")
        exit(1)

    dir_path = sys.argv[1]
    agent_name = sys.argv[2]
    get_all(dir_path, agent_name)
