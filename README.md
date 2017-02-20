# pixiv2.0
```shell
pixiv.py -m <mod> -i <inform>
         -r <r18>    enable r18(disable for daily mod)
         -t <thread> enable threads
mod:
login    login to pixiv     -i:pid        -p <password>
daily    daily download     -i:date
highlike keyword download   -i:keyword    -l <leastlike>
database database download  -i:keyword    -l <leastlike> (need builded database)
painter  painter download   -i:painterid
bookmark bookmark download  -i:painterid
```
当然啦，r18还是需要你的帐号是支持的······
当前支持Win&Linux。

login模式只需要一次登录就会生成cookies，之后自动读取cookies进行爬取。
如果爬取时，出现http报错，可以尝试重新login。
