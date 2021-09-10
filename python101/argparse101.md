### 读取文件名或文件名列表或文件名列表文件

```python
import argparse

parser = argparse.ArgumentParser(prog='update_web', description='appending new json files and generate html.')
parser.add_argument('-f', '--file', nargs='+', dest='files', help='json file list')
#parser.add_argument('-t', '--threshold', nargs='?', dest='thres', const='30', default='30',type=int, help='threshold in minute for new jsonfile detection')
args = parser.parse_args()
files = args.files
#threshold = 10*args.thres
```

实例:[从多个json文件获取内容生成网页](/home/liuxing/git/program101/python101/argparse/update_web.py)