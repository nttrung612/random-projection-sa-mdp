#!/bin/bash

# Usage:
# ./run_sarsa_eval.sh <config_file> <path_prefix> <sarsa_value> <agent_index> <session_name>

CONFIG_FILE="$1"
PATH_PREFIX="$2"
SARSA_VAL="$3"
AGENT_INDEX="$4"
SESSION_NAME="$5"

CONDA_SRC="/opt/miniforge3/etc/profile.d/conda.sh"

# Split SARSA value into reg and eps (e.g., input: 0.1_0.02 → reg=0.1, eps=0.02)
IFS='_' read -r SARSA_REG SARSA_EPS <<< "$SARSA_VAL"
echo "$SARSA_REG $SARSA_EPS"

MAD_REGS=("1e-6" "3e-6" "1e-5" "3e-5" "1e-4" "3e-4" "1e-3" "3e-3" "1e-2" "3e-2")
# MAD_REGS=("1e-6" "3e-6")

tmux new-session -d -s "$SESSION_NAME"

tmux send-keys -t "$SESSION_NAME" "cd /workspace/SA_DDPG" C-m
tmux send-keys -t "$session_name" "source $CONDA_SRC" C-m
tmux send-keys -t "$SESSION_NAME" "conda activate sa-ddpg-gpu" C-m

for MAD_REG in "${MAD_REGS[@]}"; do
    tmux send-keys -t "$SESSION_NAME" "python eval_ddpg.py --config $CONFIG_FILE --path_prefix ${PATH_PREFIX}/agent_${AGENT_INDEX} 'test_config:attack_params:enabled=true' 'test_config:attack_params:type=\"sarsa_action\"' 'test_config:sarsa_params:sarsa_reg=$SARSA_REG' 'test_config:sarsa_params:action_eps_scheduler:end=$SARSA_EPS' 'test_config:attack_params:sarsa_action_ratio=$MAD_REG'" C-m
    tmux send-keys -t "$SESSION_NAME" "wait" C-m
done

tmux send-keys -t "$SESSION_NAME" "echo 'All SARSA-ACTION evaluations finished for $SESSION_NAME'" C-m
# tmux send-keys -t "$SESSION_NAME" "exit" C-m
