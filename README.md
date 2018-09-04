# hurst
## Hurst exponent evaluation and R/S-analysis

[![pypi](https://img.shields.io/pypi/v/hurst.svg)](https://pypi.org/project/hurst/)
![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)
![Python 3x](https://img.shields.io/badge/python-3.x-blue.svg)
[![Build Status](https://travis-ci.org/Mottl/hurst.svg?branch=master)](https://travis-ci.org/Mottl/hurst)

**hurst** is a small Python module for analysing __random walks__ and evaluating the __Hurst exponent (H)__.

H = 0.5 — Brownian motion,  
0.5 < H < 1.0 — persistent behavior,  
0 < H < 0.5 — anti-persistent behavior.  

## Usage
Install **hurst** module with  
```bash
pip install hurst
```

or  

```bash
pip install -e https://github.com/Mottl/hurst
```

```python
import matplotlib.pyplot as plt
import numpy as np
import matplotplotlib.pyplot as plt
from hurst import compute_Hc, random_walk

# Use random_walk() function or generate a random walk series manually:
# series = random_walk(99999, cumprod=True)
np.random.seed(42)
random_changes = 1. + np.random.randn(99999) / 1000.
series = np.cumprod(random_changes)  # create a random walk from random changes

# Evaluate Hurst equation
H, c, data = compute_Hc(series, kind='price', simplified=True)

# Plot
f, ax = plt.subplots()
ax.plot(data[0], c*data[0]**H, color="deepskyblue")
ax.scatter(data[0], data[1], color="purple")
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('Time interval')
ax.set_ylabel('R/S ratio')
ax.grid(True)
plt.show()

print("H={:.4f}, c={:.4f}".format(H,c))
```


![R/S analysis](https://github.com/Mottl/hurst/raw/master/examples/regression.png?raw=true "R/S analysis")

```H=0.4964, c=1.4877```

## Brownian motion, persistent and antipersistent random walks
You can generate random walks with `random_walk()` function as following:

### Brownian
```brownian = random_walk(99999, proba=0.5)```


![Brownian motion](https://github.com/Mottl/hurst/raw/master/examples/Brownian_motion.png?raw=true "Brownian motion")

### Persistent
```persistent = random_walk(99999, proba=0.7)```


![Persistent random walk](https://github.com/Mottl/hurst/raw/master/examples/Persistent.png?raw=true "Persistent random walk")

### Antipersistent
```antipersistent = random_walk(99999, proba=0.3)```


![Antipersistent random walk](https://github.com/Mottl/hurst/raw/master/examples/Antipersistent.png?raw=true "Antipersistent random walk")
