```python
# -*- coding: utf-8 -*-
```

### 使用.format()时如何显示花括号本身?

```python
id=2
print('{{{}}}'.format(id))
>>> {2}
```

### 时间戳

```python
from datetime import date as dt
t1='2021-04-04-17:08:34.333'
t2='2021-04-04-18:08:34.333'
time=dt.strptime(t1,'%Y-%m-%d-%H:%M:%S.%f')
deltat=t2-t1
print(deltat.total_seconds())
```