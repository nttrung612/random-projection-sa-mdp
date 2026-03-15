# Random Projection Meets Robust Deep Reinforcement Learning

This repository contains the code used to study random-projection front-ends
for robust deep reinforcement learning. It builds on three existing SA-MDP
implementations:

- `SA-DQN` for Atari
- `SA-DDPG` for off-policy MuJoCo control
- `SA-PPO` for on-policy MuJoCo control

The refactor in this pass does not change the experimental logic. It adds a
project-level experiment index, consolidates duplicated config parsing, and
documents how the code maps to the paper.

## Project Overview

The paper introduces two front-end variants:

- `RP-LN`: fixed random projection, then layer normalization and ReLU
- `ResRP`: residual random projection with a skip path

These are intended to be drop-in additions on top of SA-MDP-style robust RL
training, not replacements for the robust objectives themselves.

The paper evaluates the approach on:

- Atari DQN experiments under `Natural`, `PGD-10`, and `PGD-50`
- MuJoCo PPO experiments under `Natural`, `MAD`, `RS`, and `RS+MAD`
- MuJoCo DDPG experiments under `Natural Reward` and `Best Attack Reward`

See [paper_experiments.md](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/docs/paper_experiments.md) for the full summary.

## Repository Structure

```text
SA-DQN/                 Atari experiments and baselines
SA-DDPG/                Off-policy MuJoCo experiments
SA-PPO/                 On-policy MuJoCo experiments
docs/                   Paper summary and codebase review
project_utils/          Shared config and experiment metadata helpers
scripts/                Project-level helper scripts
```

Useful documents:

- [paper_experiments.md](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/docs/paper_experiments.md)
- [codebase_review.md](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/docs/codebase_review.md)

## Summary Of The Paper And Experiments

The paper keeps the original SA-MDP robust RL setup and inserts a
random-projection front-end before the downstream policy or value network.

Main experiment groups:

- Atari:
  - `Freeway`, `BankHeist`, `RoadRunner`
  - plus additional RP-LN training from scratch on `Enduro`, `Alien`, `FishingDerby`
- SA-PPO:
  - `Hopper-v2`, `Walker2d-v2`, `Humanoid-v2`
- SA-DDPG:
  - `Ant-v2`, `Hopper-v2`, `Reacher-v2`

Main attacks:

- `PGD-10`
- `PGD-50`
- `MAD`
- `RS`
- `RS+MAD`

## Installation

The original subprojects have their own dependencies. In practice, reproduce one
family at a time in an isolated environment.

### Windows + WSL

If you are using Windows and running Codex in WSL, use WSL as the execution
environment for all experiments.

Guidelines:

- run all Python, pip, and experiment commands inside WSL
- install Linux dependencies inside WSL, not in PowerShell or `cmd`
- use WSL virtual environments
- for long training runs, prefer storing the repository inside the WSL Linux
  filesystem instead of under `/mnt/c/...`, because `/mnt/c` is slower for
  heavy file I/O

Basic WSL setup:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv build-essential git
```

Create and activate a virtual environment from WSL:

```bash
cd /mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

If you want better training performance, move the repository into the WSL
filesystem first:

```bash
mkdir -p ~/projects
cp -r /mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp ~/projects/
cd ~/projects/random-projection-sa-mdp
```

GPU note:

- if you want GPU training in WSL, you need WSL2 plus a Windows NVIDIA driver
  with WSL CUDA support
- if that is not configured, start with CPU runs first

### SA-DQN

```bash
cd SA-DQN
pip install -r requirements.txt
```

### SA-DDPG

```bash
cd SA-DDPG
pip install -r requirements.txt
```

### SA-PPO

```bash
cd SA-PPO
pip install -r requirements.txt
```

Environment notes:

- Python `3.7+` is expected by the original code.
- `SA-PPO` and `SA-DDPG` require MuJoCo-compatible Gym environments.
- `SA-DQN` expects Atari environment dependencies.

## How To Reproduce Each Experiment

Project-level experiment index:

```bash
python3 scripts/experiments.py
```

That command prints the paper experiment groups, configs, and canonical train /
eval commands.

If you are on Windows with WSL, run that command from WSL:

```bash
cd /mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp
source .venv/bin/activate
python3 scripts/experiments.py
```

### Atari / SA-DQN

Training:

```bash
cd SA-DQN
python3 train.py --config config/Pong_pgd.json
python3 train.py --config config/Pong_cov.json
python3 train.py --config config/Pong_nat.json
```

Evaluation:

```bash
cd SA-DQN
python3 test.py --config config/Pong_pgd.json
python3 test.py --config config/Pong_pgd.json test_config:attack=true
python3 test.py --config config/Pong_pgd.json test_config:attack=true test_config:attack_config:params:niters=50
```

Related configs:

