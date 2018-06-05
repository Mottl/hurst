#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Hurst exponent and RS-analysis
https://en.wikipedia.org/wiki/Hurst_exponent
https://en.wikipedia.org/wiki/Rescaled_range
"""

__version__ = '0.0.2'

import sys
import math
import numpy as np
try:
    import pandas as pd
except:
    pass

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
    if R == 0 or S == 0:
        return 0  # return 0 to skip this interval due undefined R/S
    return R / S

def compute_Hc(series, min_window=10):
    """
    Compute H (Hurst exponent) and C according to Hurst equiation:
    E(R/S) = c * T^H

    Refer to https://en.wikipedia.org/wiki/Hurst_exponent

    Parameters
    ----------

    series : array-like
        (Time-)series

    min_window : int, default 10
        the minimal window size for R/S calculation

    Returns tuple of
        H, c and data
        where H and c — parameters or Hurst equiation
        and data is a list of 2 lists: time intervals and R/S-values for correspoding time interval
        for further plotting log(data[0]) on X and log(data[1]) on Y
    """

    if len(series)<100:
        raise ValueError("Series length must be greater or equal to 100")

    ndarray_likes = [np.ndarray]
    if "pandas.core.series" in sys.modules.keys():
        ndarray_likes.append(pd.core.series.Series)

    # convert series to numpy array if series is not numpy array or pandas Series
    if type(series) not in ndarray_likes:
        series = np.array(series)

    if "pandas.core.series" in sys.modules.keys() and type(series) == pd.core.series.Series:
        if series.isnull().values.any():
            raise ValueError("Series contains NaNs")    
    elif np.isnan(np.min(series)):
        raise ValueError("Series contains NaNs")

    err = np.geterr()
    np.seterr(all='raise')

    window_sizes = list(map(
        lambda x: int(10**x),
        np.arange(math.log10(min_window), math.log10(len(series)-1), 0.25)))
    window_sizes.append(len(series))

    RS = []
    for w in window_sizes:
        rs = []
        for start in range(0, len(series), w):
            if (start+w)>len(series):
                break
            _ = get_RS(series[start:start+w])
            if _ != 0:
                rs.append(_)
        RS.append(np.mean(rs))

    A = np.vstack([np.log10(window_sizes), np.ones(len(RS))]).T
    H, c = np.linalg.lstsq(A, np.log10(RS), rcond=-1)[0]
    np.seterr(**err)

    c = 10**c
    return H, c, [window_sizes, RS]

if __name__ == '__main__':
    prices = [100.]
    series = np.random.randn(99999)
    for pct_change in series:
        prices.append(prices[-1] * (1.+pct_change/100))

    H, c, data = compute_Hc(np.array(prices))
    print("H={:.4f}, c={:.4f}".format(H,c))
