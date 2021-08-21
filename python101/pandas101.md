### 读取csv文件

```python
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
import pandas as pd

sd=pd.read_csv('./Seeing_Data.csv', low_memory=False, header=None) # low_memory设置是避免'DtypeWarning: Columns (5) have mixed types'这样的警告

print(sd)

jd=np.array(sd.loc[:,2]).astype('float')
seeing=np.array(sd.loc[:,5]).astype('float') # sd.loc[:,2]表示读取第2列, sd.loc[2]表示读取第2行

fig1=plt.figure(figsize=(25,7))
plt.scatter(jd,seeing)
y_loc=MultipleLocator(0.5)
x_loc=MultipleLocator(90)
ax=plt.gca()
ax.yaxis.set_major_locator(y_loc)
ax.xaxis.set_major_locator(x_loc)
```