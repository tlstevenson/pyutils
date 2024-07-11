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
from scipy.stats import binomtest

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


def to_int(x):
    return np.round(x).astype(int)


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

    # handle cases where n = 0
    if is_list(se):
        se[np.isinf(se)] = np.nan
    elif np.isinf(se):
        se = np.nan

    return se

def z_score(x):
    ''' Calculates z_score over all values in x '''

    # Flatten input to calculate z-score over all values in x
    x = np.array(x)
    flat_x = x.flatten()

    flat_z = (flat_x - np.nanmean(flat_x))/np.nanstd(flat_x)

    # reshape the z scores to match original x
    return np.reshape(flat_z, x.shape)

def binom_cis(k, n, level=0.95):
    # handle non-integer values
    if k % 1 != 0 or n % 1 != 0:
        raise ValueError('k and n must be integers. k={0}, n={1}'.format(k, n))
    else:
        k = int(k)
        n = int(n)
    if n > 1 and k > 1:
        return np.array(binomtest(k, n).proportion_ci(confidence_level=level)[:])
    else:
        return np.array([np.nan, np.nan])

def get_sequence_lengths(x):
    ''' Get a list of lengths of repeated values in array indexed by value '''
    unique_vals = np.unique(x)
    lengths = {v: [] for v in unique_vals}

    seq_len = 1
    for i in range(len(x)-1):
        if x[i] == x[i+1]:
            seq_len += 1

        if x[i] != x[i+1] or i == len(x)-2:
            lengths[x[i]].append(seq_len)
            seq_len = 1

    return lengths

# %% OS utils
def check_make_dir(full_path):
    path_dir = os.path.dirname(full_path)
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)

def get_user_home():
    return path.expanduser('~')

# %% Object utils

def flatten(lists, recursive=True):
    ''' flattens a structure of lists '''
    if recursive:
        if is_dict(lists):
            return flatten([i for v in lists.values() for i in v], recursive)
        elif is_list(lists) and len(lists) > 0 and is_list(lists[0]):
            return flatten([i for v in lists for i in v], recursive)
        else:
            return lists
    else:
        if is_dict(lists):
            return [i for v in lists.values() for i in v]
        elif is_list(lists) and is_list(lists[0]):
            return [i for v in lists for i in v]
        else:
            return lists


def is_dict(value):
    return isinstance(value, dict)

def is_list(value):
    return isinstance(value, list) or isinstance(value, tuple) or isinstance(value, np.ndarray)


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
