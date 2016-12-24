# pixiv2.0
```
pixiv.py -m <mod> -i <inform>
         -r <r18>    enable r18(disable for daily mod)
         -t <thread> enable threads
mod:
login    login to pixiv     -i:pid        -p <password>
daily    daily download     -i:date
highlike keyword download   -i:keyword    -l <leastlike> 
painter  painter download   -i:painterid
bookmark bookmark download  -i:painterid
```
当然啦，r18还是需要你的帐号是支持的······
当前仅支持Win，Linux未适配。

login模式只需要一次登录就会生成cookies，之后自动读取cookies进行爬取。
如果爬取时，出现http报错，可以尝试重新login。