#coding=utf-8

from wxpy import *
import schedule
import time
from command import Command

bot_alex = Bot(cache_path=True)
command = Command()

group_name = 'iOS group'
group = ensure_one(bot_alex.groups().search(group_name))
group.update_group(True)

friend_keeplive = ensure_one(bot_alex.friends().search('bot'))

def job():
    print('do job')
    friend_keeplive.send('i am alive')

schedule.every(15).to(25).seconds.do(job)

@bot_alex.register(group, TEXT)
def just_print(msg):
    # 打印消息
    print(msg)
    return resolve_command(msg.text, msg.member)

def resolve_command(text, sender):
    """解析当前的 message 中的 command

    Arguments:
        text {string} -- 当前收到的消息内容
        sender {string} -- 当前消息的发送者
    Returns:
        [string, None] -- 当解析成功的时候返回 string 否者返回 none
    """
    print('parpre to solove text = %s, sender = %s' % (text, sender.name))
    if command.vaild(text):
        result = command.analysis(text, sender.name)
        print('result = %s' % result)
        return result
    else:
        return None#"not found~ reply: %s" % text

# embed()

while True:
    schedule.run_pending()
    time.sleep(1)