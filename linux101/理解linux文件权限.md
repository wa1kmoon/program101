# 理解Linux文件权限

## 1 用户账户相关

### 1.1 /etc/passwd文件

- 每创建一个用户,系统会分配一个唯一的UID（User ID）给这个用户
- Linux系统使用/etc/passwd文件将用户的登录名匹配到对应的UID
    - 可以使用cat命令查看此文件的内容
        ```sh
        $ cat /etc/passwd
        root:x:0:0:root:/root:/bin/bash
        bin:x:2:2:bin:/bin:/usr/sbin/nologin
        xlew:x:1000:1000:xlew,,,:/home/xlew:/bin/bash
        #用户登录名:密码:UID:组ID:文本描述:HOME位置:用户默认shell
        ```
    - UID小于500的用户账户为系统为各种功能创建的用户账户，并非真的用户。这些称为系统账户
    - 真正的用户的UID大于500
    - passwd文件中的密码部分用x代替，真正的密码在/etc/shadow文件下

### 1.2 /etc/shadow文件

- shadow文件为每个用户账户都保存了一条记录：
    ```sh
    $ sudo cat /etc/shadow
    xlew:$6$GrHPYxq4$gZO/xxmOVZDWt9oENRmlWPOpqasiDBsuMVeJC6eHre0IYVTvIT40SQLEewP5o16Uokp48FuV2sFDpq0iovklD1:18083:0:99999:7:::
    ```
    - 每条记录有9个字段：
      - 登录名
      - 加密后的密码
      - 自上次修改密码后过去的天数（从1970.01.01开始算起）
      - 多少天后才能修改密码
      - 多少点后必须修改密码
      - 密码过期前提前多少天提醒用户修改密码
      - 密码过期后多少天禁用用户账户
      - 用户账户被禁用的日期
      - 预留字段

### 1.3 添加新用户

- useradd命令
  - -c comment  `给新用户添加备注`
  - -g initial_group `指定用户登录组的GID或组名`
  - -m loginname `创建用户的HOME目录`
  - -p passwd `为用户账户指定默认密码`
 ```sh
 $ sudo useradd -c 'same group with xlew' -g 1000 -m xlewtest -p xltest -d /home/xlewtest
 # 这里添加了用户登录名为xlewtest，备注为same group with xlew.，但在登录界面显示的是备注信息。
 ```
  
### 1.4 修改用户

- usermod命令
  - -l `修改用户账户的登录名`
  - -L `锁定账户，使用户无法登录`
  - -p `修改用户的密码`
  - -U `解除锁定，使用户能够登录`

- passwd命令 `改变用户密码`
- chpasswd命令 `适用于大量修改密码`
    ```sh
    $ chpasswd < users.txt
    # users.txt为含有userid:passwd对的文件
    ```

- chfn命令 `修改用户账户的备注信息`
  - 可使用finger命令查看用户账户信息
    ```sh
    $ finger xlew
    Login: xlew                             Name: xlew
    Directory: /home/xlew                   Shell: /bin/bash
    On since Mon Jan 27 09:41 (CST) on :0 from :0 (messages off)
    No mail.
    No Plan.
    ```
  - 如需使用chfn修改指定项目备注信息,可以指定参数
    ```sh
    $ chfn --help
    用法：chfn [选项] [登录]

    选项：
    -f, --full-name FULL_NAME     更改用户的全名
    -h, --home-phone HOME_PHONE   更改用户的家庭电话号码
    -o, --other OTHER_INFO        更改用户的其它 GECOS 信息
    -r, --room ROOM_NUMBER        更改用户的房间号
    -R, --root CHROOT_DIR         chroot 到的目录
    -u, --help                    显示此帮助信息并推出
    -w, --work-phone WORK_PHONE   更改用户的办公室电话号码
        --extrausers              Use the extra users database
    $ sudo chfn xlew -f 'first user'
    $ cat /etc/passwd|grep first
    xlew:x:1000:1000:first user,,,:/home/xlew:/bin/bash
    ```

- chsh命令 `修改用户账户的默认登录shell`
    ```sh
    $ cat /etc/passwd|grep xlewtest
    xlewtest:x:1001:1000:same group with xlew.,,,:/home/xlewtest:/bin/sh
    $ sudo chsh xlewtest -s /bin/bash
    $ cat /etc/passwd|grep xlewtest
    xlewtest:x:1001:1000:same group with xlew.,,,:/home/xlewtest:/bin/bash
    ```

## 2 使用linux组

