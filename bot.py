#! /usr/bin/env python2.7
#coding=utf-8

from wxpy import *
import schedule
import time
from kr36 import Kr
from command import Command
from check_in import CheckIn

class AlexBot(object):
    """
    机器人的主要逻辑
    """

    def __init__(self):
        self.bot = Bot(cache_path=True)
        self.bot.enable_puid()
        self.command = Command()

        group_name = 'iOS group'
        self.group = ensure_one(self.bot.groups().search(group_name))
        self.group.update_group(True)
        self.checkin = CheckIn()

        self.friend_keeplive = \
            ensure_one(self.bot.friends().search('keep-alive-bot'))

    def keep_alive(self):
        self.friend_keeplive.send('i am alive')

    def notify_weekday_checkin(self):
        print('检查打卡信息！！！！！')
        msg = self.checkin.check_all_user()
        if msg:
            self.group.send(msg)

    def load_kr_data(self):
        kr = Kr()
        msg = kr.loadData()
        if msg:
            self.group.send(msg)

    def schedule_of_weekdays(self):
        for check_time in ['10:00', '10:15', '10:30', '19:00', '19:15', '19:30', '19:45', \
                    '20:00', '20:30', '20:45', '21:00', '21:30']:
            schedule.every().days.at(check_time).do(self.notify_weekday_checkin)

    def resolve_command(self, text, sender):
        """解析当前的 message 中的 command

        Arguments:
            text {string} -- 当前收到的消息内容
            sender {string} -- 当前消息的发送者
        Returns:
            [string, None] -- 当解析成功的时候返回 string 否者返回 none
        """
        print('parpre to solove text = %s, sender = %s' % (text, sender.name))
        if self.command.vaild(text):
            result = self.command.analysis(text, sender.name)
            print('solove %s result = %s' % (text, result))
            return result

        return None#"not found~ reply: %s" % text


if __name__ == "__main__":
    alex_bot = AlexBot()
    schedule.every(15).to(25).minutes.do(alex_bot.keep_alive)
    alex_bot.schedule_of_weekdays()
    schedule.every().days.at('9:40').do(alex_bot.load_kr_data)

    @alex_bot.bot.register(alex_bot.group, TEXT)
    def router(msg):
        # 打印消息
        print("puid = %s" % msg.member.puid)  #puid
        return alex_bot.resolve_command(msg.text, msg.member)

    # embed()

    while True:
        schedule.run_pending()
        time.sleep(1)
