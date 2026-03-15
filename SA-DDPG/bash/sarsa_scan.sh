#!/bin/bash

config_file=$1
agent_name=$2
path_prefix=$3
num_agent=$4

CONDA_ENV="sa-ddpg-gpu"
CONDA_SRC="/opt/miniforge3/etc/profile.d/conda.sh"
SRC_DIR="/workspace/SA_DDPG"

for ((i=1; i<=num_agent; i++)); do
    session_name="scan_sarsa_${agent_name}_${i}"
    log_dir="${path_prefix}/agent_${i}"
    mkdir -p "$log_dir"

    echo "[INFO] Launching tmux session: $session_name"
    tmux new-session -d -s "$session_name"

    # 1. Go to source directory
    tmux send-keys -t "$session_name" "cd $SRC_DIR" C-m

    # 2. Source conda
    tmux send-keys -t "$session_name" "source $CONDA_SRC" C-m
    tmux send-keys -t "$session_name" "conda activate $CONDA_ENV" C-m

    # 3. Set config paths and disable GPU
    tmux send-keys -t "$session_name" "export MODEL_CONFIG=$config_file" C-m
    tmux send-keys -t "$session_name" "export MODELS_FOLDER=$log_dir" C-m
    # tmux send-keys -t "$session_name" "export CUDA_VISIBLE_DEVICES=-1" C-m

    # 4. Cleanup
    tmux send-keys -t "$session_name" "find \$MODELS_FOLDER -name '*_sarsa_*' -delete" C-m

    # 5. Run nested SARSA loops (as one block)
    tmux send-keys -t "$session_name" "for sarsa_eps in 0.02 0.05 0.1 0.15 0.2 0.3; do" C-m
    # tmux send-keys -t "$session_name" "for sarsa_eps in 0.02; do" C-m
    tmux send-keys -t "$session_name" "  for sarsa_reg in 0.1 0.3 1.0 3.0 10.0; do" C-m
    # tmux send-keys -t "$session_name" "  for sarsa_reg in 0.1; do" C-m
    tmux send-keys -t "$session_name" "    python eval_ddpg.py \\" C-m
    tmux send-keys -t "$session_name" "      --config \${MODEL_CONFIG} \\" C-m
    tmux send-keys -t "$session_name" "      --path_prefix \${MODELS_FOLDER} \\" C-m
    tmux send-keys -t "$session_name" "      'test_config:attack_params:enabled=true' \\" C-m
    tmux send-keys -t "$session_name" "      'test_config:attack_params:type=\"sarsa\"' \\" C-m
    tmux send-keys -t "$session_name" "      \"test_config:sarsa_params:sarsa_reg=\${sarsa_reg}\" \\" C-m
    tmux send-keys -t "$session_name" "      \"test_config:sarsa_params:action_eps_scheduler:end=\${sarsa_eps}\"" C-m
    tmux send-keys -t "$session_name" "     wait" C-m
    tmux send-keys -t "$session_name" "  done" C-m
    tmux send-keys -t "$session_name" "done" C-m
    tmux send-keys -t "$session_name" "exit" C-m


    # Wait for the current session to finish before moving on
    echo "[INFO] Waiting for tmux session: $session_name to finish..."
    while true; do
        tmux_has_session=$(tmux has-session -t "$session_name" 2>/dev/null)
        if [ $? != 0 ]; then
            echo "[INFO] $session_name completed."
            break
        fi
        sleep 10
    done
done
