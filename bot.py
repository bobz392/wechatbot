#! /usr/bin/env python2.7
#coding=utf-8

import time, signal
from wxpy import *
import schedule

from command import Command
from config import Config

class AlexBot(object):
    """
    机器人的主要逻辑
    """
    def __init__(self):
        self.bot = Bot(cache_path=True)
        self.bot.enable_puid()
        self.command = Command()
        self.group = \
            ensure_one(self.bot.groups().search(Config.group_name))
        self.admin = \
            ensure_one(self.bot.friends().search(Config.admin))
        if Config.keep_alive_user:
            self.friend_keeplive = \
                ensure_one(self.bot.friends().search(Config.keep_alive_user))
        print(self.group, self.admin, self.friend_keeplive)

    def keep_alive(self):
        if Config.keep_alive_user:
            self.friend_keeplive.send('i am alive')

    def jenkins_check_fir(self):
        msg = self.command.jenkins_check_fir()
        if msg:
            self.group.send(msg)

    def jenkins_operation_schedule(self):
        if self.command.has_jenkins_task():
            self.group.send(u'开始打包，所有包打完之前不接受新的任务了')
            self.command.jenkins_operation()

    def schedule_of_weekdays(self):
        for check_time in Config.build_times:
            schedule.every().days.at(check_time)\
                .do(self.jenkins_operation_schedule)

    def resolve_command(self, text, sender, allow_group=None):
        """解析当前的 message 中的 command

        Arguments:
            text {string} -- 当前收到的消息内容
            sender {string} -- 当前消息的发送者
            allow_group {int} -- 当前消息允许访问的分组 id， None 代表全部人都可以访问
        Returns:
            [string, None] -- 当解析成功的时候返回 string 否者返回 none
        """
        print('parpre to solove text = %s, sender = %s' % (text, sender.name))
        if self.command.vaild(text):
            result = self.command.analysis(text, sender.name, allow_group)
            if isinstance(result, unicode):
                print('solove %s result = %s' % (text, result))
            else:
                result = None
            return result
        return None

if __name__ == '__main__':
    alex_bot = AlexBot()
    schedule.every(2).to(3).hours.do(alex_bot.keep_alive)
    schedule.every(30).to(40).minutes.do(alex_bot.jenkins_check_fir)
    alex_bot.schedule_of_weekdays()

    @alex_bot.bot.register(alex_bot.group, TEXT)
    def iOS_router(msg):
        return alex_bot.resolve_command(msg.text, msg.member, Config.group_identity)

    @alex_bot.bot.register(alex_bot.admin, TEXT)
    def transfer(msg):
        return alex_bot.resolve_command(msg.text, alex_bot.admin, '1')

    while True:
        schedule.run_pending()
        time.sleep(1)