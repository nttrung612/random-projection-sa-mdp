#!/bin/bash 
rs_attack() { 
    config_path=$1
    out_dir=$2 
    sarsa_model_dir=$3 
    exp_id=$4 
    sarsa_eps_ls=(0.02 0.05 0.1 0.15 0.2 0.3) 
    sarsa_reg_ls=(0.1 0.3 1.0 3.0 10.0) 
    for sarsa_eps in "${sarsa_eps_ls[@]}"; do 
        for sarsa_reg in "${sarsa_reg_ls[@]}"; do 
            sarsa_model_path="${sarsa_model_dir}/sarsa_${sarsa_eps}_${sarsa_reg}.model" 
            # Train SARSA model 
            python test.py --config-path "$config_path" --out-dir "$out_dir" --exp-id "$exp_id" \ --sarsa-enable --sarsa-eps "$sarsa_eps" --sarsa-reg "$sarsa_reg" \ --sarsa-model-path "$sarsa_model_path"
            # RS Deterministic
            python test.py --config-path "$config_path" --out-dir "$out_dir" --exp-id "$exp_id" \ --attack-sarsa-network "$sarsa_model_path" --attack-method sarsa --deterministic \ > "${out_dir}/${exp_id}/log/rs_${sarsa_eps}_${sarsa_reg}_attack_deterministic.log" 
        done 
    done 
} 

mad_attack() { 
    config_path=$1 
    out_dir=$2 
    exp_id=$3 
    python test.py --config-path "$config_path" --out-dir "$out_dir" --exp-id "$exp_id" \ --attack-method action --deterministic \ > "${out_dir}/${exp_id}/log/mad_attack_deterministic.log" 
}

rs_mad_attack() { 
    config_path=$1 
    out_dir=$2 
    sarsa_model_dir=$3 
    exp_id=$4 
    mad_regs=(1e-6 3e-6 1e-5 3e-5 1e-4 3e-4 1e-3 3e-3 1e-2 3e-2) 
    # mad_regs=(1e-3) 
    for mad_reg in "${mad_regs[@]}"; do 
        for sarsa_model in "$sarsa_model_dir"/*; do 
            model_name=$(basename "$sarsa_model") 
            # RS+MAD Deterministic 
            python test.py --config-path "$config_path" --out-dir "$out_dir" --exp-id "$exp_id" \ --attack-sarsa-network "$sarsa_model" --attack-method sarsa+action \ --attack-sarsa-action-ratio "$mad_reg" --deterministic \ > "${out_dir}/${exp_id}/log/sarsa-mad_${model_name}_r${mad_reg}_det.log" 
        done 
    done 
}        

run_attack() { 
    config_path=$1 
    agent_dir=$2 
    exp_id=$3 
    out_dir="${agent_dir}" 
    sarsa_model_dir="${agent_dir}/${exp_id}/sarsa_models" 
    mkdir -p "$sarsa_model_dir" mkdir -p "${out_dir}/${exp_id}/log" 
    rs_attack "$config_path" "$out_dir" "$sarsa_model_dir" "$exp_id" 
    mad_attack "$config_path" "$out_dir" "$exp_id" 
    # rs_mad_attack "$config_path" "$out_dir" "$sarsa_model_dir" "$exp_id" 
} 

config_path=$1 
agent_dir=$2 
exp_id=$3 
run_attack "$config_path" "$agent_dir" "$exp_id"