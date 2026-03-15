"""Helpers shared by the DQN and DDPG experiment entrypoints.

These repositories were originally developed independently, but both use the
same nested `key:value=value` override convention and the same "defaults +
JSON + CLI overrides" loading pattern. Centralizing that behavior makes the
experiment entrypoints easier to reason about without changing their runtime
logic.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Dict, Iterable, MutableMapping


def deep_update(
    base: MutableMapping[str, Any],
    updates: MutableMapping[str, Any],
    show_warning: bool = False,
) -> MutableMapping[str, Any]:
    """Recursively merge ``updates`` into ``base``."""

    for key, value in updates.items():
        if key not in base and show_warning:
            print(
                "\033[91m Warning: key {} not found in config. "
                "Make sure to double check spelling and config option name. "
                "\033[0m".format(key)
            )
        if isinstance(value, dict):
            base[key] = deep_update(base.get(key, {}), value, show_warning)
        else:
            base[key] = value
    return base


def parse_override_value(value: str, allow_literal_eval: bool = False) -> Any:
    """Parse a CLI override value using the original repo conventions."""

    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    if allow_literal_eval:
        return ast.literal_eval(value)
    return value


def parse_cli_overrides(
    overrides: Iterable[str],
    allow_literal_eval: bool = False,
) -> Dict[str, Any]:
    """Parse ``a:b:c=value`` style overrides into nested dictionaries."""

    parsed: Dict[str, Any] = {}
    for override in overrides:
        key, raw_value = override.strip().split("=", 1)
        target = parsed
        key_parts = key.split(":")
        for part in key_parts[:-1]:
            if part not in target:
                target[part] = {}
            target = target[part]
        target[key_parts[-1]] = parse_override_value(
            raw_value,
            allow_literal_eval=allow_literal_eval,
        )
    return parsed


def load_config_file(
    defaults_path: str | Path,
    config_path: str | Path,
    overrides: Dict[str, Any] | None = None,
    show_override_warning: bool = True,
) -> Dict[str, Any]:
    """Load a config file on top of defaults and apply CLI overrides."""

    with Path(defaults_path).open() as handle:
        config = json.load(handle)
    with Path(config_path).open() as handle:
        deep_update(config, json.load(handle))
    if overrides:
        print("overriding parameters: \033[93mPlease check these parameters carefully.\033[0m")
        print("\033[93m" + str(overrides) + "\033[0m")
        deep_update(config, overrides, show_override_warning)
    return config
