## Copyright (C) 2019, Huan Zhang <huan@huan-zhang.com>
##                     Hongge Chen <chenhg@mit.edu>
##                     Chaowei Xiao <xiaocw@umich.edu>
## 
## This program is licenced under the BSD 2-Clause License,
## contained in the LICENCE file in this directory.
##
import argparse
from pathlib import Path
import random
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from project_utils.config import parse_cli_overrides

def argparser(seed = 2019):

    parser = argparse.ArgumentParser()

    # configure file 
    parser.add_argument('--config', default="UNSPECIFIED.json")
    parser.add_argument('--model_subset', type=int, nargs='+', 
            help='Use only a subset of models in config file. Pass a list of numbers starting with 0, like --model_subset 0 1 3 5')
    parser.add_argument('--path_prefix', type=str, default="", help="override path prefix")
    parser.add_argument('--seed', type=int, default=seed)
    parser.add_argument('overrides', type=str, nargs='*',
                                help='overriding config dict')
    
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)

    # for dual norm computation, we will have 1 / 0.0 = inf
    np.seterr(divide='ignore')

    args.overrides_dict = parse_cli_overrides(args.overrides, allow_literal_eval=True)

    return args
