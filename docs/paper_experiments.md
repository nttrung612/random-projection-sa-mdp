# Paper Experiments

This document summarizes the experiments described in the bundled paper,
`Random Projection Meets Robust Deep Reinforcement Learning: Toward Adversarially Resilient Policies`, and maps them to the repository.

## Core Idea

The paper keeps the original SA-MDP robust RL training procedures intact and
adds a front-end transformation before the policy/value network:

- `RP-LN`: fixed Gaussian random projection, followed by layer normalization and ReLU.
- `ResRP`: a residual blend between projected features and a skip path, again followed by layer normalization and ReLU.

The stated goal is to expand local margins in representation space while
preserving the original SA-MDP attack and training pipelines.

## Threat Model

The paper evaluates under the SA-MDP observation attack model:

- the environment evolves from the true state;
- the adversary perturbs the observation seen by the policy;
- perturbations are bounded per step.

Evaluation settings used in the paper:

- `Natural`: no adversarial perturbation.
- `PGD-10` and `PGD-50`: untargeted `L_inf` projected-gradient attacks.
- `MAD`: maximal action-difference attack.
- `RS`: robust Sarsa attack.
- `RS+MAD`: combined strong attack used in actor-critic evaluation.

## Atari Experiments

Section `7.3` evaluates DQN-style agents on Atari.

Primary comparison table:

- Environments: `Freeway`, `BankHeist`, `RoadRunner`
- Methods: `SA-DQN (PGD)`, `SA-DQN (Convex)`, `RP-LN`, `ResRP`
- Metrics: mean ± std over 50 episodes under `Natural`, `PGD-10`, and `PGD-50`

Additional from-scratch RP-LN table:

- Environments: `Enduro`, `Alien`, `FishingDerby`
- Methods: `SA-DQN (PGD)` vs `RP-LN`
- Metrics: `Natural`, `PGD-10`, `PGD-50`, `MAD`

Main reported conclusions:

- `RP-LN` improves PGD robustness over `SA-DQN (PGD)` with small natural-performance change.
- `SA-DQN (Convex)` remains strongest on `BankHeist` and `RoadRunner`.

## Continuous-Control Experiments

Section `7.4` evaluates the same front-end idea on robust actor-critic methods.

### SA-PPO

Table `3` reports:

- Environments: `Hopper-v2`, `Walker2d-v2`, `Humanoid-v2`
- Methods: `SGLD` and `SGLD+RP-LN`
- Metrics: mean ± std over 50 episodes, aggregated across 15 trained agents
- Evaluation columns: `Natural`, `MAD`, `RS`, `RS+MAD`

Paper takeaway:

- RP-LN usually improves worst-case returns on Hopper and Walker under strong attacks.
- Gains on Humanoid are smaller but still competitive.

### SA-DDPG

Table `4` reports:

- Environments: `Ant-v2`, `Hopper-v2`, `Reacher-v2`
- Methods: `SGLD`, `Convex`, `SGLD+RP-LN`
- Metrics: mean ± std over 50 episodes for the median agent among 11 trained agents
- Evaluation columns: `Natural Reward`, `Best Attack Reward`

Paper takeaway:

- RP-LN is strongest on `Ant`.
- Convex remains competitive or best on some tasks.
- Natural-reward changes are task-dependent.

## How This Repository Encodes Those Experiments

- `SA-DQN/` contains the Atari training and evaluation pipeline.
- `SA-DDPG/` contains the off-policy MuJoCo pipeline.
- `SA-PPO/src/` contains the on-policy MuJoCo pipeline.

The random-projection additions appear in the active codebase as:

- `SA-DQN/defaults.json`
  - `training_config.rp_dim`
  - `training_config.rp_lambda`
- `SA-DDPG/robust_ddpg.py`
  - optional top-level `rp` config block
- `SA-PPO/src/policy_gradients/models.py`
  - `rp_dim_factor`
  - `rp_lambda`

## Canonical Reproduction Entry Points

- `python3 scripts/experiments.py`
  - lists the paper experiments and their canonical commands

