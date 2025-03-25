# CA-Filter

本程序用来筛选微信群聊里一天内首call的合约地址（Contract Address），并将信息通过telegram bot发送至目标群聊。



## 流程工作

python方面，需要提前用pip装[wxauto](https://docs.wxauto.org/)、requests、base58：

`pip install base58 requests wxauto`



微信方面，需要你在运行的电脑上面保持登录状态，这样才能用wxauto，目前wxauto仅支持windows系统



telegram方面，需要你新建一个自己的bot以及拉进目标群聊，并获得bot token以及chat id，具体获取方式网上已经有比较多的示范了：

https://zhuanlan.zhihu.com/p/602213485
只需要做到生成bot以及token那一步即可，
chat id直接拉@getidsbot进群就可以获得


然后替换程序Catch_CA.py前面的10-12行的配置参数：

WECHAT_GROUP_NAME= "要监听的微信群名称"

TELEGRAM_BOT_TOKEN = "你刚刚生成出来的BOT TOKEN"  

TELEGRAM_CHAT_ID = "你刚刚生成出来的CHAT_ID"  



然后就可以开始运行程序了！

