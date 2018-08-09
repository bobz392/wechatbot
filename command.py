#coding=utf-8

from urlparse import urlparse, parse_qs
from datetime import datetime
import sys
from model import User, Message
from mail import DailyMail
from chandao import Chandao
from check_in import CheckIn

def parse_query_2_dict(query): 
        return dict( (k, v if len(v)>1 else v[0]) \
                for k, v in parse_qs(query).iteritems())

class Command(object):
    """命令辅助 class
    Arguments:
        object {[object]} -- [description]
    """

    def __init__(self, *args, **kwargs):
        """ 初始化当前可以使用的所有 commands
            [{string: [string]}}] -- [
                key 代表当前的参数
                list 代表可选的附带参数，详细见下面 helper_message 函数的返回说明
            ]
        """
        self.help_path = '-help'
        self.user_path = '-user'
        self.note_path = '-note'
        self.sendmail_path = '-sendmail'
        self.chandao_path = '-chandao'
        self.checkin_path = '-checkin'
        self.weekly_report_path = '-weekly'

        self.commands = {
            self.user_path: ['password', 'email', 'realname', 'sender-setme', 'sender-check'],
            self.note_path: ['message', 'id', 'week'],
            self.sendmail_path: ['empty', 'chandao'],
            self.help_path: ['-'],
            self.chandao_path: ['-'],
            self.checkin_path: ['-'],
            self.weekly_report_path: ['-'],
        }

    def vaild(self, text):
        """ 当前的 command 是否是合格的格式

        Arguments:
            text {[string]} -- msg

        Returns:
            {[bool]} -- 是否是需要解析的格式
        """
        print(text.startswith('-'))
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

    def analysis(self, message, sender):
        """
        根据消息来分解、处理
        
        Arguments:
            router_text {string} -- router 的 string，通常就是一条消息
            sender {string} -- 当前的消息发送者
        
        Returns:
            [string] -- 返回处理后的文字
        """

        router_text = u'webot://%s' % message
        parse = urlparse(router_text)
        command = parse.netloc
        if not self.commands.has_key(command):
            return HelpCommand()()
        message = None
        print('command = %s, path = %s, query = %s' \
            % (command, parse.path, parse.query))

        class_name = self.to_str(command[1:2].upper() \
            + command[2:] + 'Command')
        command_class = self.command_class(class_name)
        class_object = command_class()
        # print(type(class_object))
        # print(isinstance(class_object, HelpCommand))
        # print(class_object.__dict__)
        message = class_object(parse, sender)

        return message

class UserCommand(object):
    """
    用户相关的命令
    
    检查当前用户信息 - sunlands_webot://-user/check
    更新当前用户信息 - sunlands_webot://-user/update?password=[$password]&email=[$email]&realname=[$realname]
    切换发送者 - sunlands_webot://-user/sender-setme
    检查发送者 - sunlands_webot://-user/sender-check
    """

    @classmethod
    def helper_info(cls):
        return u'''当前的用户信息查询
Example:
    -user/check（## 用户名是不可变的为当前用户的微信名，如果改名了会导致用户失效）
    -user/update?password=[$password]&email=[$email]&realname=[$realname] （## 更新当前用户的信息）
    -user/sender-check （## 仅仅查询）
    -user/sender-setme （## 更新为当前的用户发送）
'''

    def __call__(self, router_parse, sender):
        """ 用户相关的逻辑
        
        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的指令
        """
        query = router_parse.query
        path = router_parse.path

        if path == '/check' or path == '':
            # return u'/check %s' % sender
            return User.user_exist(sender)
        if path == '/update':
            # return u'/update %s' % sender
            update_dict = parse_query_2_dict(query)
            return UserCommand.update_user(update_dict, sender)
        if path == 'sender-setme':
            # return u'/sender-setme %s' % sender
            return User.show_sender()
        if path == 'sender-check':
            # return u'/sender-check %s' % sender
            return User.sender_set_to(sender)

        return UserCommand.helper_info()

    @classmethod
    def delete_user(cls, sender):
        """
        删除指定的用户

        Arguments:
            sender {[string]} -- 删除指定用户
        """
        return User.delete_user(sender)

    @classmethod
    def update_user(cls, update_dict, sender):
        """ 更新一个用户。
        当用户不存在的时候创建新用户，否则直接更新信息

        Arguments:
            update_dict {dict} -- 更新信息
            sender {string} -- 发送者是谁，这个为不可变的name
        """
        if not update_dict:
            return u'瞎更你mb'
        else:
            return User.create_user(sender, \
                        update_dict.get('email', None), \
                        update_dict.get('password', None), \
                        update_dict.get('realname', None))