- `*_nat.json`: vanilla baseline
- `*_pgd.json`: PGD-based robust training
- `*_cov.json`: convex-relaxation robust training
- `*_adv.json`: adversarial training baseline

### SA-PPO

Training:

```bash
cd SA-PPO/src
python3 run.py --config-path config_hopper_vanilla_ppo.json
python3 run.py --config-path config_hopper_robust_ppo_sgld.json
python3 run.py --config-path config_walker_robust_ppo_sgld.json
python3 run.py --config-path config_humanoid_robust_ppo_sgld.json
```

Evaluation:

```bash
cd SA-PPO/src
python3 test.py --config-path config_hopper_robust_ppo_sgld.json --exp-id <EXP_ID> --deterministic
python3 test.py --config-path config_hopper_robust_ppo_sgld.json --load-model <MODEL> --attack-method action --deterministic
python3 test.py --config-path config_hopper_robust_ppo_sgld.json --load-model <MODEL> --sarsa-enable --sarsa-model-path sarsa_hopper.model
python3 test.py --config-path config_hopper_robust_ppo_sgld.json --load-model <MODEL> --attack-method sarsa --attack-sarsa-network sarsa_hopper.model --deterministic
```

RP-specific PPO configs currently present in the repo:

- `config_hopper_robust_ppo_sgld.json`
- `config_walker_robust_ppo_sgld.json`

### SA-DDPG

Training:

```bash
cd SA-DDPG
python3 train_ddpg.py --config config/Ant_vanilla.json
python3 train_ddpg.py --config config/Ant_robust.json
python3 train_ddpg.py --config config/Ant_robust_sgld.json
```

Evaluation:

```bash
cd SA-DDPG
python3 eval_ddpg.py --config config/Ant_robust.json
python3 eval_ddpg.py --config config/Ant_robust.json test_config:attack_params:enabled=true
python3 eval_ddpg.py --config config/Ant_robust.json test_config:attack_params:enabled=true test_config:attack_params:type=\"sarsa\"
```

## How To Run The Code

The repository still uses the original subproject entrypoints:

- `SA-DQN/train.py`
- `SA-DQN/test.py`
- `SA-DDPG/train_ddpg.py`
- `SA-DDPG/eval_ddpg.py`
- `SA-PPO/src/run.py`
- `SA-PPO/src/test.py`

Each family uses JSON config files plus optional CLI overrides. Example:

```bash
cd SA-DQN
python3 test.py --config config/RoadRunner_cov.json test_config:attack=true test_config:attack_config:params:niters=50
```

WSL examples:

```bash
cd /mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/SA-DQN
source ../.venv/bin/activate
python3 train.py --config config/Pong_pgd.json
```

```bash
cd /mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/SA-PPO/src
source ../../.venv/bin/activate
python3 run.py --config-path config_hopper_robust_ppo_sgld.json
```

```bash
cd /mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/SA-DDPG
source ../.venv/bin/activate
python3 train_ddpg.py --config config/Ant_robust_sgld.json
```

## How To Add New Experiments

### Add a new config

Start from the closest existing JSON file and only change the parameters needed
for the new variant.

Examples:

- add a new Atari config in `SA-DQN/config/`
- add a new MuJoCo DDPG config in `SA-DDPG/config/`
- add a new PPO config in `SA-PPO/src/`

### Register it at the project level

Add the new experiment to:

- [experiment_registry.py](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/project_utils/experiment_registry.py)

Then it will show up in:

```bash
python3 scripts/experiments.py
```

### Keep the paper mapping explicit

When you add a new experiment, document:

- the intended environment
- the method variant
- the threat model
- the exact train command
- the exact evaluation commands

## Dependencies And Environment Setup

At minimum, expect:

- Python `3.7+`
- `torch`
- `gym`
- Atari dependencies for `SA-DQN`
- MuJoCo dependencies for `SA-PPO` and `SA-DDPG`

Use the subproject `requirements.txt` files as the source of truth:

- [SA-DQN/requirements.txt](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/SA-DQN/requirements.txt)
- [SA-DDPG/requirements.txt](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/SA-DDPG/requirements.txt)
- [SA-PPO/requirements.txt](/mnt/c/Users/admin/Desktop/Project/Robust_RL/random-projection-sa-mdp/SA-PPO/requirements.txt)

## Major Refactoring Decisions

The refactor in this repository intentionally avoided changing the optimization
logic or attack logic. The main changes were structural:

- centralized duplicated nested-config parsing into `project_utils/config.py`
- added a canonical experiment registry in `project_utils/experiment_registry.py`
- added `scripts/experiments.py` so experiment discovery is no longer spread across three READMEs
- added project-level documentation that maps paper sections to concrete scripts and configs

This keeps the implementation faithful to the paper while making reproduction
and extension materially easier.
