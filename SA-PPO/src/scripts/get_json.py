import os 
import json 
import numpy as np 
def gather_dir(input_dir): 
    rewards_dict = {} 
    category_groups = {"r": [], "m": [], "s": []} 
    for filename in os.listdir(input_dir): 
        if filename.endswith(".log"): 
            filepath = os.path.join(input_dir, filename) 
            with open(filepath, 'r') as file: 
                for line in file: 
                    if "all rewards:" in line: 
                        try: 
                            start = line.index('[')
                            end = line.index(']') + 1 
                            rewards_list_str = line[start:end] 
                            rewards_list = eval(rewards_list_str) 
                            rewards_dict[filename] = rewards_list 
                            first_char = filename[0].lower() 
                            if first_char in category_groups: 
                                category_groups[first_char].append((filename, rewards_list)) 
                        except Exception as e: 
                            print(f"Error parsing {filename}: {e}") 
                            break 
    # Compute best stats for each group 
    best_stats = {} 
    for key, logs in category_groups.items(): 
        if logs: 
            min_mean_log = min(logs, key=lambda x: np.mean(x[1])) 
            values = np.array(min_mean_log[1]) 
            mean = np.mean(values) 
            std = np.std(values) 
            label = {"r": "best_rs", "m": "best_mad", "s": "best_rs_mad"}[key] 
            best_stats[label] = f"{mean:.4f} +- {std:.4f}" 
    # Merge and dump 
    output_path = os.path.join(input_dir, "_attack_rewards.json") 
    with open(output_path, 'w') as outfile: 
        json.dump({**rewards_dict, **best_stats}, outfile, indent=4) 
        return best_stats 

def gather_agents(agents_dir): 
    dir_stats = {} 
    for agent_name in os.listdir(agents_dir): 
        agent_log_path = os.path.join(agents_dir, agent_name, "log") 
        if os.path.isdir(agent_path): 
            dir_stats[agent_name] = gather_dir(agent_path) 
            log_path = os.path.join(agents_dir, "_attack_rewards.json") 
if __name__ == "__main__": 
    import sys if len(sys.argv) != 2: print("Usage: python min_mean_stats_dir.py <input_directory>") sys.exit(1) input_directory = sys.argv[1] gather_dir(input_directory) how can i calc the mean and std of the best stats? mean = mean(sum(best_means)) and std =?
    if len(sys.argv) != 2: 
        print("Usage: python min_mean_stats_dir.py <input_directory>") 
        sys.exit(1) 
    input_directory = sys.argv[1] 
    gather_dir(input_directory)