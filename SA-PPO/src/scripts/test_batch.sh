#!/bin/bash

config_file=$1     # e.g. config/hopper.json
src_dir=$2         # e.g. models/rpln_sappo/

CONDA_SH="/opt/miniforge3/etc/profile.d/conda.sh"
ENV_NAME="sappo"
SRC_DIR="/workspace/SA_PPO/src"

# MUST match training arrays exactly
robust_ppo_reg=(0.003 0.01 0.03 0.1 0.3 1.0)
dim_factor=(2 4 8 16)
rp_lambda=(1e-4 1e-2 1e-1 1.0 1.25 10.0)

for exp_dir in "$src_dir"/r*_d*_l*; do
    config_id=$(basename "$exp_dir")

    # ---- parse indices from folder name ----
    if [[ "$config_id" =~ r([0-9]+)_d([0-9]+)_l([0-9]+) ]]; then
        ri=${BASH_REMATCH[1]}
        di=${BASH_REMATCH[2]}
        li=${BASH_REMATCH[3]}
    else
        echo "[WARN] Skipping invalid folder: $config_id"
        continue
    fi

    # ---- lookup real values ----
    reg=${robust_ppo_reg[$ri]}
    df=${dim_factor[$di]}
    rpl=${rp_lambda[$li]}

    echo "================================================"
    echo "Testing $config_id → reg=$reg, df=$df, lambda=$rpl"
    echo "================================================"

    for exp_id in "$exp_dir"/agents/*; do
        if [ -d "$exp_id" ]; then
          exp_id=$(basename "$exp_id")
          session_name="test_${config_id}_${exp_id}"

          tmux new-session -d -s "$session_name"
          tmux send-keys -t "$session_name" "source $CONDA_SH" C-m
          tmux send-keys -t "$session_name" "conda activate $ENV_NAME" C-m
          tmux send-keys -t "$session_name" "cd $SRC_DIR" C-m

          out_dir="$exp_dir/agents/"

          tmux send-keys -t "$session_name" "python test.py --config-path $config_file --exp-id $exp_id --out-dir $out_dir --robust-ppo-reg $reg --rp-dim-factor $df --rp-lambda $rpl; exit" C-m
        fi
    done

    # wait for all agents of this sweep
    echo "Waiting for tests of $config_id to finish..."
    while true; do
      running=0
      for exp_id in "$exp_dir"/agents/*; do
          if [ -d "$exp_id" ]; then
            exp_id=$(basename "$exp_id")
            session_name="test_${config_id}_${exp_id}"
            if tmux has-session -t "$session_name" 2>/dev/null; then
              running=1
              break
            fi
          fi
      done
      if [ $running -eq 0 ]; then
        break
      fi
    done

    echo "All tests for $config_id completed."
done