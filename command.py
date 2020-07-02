# coding=utf-8

from urllib.parse import urlparse, parse_qs
from datetime import datetime
import sys
# from model import User, Message, Report
# from mail import DailyMail, WeeklyMail
# from chandao import Chandao
# from check_in import CheckIn
# from week_report import WeekReporter
from meizi import BeautyFucker
from notify_work import notify_work_instance
from conbond import conbond_data


def parse_query_2_dict(query):
    return dict((k.lower(), v if len(v) > 1 else v[0])
                for k, v in parse_qs(query).iteritems())


class Command(object):
    """命令辅助 class
    Arguments:
        object {[object]} -- [description]
    """
    use_chat_type = 1

    def __init__(self):
        """ 初始化当前可以使用的所有 commands
            [{string: [string]}}] -- [
                key 代表当前的参数
                list 代表可选的附带参数，详细见下面 helper_message 函数的返回说明
            ]
        """
        self.help_path = '-help'
        self.user_path = '-user'
        self.note_path = '-note'
        # self.sendmail_path = '-sendmail'
        # self.chandao_path = '-chandao'
        # self.checkin_path = '-checkin'
        # self.weekly_report_path = '-weekly'

        self.commands = {
            self.user_path: ['password', 'email', 'realname', 'sender-setme', 'sender-check', 'notify-delete', 'notify'],
            self.note_path: ['message', 'id', 'week'],
            # self.sendmail_path: ['empty', 'chandao'],
            self.help_path: ['-'],
            # self.chandao_path: ['-'],
            # self.checkin_path: ['-'],
            # self.weekly_report_path: ['-'],
        }

    def vaild(self, text):
        """ 当前的 command 是否是合格的格式

        Arguments:
            text {[string]} -- msg

        Returns:
            {[bool]} -- 是否是需要解析的格式
        """
        return text.startswith('-')

    def to_str(self, unicode_or_str):
        """
        通常消息中返回的是 Unicode ，这里转换 Unicode to string。
        """
        if isinstance(unicode_or_str, unicode):
            value = unicode_or_str.encode('utf-8')
        else:
            value = unicode_or_str
        return value

    def command_class(self, class_name):
        """
        获取当前 module 中指定 class name 的 class

        Arguments:
            cls {string} -- 对应的 class 的 string name

        Returns:
            {class} -- 返回对应的 class 如有的话，否则返回 None
        """
        current_module = sys.modules[__name__]
        if hasattr(current_module, class_name):
            return getattr(current_module, class_name)
        else:
            return None

    def analysis(self, message, sender, allow_group):
        """
        根据消息来分解、处理

        Arguments:
            router_text {string} -- router 的 string，通常就是一条消息
            sender {string} -- 当前的消息发送者
            allow_group {string} -- 当前的消息允许处理的 group

        Returns:
            [string] -- 返回处理后的文字
        """

        # if message == u'-perfect':
        #     if sender == '娓娓':
        #         return u'娓娓 你最棒了'
        #     else:
        #         return u'%s 你真是烦死了啊' % sender

        router_text = 'webot://%s' % self.to_str(message)
        parse = urlparse(router_text)
        command = parse.netloc.lower()
        if not self.commands.has_key(command):
            return HelpCommand()()
        message = None
        print('command = %s, path = %s, query = %s, type = %s'
              % (command, parse.path, parse.query, type(parse)))

        class_name = self.to_str(command[1:2].upper()
                                 + command[2:] + 'Command')
        command_class = self.command_class(class_name)
        command_class_object = command_class()
        # print(type(class_object))
        # print(isinstance(class_object, HelpCommand))
        # print(class_object.__dict__)
        message = command_class_object(parse, sender, allow_group)

        return message


