#!/bin/bash

# Parameters to pass to your training script
CONFIG="config/Hopper_robust_sgld.json"
AGENT_NAME="hopper_sgld_rpln"
SAVE_PATH="./models/rpln"
NUM_AGENTS=7

# Interval in seconds to check tmux
CHECK_INTERVAL=600

echo "[INFO] Waiting for all 'scan' tmux sessions to finish..."

while true; do
    if tmux ls 2>/dev/null | grep -q "scan"; then
        echo "[INFO] 'training' sessions still running. Checking again in $CHECK_INTERVAL seconds..."
        sleep $CHECK_INTERVAL
    else
        echo "[INFO] No active 'training' sessions found. Launching new training run..."
        /workspace/SA_DDPG/bash/sarsa_scan.sh "$CONFIG" "$AGENT_NAME" "$SAVE_PATH" "$NUM_AGENTS"
        break
    fi
done
