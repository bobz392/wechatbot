#coding=utf-8

from urlparse import urlparse, parse_qs
import sys
from jenkins_xiaomi import jenkins
from config import Config

def parse_query_2_dict(query):
    return dict((k.lower(), v if len(v) > 1 else v[0]) \
            for k, v in parse_qs(query).iteritems())

class Command(object):
    """命令辅助 class
    Arguments:
        object {[object]} -- [description]
    """

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
        self.sendmail_path = '-sendmail'
        self.chandao_path = '-chandao'
        self.checkin_path = '-checkin'
        self.weekly_report_path = '-weekly'
        self.jenkins_path = '-jenkins'

        self.commands = {
            self.user_path: ['password', 'email', 'realname', 'sender-setme', 'sender-check'],
            self.note_path: ['message', 'id', 'week'],
            self.sendmail_path: ['empty', 'chandao'],
            self.help_path: ['-'],
            self.chandao_path: ['-'],
            self.checkin_path: ['-'],
            self.weekly_report_path: ['-'],
            self.jenkins_path: ['-'],
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
        router_text = u'webot://%s' % message
        parse = urlparse(router_text)
        command = parse.netloc.lower()
        if not self.commands.has_key(command):
            return HelpCommand()()
        message = None
        print('command = %s, path = %s, query = %s' \
            % (command, parse.path, parse.query))

        class_name = self.to_str(command[1:2].upper() \
            + command[2:] + 'Command')
        command_class = self.command_class(class_name)
        command_class_object = command_class()
        message = command_class_object(parse, sender, allow_group)

        return message

    def jenkins_check_fir(self):
        return jenkins.request_fir_info()

    def has_jenkins_task(self):
        return jenkins.has_jenkins_task()

    def jenkins_operation(self):
        jenkins.exec_command_queue()

class JenkinsCommand(object):
    def __call__(self, router_parse, sender, allow_group):
        path = router_parse.path
        query = router_parse.query
        query_dict = parse_query_2_dict(query)

        if path == '/create':
            tag = query_dict.get('tag')
            device = query_dict.get('device')
            base = query_dict.get('base', 'master')
            return jenkins.add2jenkins(device, tag, base, sender=sender)
        elif path == '/query':
            repo = query_dict.get('repo')
            return jenkins.query_device_name(repo)
        elif path == '/do':
            if sender == Config.admin and allow_group != Config.group_identity:
                jenkins.exec_command_queue(update_pod=False)
        elif path == '/list':
            if sender == Config.admin \
                and allow_group != Config.group_identity:
                return jenkins.query_fir_check()
                # if query_dict
                # tag = query_dict.get('tag', d=None)
                # device = query_dict.get('device', d=None)
                # print(tag)
                # print(device)
                # if tag and device:
                #     jenkins.create_fir_check(device, tag, '%s' % sender)
                # else:
                #     print('query in command')
                    

    @classmethod
    def helper_info(cls):
        return u'06:00, 23:00两个时间点会进行打包操作\n\nExample: \n\t\t-jenkins/create?device=Chuangmi&tag=0.1.2\n\t\t-jenkins/query?repo=git@github.com:derekhuangxu/MJCatEye.git'

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
        # elif submodule == 'user':
        #     helper = UserCommand.helper_info()
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
        helper = None
        if submodule == 'jenkins':
            helper = JenkinsCommand.helper_info()
        return helper