class UserCommand(object):
    """
    用户相关的命令，不需要检查 group

    检查当前用户信息 - sunlands_webot://-user/check
    更新当前用户信息 - sunlands_webot://-user/update?password=[$password]&email=[$email]&realname=[$realname]
    切换发送者 - sunlands_webot://-user/sender-setme
    检查发送者 - sunlands_webot://-user/sender-check
    """

    @classmethod
    def helper_info(cls):
        #         当前的用户信息以及邮件发送者查询 & 更新
        # Example:
        #     -user/check（## 用户名是不可变的为当前用户的微信名，如果改名了会导致用户失效）
        #     -user/update?password=[$password]&email=[$email]&realname=[$realname]&group=[$group]&tel=[$tel] （## 更新当前用户的信息，密码为邮箱密码）
        #     -user/sender-check （## 仅仅查询）
        #     -user/sender-setme （## 更新为当前的用户发送）
        #     -user/airplane?open=[$open]  (## 飞行模式，目前功能为不会检查打卡，1 代表开启飞行模式)
        #     -user/slience?open=[$open]  (## 全员飞行模式，目前功能为不会检查打卡，1 代表开启飞行模式)
        return u'''
    -user/meizi  (## 邪恶一指尖)
    -user/notify-delete
    -user/notify?do=some-things&at=11:30
    -user/kzz?code=code&daysbefore=daysbefore&date=date
'''

    def __call__(self, router_parse, sender, allow_group):
        """ 用户相关的逻辑

        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的指令
        """
        query = router_parse.query
        path = router_parse.path

        # if path == '/check' or path == '':
        #     # return u'/check %s' % sender
        #     return User.user_exist(sender)
        # if path == '/update':
        #     # return u'/update %s' % sender
        #     update_dict = parse_query_2_dict(query)
        #     return UserCommand.update_user(update_dict, sender)
        # if path == '/sender-setme':
        #     # return u'/sender-setme %s' % sender
        #     return User.sender_set_to(sender)
        # if path == '/sender-check':
        #     # return u'/sender-check %s' % sender
        #     return User.show_sender()
        # if path == '/airplane':
        #     open_dict = parse_query_2_dict(query)
        #     is_open_text = open_dict.get('open', '0')
        #     is_open = True if is_open_text == '1' else False
        #     return User.set_user_airplane_mode(sender, is_open)
        # if path == '/slience':
        #     open_dict = parse_query_2_dict(query)
        #     is_slience_text = open_dict.get('open', '0')
        #     is_slience = True if is_slience_text == '1' else False
        #     return User.set_slience_mode(is_slience, allow_group)
        if path == '/meizi':
            bf = BeautyFucker()
            # return bf.prepare_page()
            return bf.get_b_fun_image()
        if path == '/notify-delete':
            return notify_work_instance.remove_notify(sender)
        if path == '/notify':
            open_dict = parse_query_2_dict(query)
            return notify_work_instance.notify_me_at(open_dict['at'], sender, open_dict['do'])
        if path == '/xiaobing':
            if Command.use_chat_type != 0:
                print('xiaobing')
                Command.use_chat_type = 0
                return u'我是犯病病，您的小冰'
            return None
        if path == '/tuling':
            if Command.use_chat_type != 1:
                print('tuling')
                Command.use_chat_type = 1
                return u'我似小赖同学，侬的霸霸，干哈'
            return None
        if path == '/tengxun':
            if Command.use_chat_type != 2:
                print('tengxun')
                Command.use_chat_type = 2
                return u'我似大赖同学，再冲5万你就变强'
            return None
        if path == '/kzz':
            kzz_dic = parse_query_2_dict(query)
            code = kzz_dic.get('code', None)
            if not code:
                return u'请输入可转债代码查询'
            days = kzz_dic.get('daysbefore', None)
            date = kzz_dic.get('date', None)
            if date:
                csv_name = conbond_data.daily_price(code, date)
                print('in date', csv_name)
                return ('file', csv_name)
            if days:
                csv_name = conbond_data.daily_before_price(code, days)
                print('in days', csv_name)
                return ('file', csv_name)

        return UserCommand.helper_info()

    # @classmethod
    # def delete_user(cls, sender):
    #     """
    #     删除指定的用户

    #     Arguments:
    #         sender {[string]} -- 删除指定用户
    #     """
    #     return User.delete_user(sender)

    # @classmethod
    # def update_user(cls, update_dict, sender):
    #     """ 更新一个用户。
    #     当用户不存在的时候创建新用户，否则直接更新信息

    #     Arguments:
    #         update_dict {dict} -- 更新信息
    #         sender {string} -- 发送者是谁，这个为不可变的name
    #     """
    #     if not update_dict:
    #         return u'瞎更你mb'

    #     return User.create_user(sender,
    #                             update_dict.get('email', None),
    #                             update_dict.get('password', None),
    #                             update_dict.get('realname', None),
    #                             update_dict.get('group', None),
    #                             update_dict.get('tel', None))


