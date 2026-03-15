#!/usr/bin/env python3
"""List the paper's experiments and the commands used to run them."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from project_utils.experiment_registry import experiments_by_family


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", help="Filter by experiment family, e.g. SA-DQN")
    args = parser.parse_args()

    grouped = experiments_by_family()
    families = [args.family] if args.family else sorted(grouped.keys())

    for family in families:
        experiments = grouped.get(family, [])
        if not experiments:
            continue
        print(family)
        print("-" * len(family))
        for experiment in experiments:
            print(f"{experiment.key}: {experiment.environment} [{experiment.variant}]")
            print(f"  paper: {experiment.paper_section}")
            print(f"  config: {experiment.config_path}")
            print(f"  train: {experiment.train_command}")
            for command in experiment.eval_commands:
                print(f"  eval:  {command}")
            print(f"  notes: {experiment.notes}")
            print()


if __name__ == "__main__":
    main()
