## examples for scipy utilities

### multi-variable curve_fit

https://stackoverflow.com/questions/28372597/python-curve-fit-with-multiple-independent-variables

```python
line = lambda x, zp, c: x[0] + c * x[1] + zp

y = tab_fit_std['rMeanApMag']
x = tab_fit_img['MAG_APER_9']
cx = tab_fit_std['gMeanApMag'] - tab_fit_std['rMeanApMag']

popt, pcov= optimize.curve_fit(line, xdata=(x,cx), ydata=y)
perr = np.sqrt(np.diag(pcov))
popt, pcov, perr
```

### iteratively curve_fit

```
def fit(model, xdata, ydata, guess, maxiters, thres=1e-3):
    _popt = guess
    for i in range(maxiters):
        popt, pcov = optimize.curve_fit(model, xdata=xdata, ydata=ydata, p0=_popt)
        diff = np.abs(((popt-_popt)/_popt).mean())
        if diff <= thres:
            break
        else:
            _popt = popt
#             print(i)
    return popt,pcov,diff
```
