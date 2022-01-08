## 下载网页文件

```bash
wget -r -nd -np --accept=Auto*BIN1*.fts https://nadc.china-vo.org/psp/next/2021/20210913/AutoFlat20210913/
```

## 从源码安装软件

https://unix.stackexchange.com/questions/173/how-to-compile-and-install-programs-from-source

```bash
./configure && make && sudo make install
```

[where to install?](https://unix.stackexchange.com/questions/30/where-should-i-put-software-i-compile-myself)

## find命令

find   path   -option   [   -print ]   [ -exec   -ok   command ]   {} \;

find 根据下列规则判断 path 和 expression，在命令列上第一个 - ( ) , ! 之前的部份为 path，之后的是 expression。如果 path 是空字串则使用目前路径，如果 expression 是空字串则使用 -print 为预设 expression。

expression 中可使用的选项有二三十个之多，在此只介绍最常用的部份。

-mount, -xdev : 只检查和指定目录在同一个文件系统下的文件，避免列出其它文件系统中的文件

-amin n : 在过去 n 分钟内被读取过

-anewer file : 比文件 file 更晚被读取过的文件

-atime n : 在过去n天内被读取过的文件

-cmin n : 在过去 n 分钟内被修改过

-cnewer file :比文件 file 更新的文件

-ctime n : 在过去n天内被修改过的文件

-empty : 空的文件-gid n or -group name : gid 是 n 或是 group 名称是 name

-ipath p, -path p : 路径名称符合 p 的文件，ipath 会忽略大小写

-name name, -iname name : 文件名称符合 name 的文件。iname 会忽略大小写

-size n : 文件大小 是 n 单位，b 代表 512 位元组的区块，c 表示字元数，k 表示 kilo bytes，w 是二个位元组。

-type c : 文件类型是 c 的文件。

    d: 目录

    c: 字型装置文件

    b: 区块装置文件

    p: 具名贮列

    f: 一般文件

    l: 符号连结

```sh
# 将当前目录及其子目录下所有文件后缀为 .c 的文件列出来:
find . -name "*.c"

# 将当前目录及其子目录中的所有文件列出：
find . -type f

# 将当前目录及其子目录下所有最近 20 天内更新过的文件列出:
find . -ctime -20

# 查找 /var/log 目录中更改时间在 7 日以前的普通文件，并在删除之前询问它们：
find /var/log -type f -mtime +7 -ok rm {} \;

# 查找当前目录中文件属主具有读、写权限，并且文件所属组的用户和其他用户具有读权限的文件：
find . -type f -perm 644 -exec ls -l {} \;

# 查找系统中所有文件长度为 0 的普通文件，并列出它们的完整路径：
find / -type f -size 0 -exec ls -l {} \;

```

## 调节显示屏幕的亮度

```sh
# 查看连接的显示设备:
>>> xrandr | grep  "connected"
eDP-1-1 connected primary 1920x1080+0+0 (normal left inverted right x axis y axis) 344mm x 194mm
DP-1-1 disconnected (normal left inverted right x axis y axis)
DP-1-2 disconnected (normal left inverted right x axis y axis)
DP-1-3 connected 1920x1080+1920+0 (normal left inverted right x axis y axis) 509mm x 286mm
# 选中设备, 调节亮度
>>> xrandr --output DP-1-3 --brightness 0.5
```

## 从下往上显示文件内容

`tac file.txt`

## 显示从文件的第10行到最后一行的内容

`sed -n '10, $p' file.txt`

## 判断变量为空

https://www.jb51.net/article/154835.htm

```sh
#!/bin/sh
para1=
if [ ! $para1 ]; then
  echo "IS NULL"
else
  echo "NOT NULL"
fi
```

## 查看哪些端口开放以及某端口服务情况

https://blog.csdn.net/q1054261752/article/details/90736040

```
sudo aptitude install nmap
nmap 127.0.0.1

lsof -i:8181
```