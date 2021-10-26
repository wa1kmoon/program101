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