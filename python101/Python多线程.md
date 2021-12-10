### Python多线程与多进程

推荐一本教程：[Python并行编程 中文](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/index.html)

引用文章[Python中单线程、多线程和多进程的效率对比实验](https://www.runoob.com/w3cnote/python-single-thread-multi-thread-and-multi-process.html)的测试结论：

- 多线程在IO密集型的操作下似乎也没有很大的优势（也许IO操作的任务再繁重一些就能体现出优势），在CPU密集型的操作下明显地比单线程线性执行性能更差，但是对于网络请求这种忙等阻塞线程的操作，多线程的优势便非常显著了
- 多进程无论是在CPU密集型还是IO密集型以及网络请求密集型（经常发生线程阻塞的操作）中，都能体现出性能的优势。不过在类似网络请求密集型的操作上，与多线程相差无几，但却更占用CPU等资源，所以对于这种情况下，我们可以选择多线程来执行

### 多线程

多线程视频教程：[Python Threading Tutorial: Run Code Concurrently Using the Threading Module](https://www.youtube.com/watch?v=IEEhzQoKtQU)

#### threading

```python
import threading
import time

start = time.perf_counter()

def do_something(second):
    print('Start Sleeping')
    time.sleep(second)
    print('Done Sleeping.')
    
threads = []
for _ in range(10):
    t = threading.Thread(target=do_something,args=[1.5])
    t.start()
    threads.append(t)
    
for thread in threads:
    thread.join()

finish = time.perf_counter()

print(f'Finished in {finish-start} second(s).')
```

- join() 方法的功能是在程序指定位置，优先让该方法的调用者使用 CPU 资源。

- join不能与start在循环里连用（原文链接：https://blog.csdn.net/brucewong0516/article/details/81050792）：

  ```python
  # 错误示例代码🙅
  threads = [Thread() for i in range(5)]
  for thread in threads:
      thread.start()
      thread.join()
  ```

  

  1. 第一次循环中,主线程通过start函数激活线程1,线程1进行计算 
  1. 由于start函数不阻塞主线程,在线程1进行运算的同时,主线程向下执行join函数 
  1. 执行join之后,主线程被线程1阻塞,在线程1返回结果之前,主线程无法执行下一轮循环 
  1. 线程1计算完成之后,解除对主线程的阻塞 
  1. 主线程进入下一轮循环,激活线程2并被其阻塞 

​	如此往复,可以看出,本来应该并发的五个线程,在这里变成了顺序队列,效率和单线程无异。



#### concurrent.futures

Python中进行并发编程一般使用threading和multiprocessing模块，不过大部分的并发编程任务都是派生一系列线程，从队列中收集资源，然后用队列收集结果。在这些任务中，往往需要生成线程池，concurrent.futures模块对threading和multiprocessing模块进行了进一步的包装，可以很方便地实现池的功能。

此模块由以下部分组成，[参考链接](https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter4/02_Using_the_concurrent.futures_Python_modules.html)：

- `concurrent.futures.Executor`: 这是一个虚拟基类，提供了异步执行的方法。
- `submit(function, argument)`: 调度函数（可调用的对象）的执行，将 `argument` 作为参数传入。
- `map(function, argument)`: 将 `argument` 作为参数执行函数，以 **异步** 的方式。
- `shutdown(Wait=True)`: 发出让执行者释放所有资源的信号。
- `concurrent.futures.Future`: 其中包括函数的异步执行。Future对象是submit任务（即带有参数的functions）到executor的实例。

```python
import concurrent.futures
import time

start = time.perf_counter()

def do_something(second):
    print('Start Sleeping')
    time.sleep(second)
    return f'Done Sleeping {second}s.'
    
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
future = executor.submit(do_something,1.2)

finish = time.perf_counter()
print(f'Finished in {finish - start} second(s).')
```

##### map

submit()方法只能进行单个任务，用并发多个任务，需要使用map与as_completed。map方法接收两个参数，第一个为要执行的函数，第二个为一个序列，会对序列中的每个元素都执行这个函数，返回值为执行结果组成的生成器，返回结果与序列结果的顺序是一致的。

```python
import concurrent.futures
import time

start = time.perf_counter()

def do_something(second):
    print('Start Sleeping')
    time.sleep(second)
    return f'Done Sleeping {second}s.'
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    futures = executor.map(do_something, secs)
    for future in futures:
        print(future)

finish = time.perf_counter()
print(f'Finished in {finish - start} second(s).')
```

##### as_completed

as_completed()方法返回一个Future组成的生成器，在没有任务完成的时候，会阻塞，在有某个任务完成的时候，会yield这个任务，直到所有的任务结束。

```python
import concurrent.futures
import time

start = time.perf_counter()

def do_something(second):
    print('Start Sleeping')
    time.sleep(second)
    return f'Done Sleeping {second}s.'
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5,4,3,2,1]
    futures = [executor.submit(do_something,sec) for sec in secs]
    for f in concurrent.futures.as_completed(futures):
        print(f.future())

finish = time.perf_counter()
print(f'Finished in {finish - start} second(s).')
```

##### wait

wait方法可以让主线程阻塞，直到满足设定的要求。有三种条件ALL_COMPLETED, FIRST_COMPLETED，FIRST_EXCEPTION。

```python
import concurrent.futures
import time

start = time.perf_counter()

def do_something(second):
    print('Start Sleeping')
    time.sleep(second)
    return f'Done Sleeping {second}s.'
    
with concurrent.futures.ThreadPoolExecutor() as executor:
    secs = [5,4,3,2,1]
    futures = [executor.submit(do_something,sec) for sec in secs]
    concurrent.futures.wait(futures, return_when=concurrent.futures.ALL_COMPLETED)
    print('All done.')

finish = time.perf_counter()
print(f'Finished in {finish - start} second(s).')
```



### 多进程

#### concurrent.futures

使用ProcessPoolExecutor与ThreadPoolExecutor方法基本一致，注意文档中有一句：

The `__main__` module must be importable by worker subprocesses. This means that [`ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ProcessPoolExecutor) will not work in the interactive interpreter.

我的理解是：函数执行部分必须写在`if __name__ == '__main__':`后面

下面写一个计算密集型程序（for循环求和）：

```python
import concurrent.futures
import time

def do_something(num):
    a = 0
    for _ in range(num):
        a += 1
    return a

if __name__ == '__main__':
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
      nums = [10000000,20000000,30000000,40000000,50000000,]
      futures = [executor.submit(do_something,num) for num in nums]
      for f in concurrent.futures.as_completed(futures):
          print(f.future())

    finish = time.perf_counter()
    print(f'Finished in {finish - start} second(s). ThreadPoolExecutor method.')

    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        nums = [10000000, 20000000, 30000000, 40000000, 50000000, ]
        futures = [executor.submit(do_something, num) for num in nums]
        for f in concurrent.futures.as_completed(futures):
            print(f.future())

    finish = time.perf_counter()
    print(f'Finished in {finish - start} second(s). ProcessPoolExecutor method.')
```

运行结果如下，可见多进程速度快很多：

```shell
➜  pyphot py3 test_thread.py
10000000
20000000
30000000
40000000
50000000
Finished in 8.21158159 second(s). ThreadPoolExecutor method.
10000000
20000000
30000000
40000000
50000000
Finished in 3.697161315999999 second(s). ProcessPoolExecutor method.
```