“用户账户在控制单个用户安全性方面很好用，但涉及在**共享资源**的一组用户时就捉襟见肘了。为了解决这个问题，Linux系统采用了另外一个安全概念——组(group)。
组权限允许多个用户对系统中的对象（如文件、目录或设备等）共享一组共用的权限。
有些Linux发行版会创建一个组，把所有用户都当做这个组的成员...。有些发行版会为每个用户创建单独的一个组，这样可以更安全一些。”

### 2.1 /etc/group文件

- /etc/group文件包含系统上用到的每个组的信息
    ```sh
    $ cat /etc/group|grep xlew
    adm:x:4:syslog,xlew
    cdrom:x:24:xlew
    sudo:x:27:xlew
    dip:x:30:xlew
    plugdev:x:46:xlew
    lpadmin:x:116:xlew
    xlew:x:1000:
    sambashare:x:126:xlew
    # 组名:组密码:GID:属于该组的用户列表
    ```
    >“在列表中，有些组并没有列出用户，这并不是说这些组没有成员。当一个用户在/etc/passwd文件中指定某个组作为默认组时，用户账户不会作为该组成员再出现在/etc/group文件中。”

### 2.2 创建新组

- groupadd命令 `在系统上创建新组`
    ```sh
    $ groupadd --help
    用法：groupadd [选项] 组

    选项:
    -f, --force           如果组已经存在则成功退出
                            并且如果 GID 已经存在则取消 -g
    -g, --gid GID                 为新组使用 GID
    -h, --help                    显示此帮助信息并推出
    -K, --key KEY=VALUE           不使用 /etc/login.defs 中的默认值
    -o, --non-unique              允许创建有重复 GID 的组
    -p, --password PASSWORD       为新组使用此加密过的密码
    -r, --system                  创建一个系统账户
    -R, --root CHROOT_DIR         chroot 到的目录
        --extrausers              Use the extra users database
    $ groupadd shared -g 501
    $ cat /etc/group|grep shared
    shared:x:501:
    ```    

- 使用usermod命令将用户添加到组
    ```sh
    $ sudo useradd -m test
    $ tail /etc/group
    ...
    shared:x:501:
    test:x:1003:
    $ sudo usermod -G shared test
    $ tail /etc/group
    ...
    shared:x:501:test
    test:x:1003:
    ```

### 2.3 修改组

- groupmod命令修改组的GID（-g选项）或组名（-n选项）


## 3 文件权限

### 3.1 默认文件权限

- 使用ll命令可查看文件或目录的权限，显示权限的字符串有10位 
  - 第一位，d代表目录，-代表文件
  - 后面九位以三位为一组，分别代表属主，属组成员，其它成员所拥有的权限。
    - 第一位r代表可写，第二位w代表可读，第三位x代表可执行，若某位是-代表无此位置对应的权限
    - 由此，三位权限码共有7种可能，每一种可对应一个二进制数，进而对应一个八进制数，此八进制数即表示文件或目录的权限
    - 目录的最高权限为777，文件最高权限为666
    - 使用umask命令查看创建文件的默认权限,返回值的后三位即代表默认权限的补码。（目录以777算，文件以666算）
        ```sh
        $ umask
        0002
        # 表示创建的目录默认权限为775,创建的文件默认权限为664
        ```
    - 也可使用umask命令修改默认权限值，例如：
        ```sh
        $ umask 026
        ```
### 3.2 改变安全性设置

- 使用chmod命令改变文件或目录的权限，chmod命令有两种模式可以更改权限：
    - 八进制模式，格式为 chmod mode file
        ```sh
        $ chmod 760 newfile
        # 这样newfile文件就有了760的权限了
        ```
    - 符号模式，格式为 chmod mode file
        ```sh
        $ chmod [ugoa][+-=][rwx...] file
        # u--user;g--group;o--other;a--all
        # +:添加权限;-:撤销权限;=:赋予权限
        $ chmod o=rwx file
        # 给其它成员以file文件的所有权限
        $ chmod o-x file
        # 移除其他成员对file文件拥有的可执行权限
        ```

- 使用chown命令改变文件的属主（也可以改变文件的属组）
    - 格式为：chown options owner[.group] file
    - 可用登录名或UID指定文件的新属主：
        ```sh
        $ chown xlew newfile
        # 将newfile文件的属主指定为xlew
        $ chown xlew.xlew newfile
        # 将newfile文件的属主指定为xlew，并将其属组指定为xlew
        $ chown .xlew newfile
        # 将newfile文件的属组指定为xlew
        ``` 
- 使用chgrp命令改变文件或目录的默认属组
    ```sh
    $ chgro xlew newfile
    # 将newfile的属组改为xlew
    ```