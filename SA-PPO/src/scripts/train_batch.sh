#!/bin/bash

robust_ppo_reg=(0.003 0.01 0.03 0.1 0.3 1.0)
dim_factor=(2 4 8 16)
rp_lambda=(1e-4 1e-2 1e-1 1.0 1.25 10.0)

config_file=$1
env_name=$2
num_agents=$3
cpu=$4

conda_env="sappo"
SRC_DIR="/workspace/SA_PPO/src"

for ((ri=4; ri<5; ri++)); do
  reg=${robust_ppo_reg[$ri]}

  for ((di=0; di<${#dim_factor[@]}; di++)); do
    df=${dim_factor[$di]}

    for ((li=0; li<${#rp_lambda[@]}; li++)); do
      rpl=${rp_lambda[$li]}

      tag="r${ri}_d${di}_l${li}"
      out_dir="models/rpln_${env_name}/${tag}/agents"

      echo "===================================================="
      echo "Sweep index: $tag  (reg=$reg, df=$df, lambda=$rpl)"
      echo "===================================================="

      # launch agents
      for ((i=1; i<=num_agents; i++)); do
        session_name="train_${env_name}_${tag}_a${i}"

        tmux new-session -d -s "$session_name"
        tmux send-keys -t "$session_name" "source /opt/miniforge3/etc/profile.d/conda.sh" C-m
        tmux send-keys -t "$session_name" "conda activate $conda_env" C-m
        tmux send-keys -t "$session_name" "cd $SRC_DIR" C-m

        tmux send-keys -t "$session_name" "
python run.py \
  --config-path $config_file \
  --cpu $cpu \
  --robust-ppo-reg $reg \
  --rp-dim-factor $df \
  --rp-lambda $rpl \
  --out-dir $out_dir;
exit
" C-m
      done

      # wait for all agents of this sweep
      echo "Waiting for sweep $tag to finish..."
      while true; do
        running=0
        for ((i=1; i<=num_agents; i++)); do
          session_name="train_${env_name}_${tag}_a${i}"
          if tmux has-session -t "$session_name" 2>/dev/null; then
            running=1
            break
          fi
        done

        if [ $running -eq 0 ]; then
          echo "Sweep finished: $tag"
          break
        fi
        sleep 10
      done

    done
  done
done

echo "ALL SWEEPS DONE."
