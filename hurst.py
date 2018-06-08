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
import warnings
import numpy as np
try:
    import pandas as pd
except:
    pass

def _to_inc(x):
    incs = x[1:] - x[:-1]
    return incs

def _to_pct(x):
    pcts = x[1:] / x[:-1] - 1.
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
    R = max(series) - min(series) # range
    S = np.std(incs)

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
        series = series.values  # convert pandas Series to numpy array
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

def random_walk(length, proba=0.5, min_lookback=1, max_lookback=100):
    """
    Generates a random walk series

    Parameters
    ----------

    proba : float, default 0.5
        the probability that the next increment will follow the trend.
        Set proba > 0.5 for the persistent random walk,
        set proba < 0.5 for the antipersistent one

    min_lookback: int, default 1
    max_lookback: int, default 100
        minimum and maximum window sizes to calculate trend direction
    """

    assert(min_lookback>=1)
    assert(max_lookback>=min_lookback)

    if max_lookback > length:
        max_lookback = length
        warnings.warn("max_lookback parameter has been set to the length of the random walk series.")

    series = [0.] * length  # array of prices
    for i in range(1, length):
        if i < min_lookback + 1:
            direction = np.sign(np.random.randn())
        else:
            lookback = np.random.randint(min_lookback, min(i-1, max_lookback)+1)
            direction = np.sign(series[i-1] - series[i-1-lookback]) * np.sign(proba - np.random.uniform())

        series[i] = series[i-1] + np.fabs(np.random.randn()) * direction

    return series

if __name__ == '__main__':
    series = np.empty(shape=(99999,))  # create an empty array
    series[0] = 0.  # initialize the first element with some value
    for i in range(1,len(series)):
        series[i] = series[i-1] + np.random.randn()

    """ Evaluate Hurst equation """
    H, c, data = hurst.compute_Hc(series)

    """ Plot """
    # uncomment the following make a plot using Matplotlib:
    """
    import matplotlib.pyplot as plt

    f, ax = plt.subplots()
    ax.plot(data[0], c*data[0]**H, color="deepskyblue")
    ax.scatter(data[0], data[1], color="purple")
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Time interval')
    ax.set_ylabel('R/S ratio')
    ax.grid(True)
    plt.show()
    """

    print("H={:.4f}, c={:.4f}".format(H,c))