class NoteCommand(object):
    """
    发送站报的命令
    
    当前用户本周的日志 - sunlands_webot://-note/week
    检查 - sunlands_webot://-note/check
    设置发送者 - sunlands_webot://-note/sender?set=[$name]
    更新 - sunlands_webot://-chandao/update?name=[$name]&password=[$password]&oid=[$oid]
    """

    @classmethod
    def helper_info(cls):
        """
        返回 chandao 的帮助信息
        """
        return u'''当前用户的日志查询 & 设置
        
Example: 
    -note/check （## 仅仅查询今天的日志）
    -note/week （## 查询本周的日志）
    -note/update?id=[$id]&m=[$m]（## 更新当前的用户日志，可以选择更新指定 id 的日志，如不指定则直接创建新日志）
    -note/delete?id=[$id] （## 删除指定 id 的消息）
'''

    def __call__(self, router_parse, sender):
        """ 日志相关的逻辑
        
        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的站报指令
        """
        path = router_parse.path
        query = router_parse.query

        if path == '/week':
            # return u'/week %s' % sender
            return Message.week_messages(sender)
        if path == '/check':
            # return u'/check %s' % sender
            return Message.today_message(sender)
        if path == '/update':
            qs = parse_query_2_dict(query)
            if qs.has_key('m') and qs.has_key('id'):
                # return u'/update %s, query = %s' % (sender, query)
                return Message.update_message(qs['id'], sender, qs['m'])
            if qs.has_key('m'):
                # return u'/create %s, query = %s' % (sender, query)
                return Message.add_message(sender, qs['m'])

            return u'更新你妹啊更新 %s' % sender

        if path == '/delete':
            qs = parse_query_2_dict(query)
            if qs.has_key('id'):
                return Message.delete_message(qs['id'], sender)
            return u'%s：删除日志失败'

        return NoteCommand.helper_info()

class ChandaoCommand(object):
    """
    发送禅道的命令

    发送 - sunlands_webot://-chandao/send
    检查 - sunlands_webot://-chandao/check
    更新 - sunlands_webot://-chandao/update?name=[$name]&password=[$password]&oid=[$oid]
    """

    @classmethod
    def helper_info(cls):
        """
        返回 chandao 的帮助信息
        """
        return u'''禅道相关

Example: 
    -chandao/check （## 检查当前用户禅道信息）
    -chandao/send  (## 手动发送当前用户的禅道)
    -chandao/update?name=[$name]&password=[$password]&oid=[$oid]  （##  设置禅道的用户名&密码，以及更新到的 object id 从任务页面获取）
'''

    def __call__(self, router_parse, sender):
        """ 禅道相关的命令解析
        
        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 谁发起的禅道命令
        """
        path = router_parse.path
        query = router_parse.query

        if path == '/check':
            # return u'/check %s' % sender
            return User.user_chandao_info(sender)
        if path == '/send':
            # return u'/send %s' % sender
            chandao = Chandao(sender)
            return chandao.send()
        if path == '/update':
            # return u'/update %s, query = %s' % (sender, query)
            qs = parse_query_2_dict(query)
            return User.update_chandao(sender, \
                        chandao_name=qs.get('name', None), \
                        password=qs.get('password', None), \
                        object_id=qs.get('oid', None))

        return ChandaoCommand.helper_info()

class CheckinCommand(object):
    """
    打卡相关的命令
    
    当前打卡情况 - sunlands_webot://-checkin
    当前打卡情况 - sunlands_webot://-checkin/all
    """

    @classmethod
    def helper_info(cls):
        return u'打卡信息相关\n\nExample: \n\t\t-checkin （## 组内所有人打卡信息查询）'

    def __call__(self, router_parse, sender):
        """打卡信息
        
        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的发送打卡指令
        """

        checkin = CheckIn()
        return checkin.check_all_user()

