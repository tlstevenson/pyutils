#!/usr/bin/env python3
import init
import utils 
import os
import torch
import numpy as np
import pandas as pd
import json
import sys
import argparse

def main(config_path, custom_num):
    
    print('Config path: {}'.format(config_path))
    print('Custom num: {}'.format(custom_num))

    if os.path.exists(config_path):
        print('Config file found')
        with open(config_path, "r") as f:
            config = json.load(f)
            print('config file contents:\n{}'.format(config))
    else:
        print('Config file was not found')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--config_path')

    parser.add_argument('--custom_num')

    args = parser.parse_args()
    
    main(args.config_path, args.custom_num)



