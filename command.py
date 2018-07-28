#coding=utf-8

from urlparse import urlparse, parse_qs
from user import User, Message
import sys

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
            '-user': ['name', 'password', 'email'],
            '-updateuser': ['password', 'email'],
            '-sender': ['setme'],
            '-note': ['content'],
            '-send': ['force'],
            '-help': ['-help'],
            '-delete': ['delete']
        }
        self.help_path = '-help'
        self.user_path = '-user'
        self.updateuser_path = '-updateuser'
        self.sender_path = '-sender'
        self.note_path = '-note'
        self.send_path = '-send'
        self.delete_path = '-delete'
        self.current_users = {}

    def vaild(self, text):
        """ 当前的 command 是否是合格的格式

        Arguments:
            text {[string]} -- msg

        Returns:
            {[bool]} -- 是否是需要解析的格式
        """
        o = urlparse(text)
        return text.startswith('-')  and \
            self.commands[o.path] is not None

    def analysis(self, text, sender):
        o = urlparse(text)
        message = None
        if o.path == self.help_path:
            message = self.helper_message(text)
        elif o.path == self.user_path:
            message = self.query_user(sender)
        elif o.path == self.updateuser_path:
            message = self.update_user(text, sender)
        elif o.path == self.delete_path:
            message = self.delete_user(sender)
        else:
            message = None
        return message

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

    def update_user(self, text, sender):
        """ 更新一个用户。
        当用户不存在的时候创建新用户，否则直接更新信息
        
        Arguments:
            text {string} -- url 用户信息字符串
            sender {string} -- 发送者是谁，这个为不可变的name
        """
        print('in update or create user')
        o = urlparse(text)
        query = o.query
        if query == '':
            return u'瞎更你mb'
        else:
            print('start qs')
            qs = dict( (k, v if len(v)>1 else v[0]) for k, v in parse_qs(query).iteritems())
            print('end qs')
            try:
                return User.create_user(sender, qs['email'], qs['password'])
            except:
                return "Unexpected error:"#, sys.exc_info()[0]

    def helper_message(self, text):
        """ 辅助消息的文字返回

        -help?[submodule]
        """
        o = urlparse(text)
        helper = None
        submodule = o.query
        if submodule == '':
            helper = u'user       当前的用户信息查询\nupdateuser 更新当前用户的信息\nsender     当前邮件的发送者查询 & 设置\nnote       当前用户的日志查询 & 设置\nsend       发送日志\n\n输入 -help?[submodule]查询子命令详细以及使用方式'
            
        elif submodule == 'user':
            helper = u"当前的用户信息查询\n\nExample:\n\t\t-user（## 用户名是不可变的为当前用户的微信名，如果改名了会导致用户失效）\n"
           
        elif submodule == 'updateuser':
            helper = u'更新当前用户的信息\n\nExample:\n\t\t-user?password=\'your password\'\n\t\t-user?email=\'zhoubo@sunlands.com\'\n'
                
        elif submodule == 'sender':
            helper = u'当前邮件的发送者的查询 & 设置\n\nExample:\n\t\t-sender （## 仅仅查询）\n\t\t-sender?setme （## 更新为当前的用户发送）'

        elif submodule == 'note':
            helper = u'当前用户的日志查询 & 设置\n\nExample: \n\t\t-note （## 仅仅查询）\n\t\t-note?[content] （## 更新为当前的用户日志）'
                
        elif submodule == 'send':
            helper = u'发送日志\n\nExample: \n\t\t-send \n\t\t-send?force  （## 强制发送，用户列表存在的会被设置为空日志）\n\t\t-send?force=[msg] （## 强制发送，用户列表存在的会被设置为 msg 指定的内容）'

        return helper

