# logging

## 1. 格式化输出, 指定输出颜色

https://cppsecrets.com/users/9837115971039711411510410110897114494848484864103109971051084699111109/Python-loggingHandlersetFormatter.php#:~:text=-%20setFormatter%20%28%29%20is%20a%20Handler%20class%20method.,in%20the%20core%20logging%20package%20or%20logging.handlers%20module.

https://www.jb51.net/article/181759.htm

```python
import logging

loglevel = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(loglevel)

streamhdl = logging.StreamHandler()
streamhdl.setLevel(loglevel)

filehdlr  = logging.FileHandler('setFormatter.txt')
filehdlr.setLevel(logging.INFO)

logger.addHandler(streamhdl)
logger.addHandler(filehdlr)

formatter = logging.Formatter("[%(asctime)s][%(name)s] %(levelname)s: %(message)s")

filehdlr.setFormatter(formatter1)
streamhdl.setFormatter(formatter)

def loginfo(logger, message):
    logger.info('\033[1;32m{}\033[0m'.format(message))

def logwarning(logger, message):
    logger.warning('\033[1;36m{}\033[0m'.format(message))

def logcritical(logger, message):
    logger.critical('\033[1;33m{}\033[0m'.format(message))

def logerror(logger, message):
    logger.error('\033[1;31m{}\033[0m'.format(message))
```