# class NoteCommand(object):
#     """
#     发送站报的命令，需要检查 group

#     当前用户本周的日志 - sunlands_webot://-note/week
#     检查 - sunlands_webot://-note/check
#     设置发送者 - sunlands_webot://-note/sender?set=[$name]
#     更新 - sunlands_webot://-chandao/update?name=[$name]&password=[$password]&oid=[$oid]
#     """

#     @classmethod
#     def helper_info(cls):
#         """
#         返回 chandao 的帮助信息
#         """
#         return u'''当前用户的日志查询 & 设置

# Example:
#     -note/check （## 仅仅查询今天的日志）
#     -note/week （## 查询本周的日志）
#     -note/update?id=[$id]&m=[$m]（## 更新当前的用户日志，可以选择更新指定 id 的日志，如不指定则直接创建新日志）
#     -note/delete?id=[$id] （## 删除指定 id 的消息）
# '''

#     def __call__(self, router_parse, sender, allow_group):
#         """ 日志相关的逻辑

#         Arguments:
#             router_parse {urlparse} -- url parse 解析出来的 router
#             sender {string} -- 由谁发出的站报指令
#         """
#         if allow_group == '1' and not User.check_user_group_id(sender, allow_group):
#             return u'恭喜您没有权限。哈哈哈哈。'

#         path = router_parse.path
#         query = router_parse.query

#         msg = None
#         if path == '/week':
#             # return u'/week %s' % sender
#             msg = Message.week_messages(sender)
#         if path == '/check':
#             # return u'/check %s' % sender
#             msg = Message.today_message(sender)
#         if path == '/update':
#             qs = parse_query_2_dict(query)
#             if qs.has_key('m') and qs.has_key('id'):
#                 # return u'/update %s, query = %s' % (sender, query)
#                 msg = Message.update_message(qs['id'], sender, qs['m'])
#             elif qs.has_key('m'):
#                 # return u'/create %s, query = %s' % (sender, query)
#                 msg = Message.add_message(sender, qs['m'])
#             else:
#                 msg = u'更新你妹啊更新 %s' % sender

#         if path == '/delete':
#             qs = parse_query_2_dict(query)
#             if qs.has_key('id'):
#                 msg = Message.delete_message(qs['id'], sender)
#             else:
#                 msg = u'%s：删除日志失败' % sender

#         return msg if msg else NoteCommand.helper_info()


# class ChandaoCommand(object):
#     """
#     发送禅道的命令，需要检查 group

#     发送 - sunlands_webot://-chandao/send
#     检查 - sunlands_webot://-chandao/check
#     更新 - sunlands_webot://-chandao/update?name=[$name]&password=[$password]&oid=[$oid]
#     """

#     @classmethod
#     def helper_info(cls):
#         """
#         返回 chandao 的帮助信息
#         """
#         return u'''禅道相关

# Example:
#     -chandao/check （## 检查当前用户禅道信息）
#     -chandao/send  (## 手动发送当前用户的禅道)
#     -chandao/update?name=[$name]&password=[$password]&oid=[$oid]  （##  设置禅道的用户名&密码，以及更新到的 object id 从任务页面获取）
# '''

#     def __call__(self, router_parse, sender, allow_group):
#         """ 禅道相关的命令解析

#         Arguments:
#             router_parse {urlparse} -- url parse 解析出来的 router
#             sender {string} -- 谁发起的禅道命令
#         """
#         if allow_group == '1' and not User.check_user_group_id(sender, allow_group):
#             return u'恭喜您没有权限。哈哈哈哈。'

#         path = router_parse.path
#         query = router_parse.query

