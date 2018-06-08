# hurst
### Hurst exponent evaluation and R/S-analysis

This is a small python-module for analysing __random walks__ and evaluating the __Hurst exponent (H)__.

H = 0.5 — random data.  
0.5 < H < 1.0 — persistent behavior.  
0 < H < 0.5 — anti-persistent behavior.  

### Usage
```python
import matplotlib.pyplot as plt
import numpy as np
import matplotplotlib.pyplot as plt
from hurst import compute_Hc


""" Generate random walk series """
series = np.empty(shape=(99999,))  # create an empty array
series[0] = 0.  # initialize the first element with some value
for i in range(1,len(series)):
    series[i] = series[i-1] + np.random.randn()

""" Evaluate Hurst equation """
H, c, data = hurst.compute_Hc(series)

""" Plot """
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