class SendmailCommand(object):
    """
    发送站报邮件的命令

    当前的邮件发送情况 - sunlands_webot://-sendmail/check
    当前的邮件发送情况 - sunlands_webot://-sendmail?chandao=[1 | 0]&empty=[$empty]
    """

    @classmethod
    def helper_info(cls):
        return u'''发送站报（也可以同时发送全组的禅道）
        
Example: 
    -sendmail?chandao=[1|0]&empty=[$empty] （## chaodao = 1 会发送禅道，这个参数可以省略 1 也是默认值。空记录会被设置为 empty 指定的内容）
    -sendmail/check （## 检查今日日志更新情况）
'''
    @classmethod
    def sendmail(cls, default_note):
        daily_mail = DailyMail()
        notes = User.all_user_note()
        mail_sender = User.query_mail_sender()
        now = datetime.now()
        # 0 到 4 代表周一到周五，周五不需要发送站报
        if now.weekday() == 4:
            return None
        if mail_sender:
            return daily_mail.build_daily_report_html(notes, \
                        sender=mail_sender.email, \
                        pwd=mail_sender.password, \
                        empty_holder=default_note)
        # 如果没有设置发送者
        return u'当前还未设置邮件发送者，邮件发送失败'
            
    def __call__(self, router_parse, sender):
        """发送站报邮件
        
        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的发送邮件指令
        """
        path = router_parse.path
        query = router_parse.query
        params = parse_query_2_dict(query)

        if path == '/check':
            return Message.check_today_message()
        
        send_chandao = params['chandao'] == '1' \
            if params.has_key('chandao') else True
        default_note = params['empty'] \
            if params.has_key('empty') else None

        msg = u''
        if User.is_sender(sender):
            mail_result = SendmailCommand.sendmail(default_note)
            if mail_result:
                msg += mail_result

            # 如果要发送禅道的话
            if send_chandao:
                print('\n发送禅道中...')
                for user in User.all_users():
                    chandao = Chandao(user.name)
                    status = chandao.send()
                    print('status = %s' % status)
                    msg += '%s\n' % status
                    print('msg = %s') % msg
            else:
                print('不需要发送禅道')
        else:
            msg = u'%s 你不是邮件发送者' % sender

        return msg


class WeeklyCommand(object):
    """
    发送周报邮件的命令
        
    创建周报 - sunlands_webot://-weekly/update?[next&title&desc=$]
    确认周报无误 - sunlands_webot://-weekly/check
    预览周报 - sunlands_webot://weekly/review
    """
    
    @classmethod
    def helper_info(cls):
        return  u'''周报相关（计算相对复杂，目前开发阶段未启用多线程，请一个一个运行，发送前请务必确认）

Example：
    -weekly?[next&title&desc=$] （##  用户周报构建，next 为下周的任务，多个任务务必以中文逗号分隔，有默认值【继续完成下周任务】，title和desc分别为项目名和内容描述）
    -weekly/check （##  确认周报，只有每个人确认以后才能发送，即确认周报无误）
    -weekly/review  （## 预览的本周完成内容，注意每个分组务必以【-】区分）
    -weekly?[update=$]  （## 更新周报的本周完成内容，注意事项同上）
    -weekly?send  （## 确认后可以发送周报）
'''

    def __call__(self, router_parse, sender):
        """
        发送周报邮件的命令
        
        Arguments:
            router_parse {urlparse} -- url parse 解析出来的 router
            sender {string} -- 由谁发出的发送邮件指令
        """
        path = router_parse.path
        query = router_parse.query
        return u'开发中，请耐心'

class HelpCommand(object):

    def __call__(self, router_parse, sender):
        """ 辅助消息的文字返回

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
            
输入 -help?[submodule]查询子命令详细以及使用方式'
'''    
        elif submodule == 'user':
            helper = UserCommand.helper_info()
        elif submodule == 'note':
            helper = NoteCommand.helper_info()
        elif submodule == 'sendmail':
            helper = SendmailCommand.helper_info()
        elif submodule == 'chandao':
            helper = ChandaoCommand.helper_info()
        elif submodule == 'checkin':
            helper = CheckinCommand.helper_info()
        elif submodule == 'weekly':
            helper = WeeklyCommand.helper_info()

        return helper