#         if path == '/check':
#             # return u'/check %s' % sender
#             return User.user_chandao_info(sender)
#         if path == '/send':
#             # return u'/send %s' % sender
#             chandao = Chandao(sender)
#             return chandao.send()
#         if path == '/update':
#             # return u'/update %s, query = %s' % (sender, query)
#             qs = parse_query_2_dict(query)
#             return User.update_chandao(sender,
#                                        chandao_name=qs.get('name', None),
#                                        password=qs.get('password', None),
#                                        object_id=qs.get('oid', None))

#         return ChandaoCommand.helper_info()


# class CheckinCommand(object):
#     """
#     打卡相关的命令，需要检查 group

#     当前打卡情况 - sunlands_webot://-checkin
#     当前打卡情况 - sunlands_webot://-checkin/all
#     """

#     @classmethod
#     def helper_info(cls):
#         return u'打卡信息相关\n\nExample: \n\t\t-checkin （## 组内所有人打卡信息查询）'

#     def __call__(self, router_parse, sender, allow_group):
#         """打卡信息

#         Arguments:
#             router_parse {urlparse} -- url parse 解析出来的 router
#             sender {string} -- 由谁发出的发送打卡指令
#         """
#         if allow_group and not User.check_user_group_id(sender, allow_group):
#             return u'恭喜您没有权限。哈哈哈哈。'

#         checkin = CheckIn()
#         return checkin.check_all_user(allow_group)


# class SendmailCommand(object):
#     """
#     发送站报邮件的命令，需要检查 group

#     当前的邮件发送情况 - sunlands_webot://-sendmail/check
#     当前的邮件发送情况 - sunlands_webot://-sendmail?chandao=[1 | 0]&empty=[$empty]
#     """

#     @classmethod
#     def helper_info(cls):
#         return u'''发送站报（也可以同时发送全组的禅道）

# Example:
#     -sendmail?chandao=[1|0]&empty=[$empty] （## chaodao = 1 会发送禅道，这个参数可以省略 1 也是默认值。空记录会被设置为 empty 指定的内容）
#     -sendmail/check （## 检查今日日志更新情况）
# '''

#     @classmethod
#     def sendmail(cls, default_note, allow_group):
#         daily_mail = DailyMail()
#         notes = User.all_user_note(allow_group)
#         mail_sender = User.query_mail_sender()
#         now = datetime.now()
#         # 0 到 4 代表周一到周五，周五不需要发送站报
#         if now.weekday() == 4:
#             return None
#         if mail_sender:
#             return daily_mail.build_daily_report_html(notes,
#                                                       sender=mail_sender.email,
#                                                       pwd=mail_sender.password,
#                                                       empty_holder=default_note)
#         # 如果没有设置发送者
#         return u'当前还未设置邮件发送者，邮件发送失败'

#     def __call__(self, router_parse, sender, allow_group):
#         """发送站报邮件

#         Arguments:
#             router_parse {urlparse} -- url parse 解析出来的 router
#             sender {string} -- 由谁发出的发送邮件指令
#         """
#         if allow_group == '1' and not User.check_user_group_id(sender, allow_group):
#             return u'恭喜您没有权限。哈哈哈哈。'

#         path = router_parse.path
#         query = router_parse.query
#         params = parse_query_2_dict(query)

#         if path == '/check':
#             return Message.check_today_message(allow_group)
#         send_chandao = params['chandao'] == '1' \
#             if params.has_key('chandao') else True
#         default_note = params['empty'] \
#             if params.has_key('empty') else None
#         if not Message.check_empty_message(allow_group) and not default_note:
#             return u'还有人未添加周报，如果想强制发送请传递 empty 参数'
#         msg = u''
#         if User.is_sender(sender):
#             mail_result = SendmailCommand.sendmail(default_note, allow_group)
#             if mail_result:
#                 msg += mail_result

#             # 如果要发送禅道的话
#             if send_chandao:
#                 for user in User.all_users(allow_group):
#                     chandao = Chandao(user.name)
#                     status = chandao.send()
#                     msg += '%s\n' % status
#             else:
#                 print('不需要发送禅道')
#         else:
#             msg = u'%s 你不是邮件发送者' % sender

#         return msg


