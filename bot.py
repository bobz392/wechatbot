#! /usr/bin/env python2.7
# coding=utf-8

import schedule
import time
import os
import datetime
import random
import signal
import chat

from wxpy import *
from kr36 import Kr
from command import Command
from wxpy import Tuling
# from check_in import CheckIn
from notify_work import notify_work_instance


class AlexBot(object):
    """
    机器人的主要逻辑
    """

    def __init__(self):
        self.bot = Bot(cache_path=True)
        self.bot.enable_puid()
        self.command = Command()

        print(self.bot.groups())

        # group_name = 'notify_group'
        # group_name = 'new_notify'
        # group_name = u'不是那个沃尔玛'
        # group_name = 'test'
        group_name = u'开挂的IT'
        self.group = ensure_one(self.bot.groups().search(group_name))
        self.group.update_group(True)
        # self.checkin = CheckIn()
        self.tuling = Tuling('02518a2c4b004145bdea82ae0440d715')
        self.tengxun = chat.TencentChat()
        # self.xiaobing = ensure_one(self.bot.mps().search(u'小冰'))
        self.friend_keeplive = \
            ensure_one(self.bot.friends().search(u'阿力木'))
        self.admin = ensure_one(self.bot.friends().search(u'M_zhou'))

        # group_ml_name = u'ML集训营1期VIP-NLP-周博'
        # self.group_ml = ensure_one(self.bot.groups().search(group_ml_name))

    def keep_alive(self):
        self.friend_keeplive.send('i am alive')

    # def hour_notify(self):
    #     from datetime import datetime
    #     today = datetime.today()
    #     week_day = today.weekday()
    #     if week_day != 6 and week_day != 5:
    #         self.group.send(u'吃了吗，日报写了吗，喝水了吗，如厕了吗。%s:00 点啦。' %
    #                         datetime.now().strftime("%H"))
    #     if today.hour >= 18:
    #         file_path = os.getcwd() + '/beauty/'
    #         self.group.send_image(file_path + 'work.png')

    # def notify_iOS_checkin(self):
    #     print('检查 iOS 打卡信息！！！！！')
    #     msg = self.checkin.check_all_user('1')
    #     if msg:
    #         self.group.send(msg)

    def load_kr_data(self):
        kr = Kr()
        msg = kr.loadData()
        if msg:
            self.group.send(msg)

    def write_image2file(self, data, sender_name):
        file_path = os.getcwd() + '/beauty/'
        p = random.randint(0, 100)
        if p < 5:
            return file_path + 'problem.jpg'

        file_name = file_path + datetime.datetime.now().strftime("%Y-%m-%d-%H-%m-%s.png")
        if os.path.exists(file_path) is False:
            os.makedirs(file_path)
        f = open(file_name, 'ab')
        f.write(data)
        f.close()
        return file_name
        # from random import randint
        # return file_path + ('%d.jpg' % randint(1, 4))

    def schedule_of_weekdays(self):
        for check_time in ['10:00', '11:00', '12:00', '14:00', '15:00', '16:00',
                           '17:00', '18:00', '19:00', '20:00']:
            # schedule.every().days.at(check_time).do(self.hour_notify)
            if check_time == '10:00' or check_time == '14:00' or check_time == '16:00' or check_time == '19:00':
                schedule.every().days.at(check_time).do(self.load_kr_data)

    def resolve_command(self, text, sender, allow_group=None):
        """解析当前的 message 中的 command

        Arguments:
            text {string} -- 当前收到的消息内容
            sender {string} -- 当前消息的发送者
            allow_group {int} -- 当前消息允许访问的分组 id， None 代表全部人都可以访问
        Returns:
            [string, None] -- 当解析成功的时候返回 string 否者返回 none
        """
        if sender.name == u'M_zhou' and text == u'-36kr':
            return self.load_kr_data()
        if text == u'-user/boy':
            print(text, sender.name)
            file_path = os.getcwd() + '/beauty/'
            if sender.name == u'M_zhou':
                print(self.group.send_image(file_path + 'boy1.png'))
            else:
                print(self.group.send_image(file_path + 'boy2.png'))

            print('load boy finish')
            return None

        print('parpre to solove text = %s, sender = %s' % (text, sender.name))
        if self.command.vaild(text):
            result = self.command.analysis(text, sender.name, allow_group)
            if isinstance(result, unicode):
                print('solove %s result = %s' % (text, result))
                return result
            elif isinstance(result, tuple):
                print('result_type = %s' % type(result))
                if result[0] == 'file':
                    # if sender.name == u'M_zhou' or sender.name == u'园园':
                    self.group.send_file(result[1])
                    # else:
                    #     return u'现在流量有限抱歉了，只有园园老师来操作'

            else:
                print('result type = %s' % type(result))
                file_name = self.write_image2file(result, sender.name)
                print(file_name)
                print(self.group.send_image(file_name))

        return None


if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)

        alex_bot = AlexBot()
        notify_work_instance.set_group(alex_bot.group)

        schedule.every(5).to(10).minutes.do(alex_bot.keep_alive)
        # alex_bot.schedule_of_weekdays()
        # schedule.every().days.at('9:40').do(alex_bot.load_kr_data)

        @alex_bot.bot.register(alex_bot.admin, TEXT)
        def transfer(msg):
            if msg.text.startswith(u'-t'):
                transfer_msg = msg.text.replace(u'-t', u'')
                alex_bot.group.send(transfer_msg)

        # @alex_bot.bot.register(alex_bot.group_ml, TEXT)
        # def transfer(msg):
        #     alex_bot.admin.send(msg)

        # @alex_bot.bot.register(alex_bot.xiaobing, [TEXT, PICTURE])
        # def transfer_xiaobing(msg):
        #     print('recive xiaobing reply' + msg.text)
        #     alex_bot.group.send(msg)

        @alex_bot.bot.register(alex_bot.group, TEXT)
        def iOS_router(msg):
            # 打印消息
            # print("puid = %s" % msg.member.puid)  # puid
            # prosbolity = random.randint(0, 100)
            if msg.is_at:  # or prosbolity < 10:
                remove_at_msg = msg.text.replace(u'@ALEX ', u'')
                # if Command.use_chat_type == 0:
                print('send to bot %s ,%d' %
                      (remove_at_msg, Command.use_chat_type))
                #     alex_bot.xiaobing.send(remove_at_msg)
                # el
                if Command.use_chat_type == 1:
                    alex_bot.tuling.do_reply(msg)
                elif Command.use_chat_type == 2:
                    tx_reply = alex_bot.tengxun.request(remove_at_msg)
                    alex_bot.group.send(tx_reply)
            else:
                return alex_bot.resolve_command(msg.text, msg.member, '1')

        # @alex_bot.bot.register(alex_bot.friend_keeplive)
        # def reply_my_friend(msg):
        #     print(msg)
        #     if msg.is_at:
        #         alex_bot.tuling.do_reply(msg)

        # alex_bot.group.send('我是小赖同学，您的霸霸，为您服务')
        while True:
            schedule.run_pending()
            time.sleep(1)

    except Exception, exc:
        print exc
