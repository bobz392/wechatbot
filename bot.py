#coding=utf-8

from wxpy import *
import schedule
import time
from command import Command
from check_in import CheckIn

bot_alex = Bot(cache_path=True)
command = Command()

group_name = 'iOS group'
group = ensure_one(bot_alex.groups().search(group_name))
# group.update_group(True)

friend_keeplive = ensure_one(bot_alex.friends().search('bot'))

def job():
    print('do job')
    friend_keeplive.send('i am alive')

check_in = CheckIn()

def notify_check_innotify_check_in():
    msg = check_in.check_all_user()
    group.send(msg) 


def schedule_of_weekdays(*days):
    for day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']:
        check_in_job = schedule.every()
        for check_time in ['19:15', '19:30', '19:45', \
                '20:00', '20:30', '20:45', '21:00', '21:30']:
            getattr(check_in_job, day).at(check_time).do()    
      

schedule.every(15).to(25).minutes.do(job)


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
