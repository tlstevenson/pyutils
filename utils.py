# -*- coding: utf-8 -*-
"""
Helper functions

@author: tanner stevenson
"""

import numpy as np
import os
import os.path as path
import matplotlib.colors as mc
import colorsys

# %% Number utils
def is_scalar(x):
    return np.ndim(x) == 0

def convert_to_multiple(value, factor, direction='nearest'):

    match direction:
        case 'nearest':
            return factor * np.round(value/factor)
        case 'up':
            return factor * np.ceil(value/factor)
        case 'down':
            return factor * np.floor(value/factor)


def stderr(x, axis=0, ignore_nan=True):
    ''' Calculates standard error '''

    x = np.array(x)

    if ignore_nan:
        std = np.nanstd(x, axis)
        n = np.sum(np.logical_not(np.isnan(x)), axis)
    else:
        std = np.std(x, axis)
        n = np.shape(x)[axis]

    se = std/np.sqrt(n)
    se[np.isinf(se)] = np.nan  # handle cases where n = 0
    return se

# %% OS utils
def check_make_dir(full_path):
    path_dir = os.path.dirname(full_path)
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)


def get_user_home():
    return path.expanduser('~')

## Object utils
def flatten_dict_array(dict_array):
    ''' flattens a dictionary of lists '''
    return [i for v in dict_array.values() for i in v]


# %% Plot utils
def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    From: https://gist.github.com/technic/8bf3932ad7539b762a05da11c0093ed5

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = np.array(colorsys.rgb_to_hls(*mc.to_rgb(c)))
    return colorsys.hls_to_rgb(c[0], 1-amount * (1-c[1]), c[2])

