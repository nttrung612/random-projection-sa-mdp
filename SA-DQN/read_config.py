from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from project_utils.config import load_config_file


def update_dict(d, u, show_warning = False):
    from project_utils.config import deep_update

    return deep_update(d, u, show_warning)

def load_config(args):
    print("loading config file: {}".format(args.config))
    config = load_config_file("defaults.json", args.config, args.overrides_dict)
    if args.path_prefix:
        config["path_prefix"] = args.path_prefix
    return config
