import os
import smail
import time


process="/Users/zhoubo/Desktop/wechat-bot/wx.lock"
os.system("ps -ef|grep bot.py|grep -v grep >%s" % process)
if not(os.path.getsize(process)):
    os.system("python /Users/zhoubo/Desktop/wechat-bot/wx.py &")