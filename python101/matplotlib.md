### 如何设置坐标轴刻度

```python
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

fig2 = plt.figure(figsize=(15,10))
plt.plot(freqs, ps)
plt.xlabel('frequency(circle/second)', fontsize=18)
plt.title('Power spectrum (np.fft.fft)', fontsize=20)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(1)
## 把y轴的刻度间隔设置为10，并存在变量里
y_major_locator=MultipleLocator(10)
#ax为两条坐标轴的实例
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
## 把y轴的主刻度设置为10的倍数
ax.yaxis.set_major_locator(y_major_locator)
plt.xlim(-31,31)
plt.show()

## 原参考:https://www.jb51.net/article/163842.htm
x_values=list(range(11))
y_values=[x**2 for x in x_values]
plt.plot(x_values,y_values,c='green')
plt.title('Squares',fontsize=24)
plt.tick_params(axis='both',which='major',labelsize=14)
plt.xlabel('Numbers',fontsize=14)
plt.ylabel('Squares',fontsize=14)
x_major_locator=MultipleLocator(1)
#把x轴的刻度间隔设置为1，并存在变量里
y_major_locator=MultipleLocator(10)
#把y轴的刻度间隔设置为10，并存在变量里
ax=plt.gca()
#ax为两条坐标轴的实例
ax.xaxis.set_major_locator(x_major_locator)
#把x轴的主刻度设置为1的倍数
ax.yaxis.set_major_locator(y_major_locator)
#把y轴的主刻度设置为10的倍数
plt.xlim(-0.5,11)
#把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
plt.ylim(-5,110)
#把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
plt.show()

```

### 常用fontsize

```python
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rc('xtick', labelsize=15) 
matplotlib.rc('ytick', labelsize=15) 

fig2 = plt.figure(figsize=(15,7))
ax1 = fig2.add_subplot(121)
ax1.hist(d_sample[201:], bins=50)
ax1.set_xlabel(r'$d(pc)$', fontsize=18)
ax1.set_ylabel(r'$counts$', fontsize=18)
ax1.set_title(r'$distance\ distribution\ from\ sampling$', fontsize=20)

ax2 = fig2.add_subplot(122)
d = np.arange(1000, 2500, 1)
ax2.plot(d, func_fd(d), linewidth=3)
ax2.set_xlabel(r'$d(pc)$', fontsize=18)
ax2.set_ylabel(r'$P(d)$', fontsize=18)
ax2.set_title(r'$theoretical\ PDF\ of\ distance$', fontsize=20)
fig2.savefig('distance_distribution.png',bbox_inches='tight', dpi=300)

# or

fig = plt.figure(figsize=(21,7))
ax1 = fig.add_subplot(131)
ax1.hist(uni_sample[-1], bins=15, label=r'$min=0,\ max=12$')
ax1.set_xlabel(r'$x$', fontsize=12)
ax1.set_ylabel(r'$counts$', fontsize=12)
ax1.set_title(r'$uniform$', fontsize=15)
ax1.legend(prop = {'size':10})

ax2 = fig.add_subplot(132)
ax2.hist(pos_sample[-1], bins=15, label=r'$\lambda=10$')
ax2.set_xlabel(r'$x$', fontsize=12)
ax2.set_ylabel(r'$counts$', fontsize=12)
ax2.set_title(r'$poisson$', fontsize=15)
ax2.legend(prop = {'size':10})

ax3 = fig.add_subplot(133)
ax3.hist(exp_sample[-1], bins=15, label=r'$\theta=3$')
ax3.set_xlabel(r'$x$', fontsize=12)
ax3.set_ylabel(r'$counts$', fontsize=12)
ax3.set_title(r'$exponential$', fontsize=15)
ax3.legend(prop = {'size':10})

# or 

fig3 = plt.figure(figsize=(12,12))
plt.bar(x, res.cumcount/res.cumcount.max(), width=res.binsize, label=r'sampling')
plt.plot(d, cdf, linewidth=2, color='r', label=r'theory')
plt.xlabel(r'$d(pc)$', fontsize=18)
plt.ylabel(r'$cdf$', fontsize=18)
plt.legend(fontsize=18)
plt.title(r'$cumulative\ distribution\ of\ distance$', fontsize=20)
fig3.savefig('cdf.png',bbox_inches='tight', dpi=300)
```

### errorbars

```python
figure=plt.figure(figsize=(15,7))
ax1=figure.add_subplot(121)
ax1.errorbar(x,y,yerr=yer,ecolor='blue',marker='.',mfc='blue',linestyle='none',label='target') # ls='none'指取消默认的连线
```