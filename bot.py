#! /usr/bin/env python2.7
#coding=utf-8

from wxpy import *
import schedule
import time, signal
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
        print(self.bot.groups())
        # group_name = 'iOS group'
        group_name = 'notify_group'
        self.group = ensure_one(self.bot.groups().search(group_name))
        # self.group.update_group(True)
        self.checkin = CheckIn()

        # checkin_group_name = 'checkin notify'
        # try:
        #     self.checkin_group = ensure_one(self.bot.groups().search(checkin_group_name))
        # except ValueError:
        #     self.checkin_group = None

        self.friend_keeplive = \
            ensure_one(self.bot.friends().search(u'阿力木'))

    def keep_alive(self):
        self.friend_keeplive.send('i am alive')
    
    import datetime
    def hour_notify(self):
        self.group.send(u'吃了吗，日报写了吗，喝水了吗，如厕了吗。%s:00 点啦。' % datetime.datetime.now().strftime("%H"))

    def notify_iOS_checkin(self):
        print('检查 iOS 打卡信息！！！！！')
        msg = self.checkin.check_all_user('1')
        if msg:
            self.group.send(msg)

    # def notify_checkgroup_checkin(self):
    #     print('检查打卡组打卡信息！！！！！')
    #     msg = self.checkin.check_all_user('2')
    #     if msg:
    #         self.checkin_group.send(msg)

    def load_kr_data(self):
        kr = Kr()
        msg = kr.loadData()
        if msg:
            self.group.send(msg)
            # print(ms)
            # time.sleep(5)
            # self.checkin_group.send(msg)

    def write_image2file(self, data):
        import os
        import datetime
        
        file_path = os.getcwd() + '/beauty/'
        file_name = file_path + datetime.datetime.now().strftime("%Y-%m-%d-%H-%m-%s.png")
        if os.path.exists(file_path) is False:
            os.makedirs(file_path)
        f = open(file_name, 'ab')
        f.write(data)
        f.close()
        return file_name

    def schedule_of_weekdays(self):
        # for check_time in ['10:00', '10:15', '10:30', '19:00', '19:15', '19:30', '19:45', \
        #             '20:00', '20:30', '20:45', '21:00', '21:30']:
        for check_time in ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', \
            '17:00', '18:00', '19:00', '20:00', '21:00']:
            schedule.every().days.at(check_time).do(self.hour_notify)
            if check_time == '10:00' or check_time == '14:00' or check_time == '16:00':
                schedule.every().days.at(check_time).do(self.load_kr_data)
            # schedule.every().days.at(check_time).do(self.notify_iOS_checkin)
            # time.sleep(5)
            # schedule.every().days.at(check_time).do(self.notify_checkgroup_checkin)

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
                print('result type = %s' % type(result))
                file_name = self.write_image2file(result)
                # if allow_group == 1:
                self.group.send_image(file_name)
                # else:
                #     self.checkin_group.send_image(file_name)
                result = None
            return result

        return None#"not found~ reply: %s" % text

if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)

        alex_bot = AlexBot()
        schedule.every(5).to(10).minutes.do(alex_bot.keep_alive)
        alex_bot.schedule_of_weekdays()
        schedule.every().days.at('9:40').do(alex_bot.load_kr_data)

        @alex_bot.bot.register(alex_bot.group, TEXT)
        def iOS_router(msg):
            # 打印消息
            print("puid = %s" % msg.member.puid)  #puid
            return alex_bot.resolve_command(msg.text, msg.member, '1')

        # @alex_bot.bot.register(alex_bot.checkin_group, TEXT)
        # def check_in_router(msg):
        #     print("checkin group puid = %s" % msg.member.puid)#puid
        #     return alex_bot.resolve_command(msg.text, msg.member, '2')

        # embed()
        alex_bot.load_kr_data()

        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception, exc:
        print exc