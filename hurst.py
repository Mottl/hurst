#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Hurst exponent and RS-analysis
https://en.wikipedia.org/wiki/Hurst_exponent
https://en.wikipedia.org/wiki/Rescaled_range
"""

__version__ = '0.0.2'

import numpy as np
import math

def _to_inc(x):
    _x = x if type(x) == np.ndarray else np.array(x)
    incs = _x[1:] - _x[:-1]
    return incs

def _to_pct(x):
    _x = x if type(x) == np.ndarray else np.array(x)
    pcts = _x[1:] / _x[:-1] - 1.
    return pcts

def get_RS(series):
    """
    Get rescaled range from time-series of values (i.e. stock prices)

    Parameters
    ----------

    series : array-like
        (Time-)series
    """

    incs = _to_inc(series)

    R = max(series)-min(series) # range
    S = np.std(incs) # standard deviation
    return R/S

def compute_Hc(series):
    """
    Compute H (Hurst exponent) and C according to Hurst equiation:
    E(R/S) = c * T^H

    Refer to https://en.wikipedia.org/wiki/Hurst_exponent

    Parameters
    ----------

    series : array-like
        (Time-)series
    """

    if len(series)<100:
        raise ValueError("Series length must be greater or equal to 100")

    window_sizes = list(map(
        lambda x: int(10**x),
        np.arange(1., math.log10(len(series)-1), 0.25)))
    window_sizes.append(len(series))

    RS = []
    for w in window_sizes:
        rs = []
        for start in range(0, len(series), w):
            if (start+w)>len(series):
                break
            rs.append(get_RS(series[start:start+w]))
        RS.append(np.average(rs))

    A = np.vstack([np.log10(window_sizes), np.ones(len(RS))]).T
    H, c = np.linalg.lstsq(A, np.log10(RS), rcond=-1)[0]
    c = 10**c
    return H, c

if __name__ == '__main__':
    prices = [100.]
    series = np.random.randn(99999)
    for pct_change in series:
        prices.append(prices[-1] * (1.+pct_change/100))

    H, c = compute_Hc(np.array(prices))
    print("H={:.4f}, c={:.4f}".format(H,c))