# class WeeklyCommand(object):
#     """
#     发送周报邮件的命令，需要检查 group

#     创建周报 - sunlands_webot://-weekly/update?[next&title&desc=$]
#     确认周报无误 - sunlands_webot://-weekly/check
#     预览周报 - sunlands_webot://weekly/review
#     """

#     @classmethod
#     def helper_info(cls):
#         return u'''周报相关（计算相对复杂，目前开发阶段未启用多线程，请一个一个运行，发送前请务必确认）

# Example：
#     -weekly/create?todo&title&desc=[$] （##  用户周报构建，todo 为下周的任务，多个任务务必以中文逗号分隔，有默认值【继续完成下周任务】，title和desc分别为项目名和内容描述）
#     -weekly/check （##  确认周报，只有每个人确认以后才能发送，即确认周报无误）
#     -weekly/review  （## 预览的本周完成内容，注意每个分组务必以【-】区分）
#     -weekly/update?done=[$done]&todo&title&desc=[$]  （## 更新周报的本周完成内容以及其它信息，注意事项同上）
#     -weekly/send  （## 确认后可以发送周报）
# '''

#     def __call__(self, router_parse, sender, allow_group):
#         """
#         发送周报邮件的命令

#         Arguments:
#             router_parse {urlparse} -- url parse 解析出来的 router
#             sender {string} -- 由谁发出的发送邮件指令
#         """
#         # if allow_group == '1' and not User.check_user_group_id(sender, allow_group):
#         # return u'恭喜您没有权限。哈哈哈哈。'

#         path = router_parse.path
#         query = router_parse.query
#         query_dict = parse_query_2_dict(query)
#         msg = None
#         if path == '/create':
#             report = WeekReporter(name=sender,
#                                   next_week=query_dict.get(
#                                       'todo', u'继续完成相应需求'),
#                                   title=query_dict.get('title'),
#                                   desc=query_dict.get('desc'))
#             msg = report.create_report()
#         else:
#             w_pr = Report.query_weekly_report(sender)
#             if not w_pr:
#                 return u'%s：本周周报还未创建' % sender
#             elif path == '/review':
#                 report_fix = w_pr.fix_report if w_pr.fix_report \
#                     else w_pr.origin_report
#                 msg = u'周报标题：%s、描述：%s。\n%s\n下周任务：%s' \
#                     % (w_pr.project_title, w_pr.description,
#                         report_fix, w_pr.next_week_todo)
#             elif path == '/check':
#                 w_pr.report_checked()
#                 msg = u'%s：可以发送周报啦' % sender
#             elif path == '/send':
#                 if w_pr.checked:
#                     w_mail = WeeklyMail()
#                     msg = w_mail.build_weekly_report_html(sender)
#                 else:
#                     msg = u'%s：请确认周报无误后再发送' % sender
#             elif path == '/update':
#                 msg = w_pr.update_report(done=query_dict.get('done'),
#                                          todo=query_dict.get('todo'), title=query_dict.get('title'),
#                                          desc=query_dict.get('desc'))
#         return msg if msg else WeeklyCommand.helper_info()


class HelpCommand(object):

    def __call__(self, router_parse, sender, allow_group):
        """ 辅助消息的文字返回，不需要检查 group

        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的帮助指令
        -help?[submodule]
        """
        helper = None
        submodule = router_parse.query
        if submodule == '':
            helper = u'''user        当前的用户信息查询
note        当前用户的日志查询 & 设置
sendmail    发送日志
chandao     禅道相关
checkin     打卡信息查询
weekly      周报任务相关
            
输入 -help?[submodule]查询子命令详细以及使用方式
'''
        elif submodule == 'user':
            helper = UserCommand.helper_info()
        # elif submodule == 'note':
        #     helper = NoteCommand.helper_info()
        # elif submodule == 'sendmail':
        #     helper = SendmailCommand.helper_info()
        # elif submodule == 'chandao':
        #     helper = ChandaoCommand.helper_info()
        # elif submodule == 'checkin':
        #     helper = CheckinCommand.helper_info()
        # elif submodule == 'weekly':
        #     helper = WeeklyCommand.helper_info()

        return helper
