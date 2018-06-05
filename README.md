# hurst
### Hurst exponent evaluation and R/S-analysis

This is a small python-module for analysing time-series and evaluating Hurst exponent (H).

H = 0.5 — random data.  
0.5 < H < 1.0 — persistent behavior.  
0 < H < 0.5 — anti-persistent behavior.  

### Usage
```python
import matplotlib.pyplot as plt
from hurst import compute_Hc

price = [100.] * 100
H, c, data = compute_Hc(price)
print("H={}, c={}".format(H, c))
timeinterval = data[0]
RS = data[1]

plt.scatter(timeinterval, RS)
```
