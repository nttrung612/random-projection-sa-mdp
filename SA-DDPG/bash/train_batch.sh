#!/bin/bash

config_file=$1
agent_name=$2
path_prefix=$3
num_agent=$4

CONDA_ENV="sa-ddpg-gpu"
CONDA_SRC="/opt/miniforge3/etc/profile.d/conda.sh"

# Loop over agent count
for ((i=1; i<=num_agent; i++)); do
    session_name="training_${agent_name}_${i}"
    log_dir="${path_prefix}/agent_${i}"
    mkdir -p "$log_dir"  # ensure log directory exists

    # Start detached tmux session
    tmux new-session -d -s "$session_name"

    # Send conda source
    tmux send-keys -t "$session_name" "source $CONDA_SRC" C-m
    tmux send-keys -t "$session_name" "conda activate $CONDA_ENV" C-m

    tmux send-keys -t "$session_name" "cd /workspace/SA_DDPG" C-m

    # Run training command
    tmux send-keys -t "$session_name" "python train_ddpg.py --config $config_file --path_prefix $log_dir" C-m
    tmux send-keys -t "$session_name" "exit" C-m
done
