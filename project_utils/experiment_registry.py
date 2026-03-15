"""Canonical experiment metadata for the paper and this repository."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class Experiment:
    key: str
    family: str
    environment: str
    variant: str
    paper_section: str
    config_path: str
    train_command: str
    eval_commands: List[str]
    notes: str


EXPERIMENTS: List[Experiment] = [
    Experiment(
        key="dqn-pong-pgd",
        family="SA-DQN",
        environment="Pong",
        variant="SA-DQN (PGD baseline)",
        paper_section="Table 1 / Table 2 context",
        config_path="SA-DQN/config/Pong_pgd.json",
        train_command="cd SA-DQN && python3 train.py --config config/Pong_pgd.json",
        eval_commands=[
            "cd SA-DQN && python3 test.py --config config/Pong_pgd.json",
            "cd SA-DQN && python3 test.py --config config/Pong_pgd.json test_config:attack=true",
            "cd SA-DQN && python3 test.py --config config/Pong_pgd.json test_config:attack=true test_config:attack_config:params:niters=50",
        ],
        notes="Vanilla/adv/convex/pgd Atari baselines live under SA-DQN/config/*.json.",
    ),
    Experiment(
        key="dqn-fre/bank/roadrunner",
        family="SA-DQN",
        environment="Freeway / BankHeist / RoadRunner",
        variant="Atari comparison suite",
        paper_section="Table 1",
        config_path="SA-DQN/config/{Freeway,BankHeist,RoadRunner}_{nat,cov,pgd,adv}.json",
        train_command="cd SA-DQN && python3 train.py --config config/<ENV>_<VARIANT>.json",
        eval_commands=[
            "cd SA-DQN && python3 test.py --config config/<ENV>_<VARIANT>.json",
            "cd SA-DQN && python3 test.py --config config/<ENV>_<VARIANT>.json test_config:attack=true",
        ],
        notes="Repo defaults include RP hooks via training_config.rp_dim and training_config.rp_lambda.",
    ),
    Experiment(
        key="ppo-hopper-walker-humanoid-sgld",
        family="SA-PPO",
        environment="Hopper-v2 / Walker2d-v2 / Humanoid-v2",
        variant="SGLD and SGLD+RP-LN",
        paper_section="Table 3",
        config_path="SA-PPO/src/config_{hopper,walker,humanoid}_robust_ppo_sgld.json",
        train_command="cd SA-PPO/src && python3 run.py --config-path config_<ENV>_robust_ppo_sgld.json",
        eval_commands=[
            "cd SA-PPO/src && python3 test.py --config-path config_<ENV>_robust_ppo_sgld.json --exp-id <EXP_ID> --deterministic",
            "cd SA-PPO/src && python3 test.py --config-path config_<ENV>_robust_ppo_sgld.json --load-model <MODEL> --attack-method action --deterministic",
            "cd SA-PPO/src && python3 test.py --config-path config_<ENV>_robust_ppo_sgld.json --load-model <MODEL> --sarsa-enable --sarsa-model-path <SARSA_MODEL>",
        ],
        notes="Only the SGLD PPO configs currently include RP-specific JSON fields.",
    ),
    Experiment(
        key="ddpg-ant-hopper-reacher",
        family="SA-DDPG",
        environment="Ant-v2 / Hopper-v2 / Reacher-v2",
        variant="SGLD, convex, and SGLD+RP-LN",
        paper_section="Table 4",
        config_path="SA-DDPG/config/{Ant,Hopper,Reacher}_{robust,robust_sgld,vanilla}.json",
        train_command="cd SA-DDPG && python3 train_ddpg.py --config config/<ENV>_<VARIANT>.json",
        eval_commands=[
            "cd SA-DDPG && python3 eval_ddpg.py --config config/<ENV>_<VARIANT>.json",
            "cd SA-DDPG && python3 eval_ddpg.py --config config/<ENV>_<VARIANT>.json test_config:attack_params:enabled=true",
        ],
        notes="The DDPG code already accepts an optional top-level rp block in the JSON config.",
    ),
]


def iter_experiments() -> Iterable[Experiment]:
    return EXPERIMENTS


def experiments_by_family() -> Dict[str, List[Experiment]]:
    grouped: Dict[str, List[Experiment]] = {}
    for experiment in EXPERIMENTS:
        grouped.setdefault(experiment.family, []).append(experiment)
    return grouped

