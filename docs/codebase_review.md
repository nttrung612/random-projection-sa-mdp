# Codebase Review

This note records how the codebase is organized today, what parts correspond to
the paper, and which problems should be addressed before extending the work.

## Repository-to-Paper Map

### `SA-DQN/`

Relevant files:

- `train.py`: Atari training loop, replay buffer integration, robust loss, target updates
- `test.py`: evaluation loop, PGD attack, optional certification
- `models.py`: Q-network definitions and model construction
- `attacks.py`: attack implementations used during evaluation and adversarial training
- `defaults.json` and `config/*.json`: baseline experiment definitions
- `common/`: wrappers, layers, replay buffer helpers

Paper alignment:

- Implements the Atari experiments from Table 1 and Table 2.
- The paper's RP front-end is represented by `training_config.rp_dim` and `training_config.rp_lambda`.
- `bound_solver` switches between convex-style and PGD-style robust training.

### `SA-DDPG/`

Relevant files:

- `train_ddpg.py`: training entrypoint and config translation into `deep_rl`
- `eval_ddpg.py`: evaluation entrypoint, attack orchestration, optional Sarsa pretraining
- `robust_ddpg.py`: the robust actor-critic implementation, including the optional RP front-end
- `train_sarsa.py` and `sarsa_ddpg.py`: robust Sarsa attack support
- `config/*.json`: environment-specific experiment overrides

Paper alignment:

- Implements the SA-DDPG experiments in Table 4.
- The strongest-attack evaluation is composed in `eval_ddpg.py`.
- The RP variant is not broken out into dedicated config files; it is enabled by an optional top-level `rp` config block.

### `SA-PPO/src/`

Relevant files:

- `run.py`: training entrypoint and CLI
- `test.py`: evaluation, attack orchestration, Sarsa training, result dumping
- `policy_gradients/agent.py`: trainer and rollout logic
- `policy_gradients/models.py`: policy/value networks, including RP front-end support
- `config_*.json`: experiment definitions

Paper alignment:

- Implements the SA-PPO experiments in Table 3.
- Only the SGLD PPO configs currently include RP-specific parameters.
- Attack evaluation covers MAD and RS workflows described in the paper.

## Main Problems Found

### 1. Duplicate config-parsing logic

`SA-DQN` and `SA-DDPG` both reimplemented:

- nested override parsing;
- recursive dict merges;
- "defaults + config + CLI override" loading.

That duplication increases maintenance cost and makes behavior drift likely.

### 2. No project-level experiment index

The repo had subproject READMEs, but no single source of truth for:

- which configs correspond to which paper tables;
- which commands reproduce which experiment;
- where RP-specific variants live.

### 3. Mixed active code and vendored / duplicated code

Examples:

- `SA-DQN-/SA-DQN/` duplicates the active `SA-DQN/` tree
- multiple vendored `auto_LiRPA` and `cox` copies exist

This makes it harder to determine which files are authoritative.

### 4. Weak naming around variants

The paper is framed around `RP-LN` and `ResRP`, but the code exposes RP support
through parameters like:

- `rp_dim`
- `rp_lambda`
- `rp_cfg`
- `rp_dim_factor`

Those names are implementation-oriented, not experiment-oriented, so the paper
to code mapping is harder than necessary.

### 5. Reproduction knowledge is spread across READMEs and scripts

Important details were split between:

- subproject READMEs
- bash helper scripts
- JSON configs
- implicit defaults

That is workable for the original authors, but poor for reproduction by a new contributor.

## Refactoring Done In This Pass

### Shared configuration utilities

Added:

- `project_utils/config.py`

Refactored:

- `SA-DQN/argparser.py`
- `SA-DQN/read_config.py`
- `SA-DDPG/argparser.py`
- `SA-DDPG/config.py`

Why:

- removes duplicated parsing logic;
- keeps override behavior consistent across DQN and DDPG;
- reduces the chance of subtle reproduction bugs when adding new nested config keys.

### Canonical experiment registry

Added:

- `project_utils/experiment_registry.py`
- `scripts/experiments.py`

Why:

- creates a project-level index of the paper experiments;
- gives one stable place to discover training and evaluation commands.

### Documentation structure

Added:

- `docs/paper_experiments.md`
- root `README.md`

Why:

- makes the codebase understandable without reading three unrelated READMEs first;
- preserves the paper-to-code mapping for future extensions.

## Proposed Next Structural Step

If you want to continue refactoring beyond this pass, the cleanest next move is
to create a top-level structure like this:

```text
docs/
  paper_experiments.md
  codebase_review.md
experiments/
  atari/
  mujoco/
project_utils/
  config.py
  experiment_registry.py
SA-DQN/
SA-DDPG/
SA-PPO/
scripts/
  experiments.py
```

That preserves the original algorithm implementations while moving all
reproduction and orchestration concerns to the top level.

