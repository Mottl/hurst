# hurst
## Hurst exponent evaluation and R/S-analysis

[![Build Status](https://travis-ci.org/Mottl/hurst.svg?branch=master)](https://travis-ci.org/Mottl/hurst)

**hurst** is a small Python module for analysing __random walks__ and evaluating the __Hurst exponent (H)__.

H = 0.5 — Brownian motion,  
0.5 < H < 1.0 — persistent behavior,  
0 < H < 0.5 — anti-persistent behavior.  

## Usage
```python
import matplotlib.pyplot as plt
import numpy as np
import matplotplotlib.pyplot as plt
from hurst import compute_Hc, random_walk

# Use random_walk() function or generate a random walk series manually:
random_increments = np.random.randn(99999) 
series = np.cumsum(random_increments)  # create a random walk from random increments

# Evaluate Hurst equation
H, c, data = hurst.compute_Hc(series)

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


![R/S analysis](examples/regression.png?raw=true "R/S analysis")

```H=0.4964, c=1.4877```

## Brownian motion, persistent and antipersistent random walks
You can generate random walks with `random_walk()` function as following:

### Brownian
```brownian = random_walk(99999, proba=0.5)```


![Brownian motion](examples/Brownian_motion.png?raw=true "Brownian motion")

### Persistent
```persistent = random_walk(99999, proba=0.7)```


![Persistent random walk](examples/Persistent.png?raw=true "Persistent random walk")

### Antipersistent
```antipersistent = random_walk(99999, proba=0.3)```


![Antipersistent random walk](examples/Antipersistent.png?raw=true "Antipersistent random walk")
