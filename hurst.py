"""
	Hurst exponent and RS-analysis
	https://en.wikipedia.org/wiki/Hurst_exponent
	https://en.wikipedia.org/wiki/Rescaled_range
"""

__version__ = '0.0.1'

import numpy as np
import math

def to_inc(x):
	pct = map(lambda x1,x2: float(x2)-x1, x, x[1:])
	return list(pct)

def to_pct(x):
	pct = map(lambda x1,x2: float(x2)/x1-1., x, x[1:])
	return list(pct)

"""
	get_RS - get rescaled range from time-series of values (i.e. stock prices)
"""
def get_RS(series):
	incs = to_inc(series)

	R = math.fabs(max(series)-min(series)) # range
	S = np.std(incs) # standard deviation
	return R/S

"""
	computeCH - compute c and H according to Hurst equiation
"""
def compute_Hc(series):
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
	H, c = np.linalg.lstsq(A, np.log10(RS))[0]
	c = 10**c
	return H, c

if __name__ == '__main__':
	prices = [100.]
	series = np.random.randn(99999)
	for pct_change in series:
		prices.append(prices[-1] * (1.+pct_change/100))

	H, c = compute_Hc(prices)
	print("H={}, c={}".format(H,c))
