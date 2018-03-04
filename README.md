# pixiv2.0.1
```shell
BBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBB              BBBBBB
BBBBB    BBBBBBBBBBB    BBBB
BBB     BBBBBBBBBBBBBB   BBB
B   B#  BBBBBBBBBBBBBBB   BB
B  BB#  BBBBBBBBBBBBBBB    B
BB#BB#  BBBBBBBBBBBBBBB#   B
BBBBB#  BBBBBBBBBBBBBBB-   B
BBBBB#  BBBBBBBBBBBBBBB    B
BBBBB#  BBBBBBBBBBBBBB    BB
BBBBB#  BBBBBBBBBBBBB    BBB
BBBBB#    BBBBBBBBB    BBBBB
BBBBB#  BB          BBBBBBBB
BBBBB#  BBBBBBBBBBBBBBBBBBBB
BBBBB#  BBBBBBBBBBBBBBBBBBBB
BBBB      BBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBB

pixiv.py -m <mod> -i <inform>
         -r <r18>    enable r18 (only for daily and weekly)
         -t <thread> enable threads
         -d <detail> enable detail message
mod:
login    login to pixiv     -i <pid>        -p <password>
ranking  ranking download   -i <date>       -s <style> (default:daily ,weekly, monthly, rookies, original, male, female)
highlike keyword download   -i <keyword>    -l <leastlike>
database database download  -i <keyword>    -l <leastlike> (need builded database)
painter  painter download   -i <painterid>
bookmark bookmark download  -i <painterid>
```
当然啦，r18还是需要你的帐号是支持的······
当前支持Win&Linux。

login模式只需要一次登录就会生成cookies，之后自动读取cookies进行爬取。
如果爬取时，出现http报错，可以尝试重新login。

脚本无法识别登陆成功与否，请在无法爬取时，确认你login的是正确的账号密码。

感谢@exa160 的Pull

> 这里是做出的修复：
- getids代码正则匹配修复，不再一个id重复两次，降低被反风险 ...
- 修复 -r指令错误
- 优化算法，断开连接尝试重连一次，第一次断开连接不会直接退出执行（那个GUI版本闪退就是因为被反或者网不好）
- 修复ceiling宏定义无效
- 增加daily以外的ranking榜排名方式，并将daily改为ranking，-r仅支持daily和weekly
- 微小的逻辑优化

---
2018年3月4日：

重新测试之后，发现单线程抓取已失效，但多线程依然可以正常运行。**建议所有爬取操作都加入`-t`参数。**highlike功能因为pixiv的搜索貌似采用了新的机制，无法获取到搜索结果，导致了该功能失效。

近期不大可能有功夫去修复（主要是快毕业了），以后做（tan90°的）pixiv爬虫ver.3的时候会全部修复？