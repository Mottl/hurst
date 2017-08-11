# hurst
### Hurst exponent evaluation and R/S-analysis

This is a small python-module for analysing time-series and evaluating Hurst exponent (H).

H = 0.5 — random data.  
0.5 < H < 1.0 — persistent behavior.  
0 < H < 0.5 — anti-persistent behavior.  

### Usage

    from hurst import compute_Hc

    price = [100.] * 100
    H, c = compute_Hc(price)
