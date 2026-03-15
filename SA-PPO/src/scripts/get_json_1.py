import numpy as np
import os
import json
def get_reward(path):
    rewards = np.load(path, allow_pickle=True)
    return rewards

def scan_dir(input_dir, attack_type="attack-none-eps-same"):
    rewards_list = {}
    for filename in os.listdir(input_dir + "/agents"):
        rewards = get_reward(os.path.join(input_dir, "agents", filename +"/" +  attack_type + "/rewards.pkl"))
        rewards_list[filename] = rewards
    output_path = os.path.join(input_dir, "_attack_rewards.json")
    with open(output_path, 'w') as outfile:
        json.dump(rewards_list, outfile, indent=4)
    return rewards_list

def scan_all(dir, attack_type="attack-none-eps-same"):
    for subdir in os.listdir(dir):
        input_dir = os.path.join(dir, subdir)
        if os.path.isdir(input_dir):
            scan_dir(input_dir, attack_type=attack_type)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python get_json.py <input_directory>")
        sys.exit(1)
    input_directory = sys.argv[1]
    scan_all(input_directory)