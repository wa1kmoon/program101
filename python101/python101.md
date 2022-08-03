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
import time as tt
times=['2021-08-22T09:18:18', '2021-08-22T21:41:04','2021-08-22T22:00:23'] #爆发时间, 第一张开始时间, 最后一张结束时间
timess=[]
for time in times:
    tim=tt.strptime(time,'%Y-%m-%dT%H:%M:%S') # 格式解析
    timess.append(tt.mktime(tim)) # 转换为时间戳(s为单位)

inter=(np.array(timess)[1:]- np.array(timess)[0]) # 计算距离爆发开始的间隔

# 时间戳转化为格式话时间:
time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(midtime)) # midtime为时间戳, 先转换成localtime, 再转换成格式化时间
```

### 使用json库读写json文件

```python
with open(newfile,'r') as nf:
    njs=json.load(nf) # 读取json内容为一个列表

with open(objfile,'r') as of:
    ojs=json.load(of)
    
print(len(ojs+njs))

with open(objfile,'w') as of:
    json.dump(ojs+njs, of, ensure_ascii=False, indent=4) # 将json格式列表写入json文件, indent表示缩进,没有indent就没有格式. ensure_ascii=False是为了使汉字能正常写入
```

### 删除列表里的指定字符串, 列表本身将被改变

```python
def delsp(list, str):
    while True:
        if str in list:
            list.remove(str)
        else:
            break
    return list
```

### pdf转jpg

```python
### Time: 20190904
### Author: YaoLing
### Des: pdf convert to jpg

# -*- coding: UTF-8 -*-

from pdf2image import convert_from_path ## pip install pdf2image  or pip install --user pdf2image

pdf_name = "1.pdf"
jpg_name =pdf_name[:-4]+'.jpg'

pages = convert_from_path(pdf_name, 500)
for idx,page in enumerate(pages):
    page.save(str(idx+1)+jpg_name, 'JPEG')
```

### 回到行首重新输出

```python
import sys

def progress(i):
    progress = i/10000
    sys.stdout.write("Progress:{} {:.2f}%  \r".format('+'*int(80*progress) + '-'*(80-int(80*progress)), progress*100))
    #sys.stdout.flush()

for i in range(10001):
    progress(i)
```

### 计算众数

```python
def mode(data, binsize=0.01):
    """
    binsize(float): precision of the calculated mode value.
    """
    nbin = int((data.max()-data.min())/binsize)
    hist,bins = np.histogram(data, bins=nbin)
    cbin = (bins[1:]+bins[:-1])/2
    mode=cbin[np.where(hist==hist.max())[0]][0]
    return mode
```

### 在jupyter中重新加载模块

https://blog.csdn.net/ybdesire/article/details/86709727

```python
# python 2.x
import module
reload(module)

# python 3.2 3.3
import mudule
import importlib
importlib.reload(module)

# pyhon 3.4+
import module
import imp
imp.reload(module)

```

### reading docs

#### 函数定义: 使用'/','*'进行位置参数和关键字参数的指定

```python
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
        |        Positional or keyword   |
        |                                - Keyword only
         -- Positional only

```

在这里还可以发现更多细节，特定形参可以被标记为 仅限位置。 如果是 仅限位置 的形参，则其位置是重要的，并且该形参不能作为关键字传入。 仅限位置形参要放在 / (正斜杠) 之前。 这个 / 被用来从逻辑上分隔仅限位置形参和其它形参。 如果函数定义中没有 /，则表示没有仅限位置形参。

在 / 之后的形参可以为 位置或关键字 或 仅限关键字。

要将形参标记为 仅限关键字，即指明该形参必须以关键字参数的形式传入，应在参数列表的第一个 仅限关键字 形参之前放置一个 *。

仅限位置形参的名称可以在 **kwds 中使用而不产生歧义。

#### 解包参数列表

使用'*'操作符解包列表和元素**提供位置参数**:
```python
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]
```

使用'\*\*'操作符解包字典**提供关键字参数**:
```python
>>> def parrot(voltage, state='a stiff', action='voom'):
...     print("-- This parrot wouldn't", action, end=' ')
...     print("if you put", voltage, "volts through it.", end=' ')
...     print("E's", state, "!")
...
>>> d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
>>> parrot(**d)
-- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !
```
