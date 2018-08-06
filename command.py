#coding=utf-8

from urlparse import urlparse, parse_qs
from datetime import datetime
import sys
from model import User, Message
from mail import Mail
from chandao import Chandao


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
        self.commands = {
            '-user': ['-'],
            '-updateuser': ['password', 'email', 'realname'],
            '-sender': ['setme'],
            '-note': ['message', 'id', 'week'],
            '-sendmail': ['force'],
            '-help': ['-'],
            '-delete': ['-'],
            '-chandao': ['-'],
        }
        self.help_path = '-help'
        self.user_path = '-user'
        self.updateuser_path = '-updateuser'
        self.sender_path = '-sender'
        self.delete_path = '-delete'
        self.note_path = '-note'
        self.sendmail_path = '-sendmail'
        self.chandao_path = '-chandao'

    def vaild(self, text):
        """ 当前的 command 是否是合格的格式

        Arguments:
            text {[string]} -- msg

        Returns:
            {[bool]} -- 是否是需要解析的格式
        """
        parse = urlparse(text)
        return text.startswith('-')  and \
            self.commands[parse.path] is not None

    def analysis(self, text, sender):
        parse = urlparse(text)
        path = parse.path
        message = None
        print('path = %s' % path)
        if path == self.help_path:
            message = self.helper_message(text)
        elif path == self.user_path:
            message = self.query_user(sender)
        elif path == self.updateuser_path:
            message = self.update_user(text, sender)
        elif path == self.delete_path:
            message = self.delete_user(sender)
        elif path == self.sender_path:
            message = self.email_sender(text, sender)
        elif path == self.note_path:
            message = self.note_command(text, sender)
        elif path == self.sendmail_path:
            message = self.sendmail(text, sender)
        elif path == self.chandao_path:
            message = self.chandao_command(text, sender)

        return message

    def email_sender(self, text, sender):
        """当前的邮件发送者的一些查询信息

        Arguments:
            text {[string]} -- url 当前的邮件发送者是查询还是设置
            sender {[string]} -- 当前的信息发送者是谁
        """
        parse = urlparse(text)
        msg = None
        if parse.query == 'setme':
            print('set who call')
            msg = User.sender_set_to(sender)
        else:
            print('sender show call')
            msg = User.show_sender()
        return msg

    def delete_user(self, sender):
        """删除指定的用户
        
        Arguments:
            sender {[string]} -- 删除指定用户
        """
        return User.delete_user(sender)

    def query_user(self, sender):
        """查询指定的用户
        
        Arguments:
            sender {[string]} -- 发送者是谁，这个为不可变的name
        """
        return User.user_exist(sender)

    def parse_query_2_dict(self, query): 
        return dict( (k, v if len(v)>1 else v[0]) \
                for k, v in parse_qs(query).iteritems())

    def update_user(self, text, sender):
        """ 更新一个用户。
        当用户不存在的时候创建新用户，否则直接更新信息
        
        Arguments:
            text {string} -- url 用户信息字符串
            sender {string} -- 发送者是谁，这个为不可变的name
        """
        parse = urlparse(text)
        query = parse.query
        if query == '':
            return u'瞎更你mb'
        else:
            qs = self.parse_query_2_dict(query)
            return User.create_user(sender, qs.get('email', None), \
                        qs.get('password', None), qs.get('realname', None))
            # try:
            #     return User.create_user(sender, qs['email'], qs['password'])
            # except:
            #     return "Unexpected error:", sys.exc_info()[0]

    def note_command(self, text, sender):
        """ 日志相关的逻辑
        
        Arguments:
            text {string} -- url 日志信息字符串
            sender {string} -- 发送者是谁，这个为不可变的name
        """
        parse = urlparse(text)
        query = parse.query

        if query == 'week':
            return Message.week_messages(sender)
        else:
            qs = self.parse_query_2_dict(query)
            if qs.has_key('message') and qs.has_key('id'):
                return Message.update_message(qs['id'], sender, qs['message'])
            elif qs.has_key('message'):
                return Message.add_message(sender, qs['message'])
            else:
                print('message today')
                return Message.today_message(sender)
            
    def sendmail(self, text, sender):
        print('send mail!!!!')
        """发送邮件的
        
        Arguments:
            text {string} -- url 日志信息字符串
            sender {string} -- 由谁发出的发送邮件指令
        """
        msg = u''
        if User.is_sender(sender):
            now = datetime.now()
            if now.weekday() != 4:
                mail = Mail()
                infos = User.all_user_note()
                msg = mail.build_daily_report_html(infos)

            for user in User.all_users():
                chandao = Chandao(user.name)
                status = chandao.send()
                print('status = %s' % status)
                msg += '%s\n' % status
                print('msg = %s') % msg
        else:
            msg = u'%s 你不是邮件发送者' % sender
        return msg

    def chandao_command(self, text, sender):
        """ 禅道相关的命令解析
        
        Arguments:
            text {[string]} -- 禅道相关的命令的url
            sender {[string]} -- 谁发起的禅道命令
        """
        parse = urlparse(text)
        query = parse.query

        if query == 'check':
            return User.user_chandao_info(sender)
        elif query == 'send':
            c = Chandao(sender)
            return c.send()
        else: 
            qs = self.parse_query_2_dict(query)
            return User.update_chandao(sender, chandao_name=qs.get('name', None), \
                  password=qs.get('password', None), object_id=qs.get('oid', None))

    def helper_message(self, text):
        """ 辅助消息的文字返回

        -help?[submodule]
        """
        parse = urlparse(text)
        helper = None
        submodule = parse.query
        if submodule == '':
            helper = u'user       当前的用户信息查询\nupdateuser 更新当前用户的信息\nsender     当前邮件的发送者查询 & 设置\nnote       当前用户的日志查询 & 设置\nsendmail       发送日志\nchandao      禅道相关\n\n输入 -help?[submodule]查询子命令详细以及使用方式'
            
        elif submodule == 'user':
            helper = u"当前的用户信息查询\n\nExample:\n\t\t-user（## 用户名是不可变的为当前用户的微信名，如果改名了会导致用户失效）\n"
           
        elif submodule == 'updateuser':
            helper = u'更新当前用户的信息\n\nExample:\n\t\t-updateuser?password=[password]\n\t\t-updateuser?email=zhoubo@sunlands.com\n\t\t-updateuser?realname=周博'
                
        elif submodule == 'sender':
            helper = u'当前邮件的发送者的查询 & 设置\n\nExample:\n\t\t-sender （## 仅仅查询）\n\t\t-sender?setme （## 更新为当前的用户发送）'

        elif submodule == 'note':
            helper = u'当前用户的日志查询 & 设置\n\nExample: \n\t\t-note （## 仅仅查询今天的日志）\n\t\t-note?week （## 查询本周的日志）\n\t\t-note?[id & message] （## 更新当前的用户日志，可以选择更新指定 id 的日志，如不指定则直接创建新日志）'
                
        elif submodule == 'sendmail':
            helper = u'发送日志\n\nExample: \n\t\t-sendmail \n\t\t-sendmail?force  （## 强制发送，用户列表存在的会被设置为空日志）\n\t\t-sendmail?force=[msg] （## 强制发送，用户列表存在的会被设置为 msg 指定的内容）'

        elif submodule == 'chandao':
            helper = u'禅道相关\n\nExample: \n\t\t-chandao?check （## 检查当前用户禅道信息）\n\t\t-chandao?send  (## 手动发送当前用户的禅道)\n\t\t-chandao?name=[name]&password=[password]&oid=[oid]  （##需要设置禅道的用户名&密码，以及更新到的 object id 从任务页面获取）'

        return helper

