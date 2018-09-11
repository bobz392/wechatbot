#! /usr/bin/env python2.7
#coding=utf-8

from sqlalchemy import Column, String, ForeignKey,\
    DateTime, Integer, BigInteger, Boolean, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_, func, create_engine
from datetime import datetime, timedelta

Base = declarative_base()

engine = create_engine('sqlite:///shit-email.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

class DBError(RuntimeError):
    def __init__(self, arg):
        self.args = arg

def first_date_of_week():
    now = datetime.now()
    weekday_of_today = now.weekday()
    first_day = now - timedelta(days=weekday_of_today)
    return datetime(first_day.year, first_day.month, first_day.day, \
                hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

class User(Base):

    __tablename__ = 'user'

    name = Column(String(50), primary_key=True)
    email = Column(String(40), unique=True)
    realname = Column(String(10))
    # 邮件发送者的邮箱密码
    password = Column(String(40))
    sender = Column(Boolean, default=False)
    airplane_mode = Column(Boolean, default=False)
    phone_number = Column(String(11), default=None)
    # 禅道
    chandao_object_id = Column(String(40), default=None)
    chandao_name = Column(String(40), default=None)
    chandao_password = Column(String(40), default=None)
    # 分组
    group = Column(String(60), default=None)

    # useless
    chandao_session_id = Column(String(40), default=None)
    chandao_za = Column(String(40), default=None)

    @staticmethod
    def all_users(allow_group, sess=session):
        return sess.query(User)\
                .filter(User.group == allow_group).all()

    @staticmethod
    def query_user(name):
        return session.query(User).filter(User.name == name).first()

    @staticmethod
    def query_user_group(name):
        group_id = User.query_user_group_id(name)
        msg = None
        if group_id :
            group = Group.query_group_name(group_id)
            if group:
                msg = u'用户:%s，分组（id = %s）为%s。' \
                    % (name, group_id, group)
            else:
                msg = u'用户:%s，目前没有分组' % name
        else:
            msg = u'用户：%s 不存在。' % name
        return msg

    @staticmethod
    def query_user_group_id(name):
        """查询当前用户的 group id
        
        Arguments:
            name {string} --  用户名
        
        Returns:
             string --  当前的用户 group id 没有返回 none
        """
        user = User.query_user(name)
        if user:
            return user.group
    
        return None

    @staticmethod
    def set_user_airplane_mode(name, mode):
        user = User.query_user(name)
        if user:
            user.airplane_mode = mode
            session.commit()
            return u'%s：设置飞行模式成功，当前 %s' % \
                (name, u'开启' if mode else u'关闭')
            
        return u'%s：设置勿扰模式失败'

    @staticmethod
    def update_user_group_id(name, group_id):
        user = User.query_user(name)
        group = Group.query_group_name(group_id)
        if user and group:
            user.group = group_id
            session.commit()
            return  u'用户：%s 分组更新为 id = %s' \
                % (name, group_id)

        return u'用户：%s 不存在或者分组 id = %s 不存在。' \
            % (name, group_id)

    @staticmethod
    def user_chandao_info(name):
        """用户的禅道信息
        """
        user = User.query_user(name)
        msg = None
        if user:
            msg = u'用户 %s\nchandao name： %s\nobject id：%s' \
                % (name, user.chandao_name, user.chandao_object_id)
        else:
            msg = u'都没注册信息，查询 nmb'
        return msg

    @staticmethod
    def update_chandao(name, chandao_name=None, password=None, object_id=None):
        user = User.query_user(name)
        msg = None
        if user:
            if chandao_name:
                user.chandao_name = chandao_name
            if password:
                user.chandao_password = password
            if object_id:
                user.chandao_object_id = object_id
            session.commit()
            msg = u'禅道信息更新成功'
        else:
            msg = u'都没注册信息，查询 nmb'
        return msg

    @staticmethod
    def create_user(name, email=None, password=None, \
                    realname=None, group=None, tel=None):
        """创建一个 user 如果必要的话，如果当前 user 已经存在，那么会更新不为空的信息。

        Arguments:
            name {string} -- 需要更新或者创建的用户

        Keyword Arguments:
            email {string} -- 263邮箱 (default: {None})
            password {string} -- 263邮箱密码 (default: {None})
            realname {string} -- 真实的名字，如果这里为 None 会拆分邮箱前缀 (default: {None})
        """
        user = User.query_user(name)
        msg = u'创建或者更新异常'
        if user:
            if email:
                user.email = email
            if password:
                user.password = password
            if realname:
                user.realname = realname
            if group and Group.query_group_name(group):
                user.group = group
            if tel:
                user.phone_number = tel
            session.commit()
            msg = u'更新成功'
        else:
            if email == None or password == None:
                msg = u'邮箱和密码不能为空'
            else:
                emailnames = email.split('@')
                emailname = emailnames[0] if len(emailnames) >= 1 else email
                realname = realname if realname is not None else emailname
                user = User(name=name, email=email, \
                    password=password, realname=realname)
                user.group = group
                user.phone_number = tel
                user.airplane_mode = False
                session.add(user)
                session.commit()
                if user in session:
                    msg = u'用户 %s 创建成功' % name
                else:
                    msg = u'用户 %s 创建失败' % name
        return msg

    @staticmethod
    def check_user_group_id(name, group_id):
        """检查用户的 group id 是否正确

        Arguments:
            group_id {int} -- 检查的 group id

        Return:
            返回是否是正确的分组
        """
        user = User.query_user(name)
        if user:
            return user.group == group_id

        return False

    @staticmethod
    def is_sender(name):
        """ 指定的用户是不是邮件发送者

        Arguments:
            sender {string} -- 当前消息发送者的名字
        """
        user = User.query_user(name)
        if user:
            return user.sender
        else:
            return False

    @staticmethod
    def sender_set_to(name):
        """设置当前的 sender 为 name 的 user

        Arguments:
            name {string} -- 当前的发送者的名字，也是即将被设置为邮件发送者

        Returns:
            {string} -- 设置的相关信息返回
        """
        maybe_sender = User.query_user(name)
        if maybe_sender:
            current_sender = session.query(User).filter(User.sender == True).first()
            msg = u''
            if current_sender:
                if current_sender.name == maybe_sender.name:
                    return u'你他mb的设置个毛啊，本来就是你'
                else:
                    current_sender.sender = False
                    msg += u'发送者 %s 已经被取消\n' % current_sender.name
            maybe_sender.sender = True
            msg += u'发送者 %s 已经被设置' % maybe_sender.name
            session.commit()
            return msg
        else:
            return u'都没注册信息，发送 nmb'

    @staticmethod
    def query_mail_sender():
        """返回当前的 mail 发送者
        """
        return session.query(User).filter(User.sender == True).first()

    @staticmethod
    def show_sender():
        """ 查询当前的邮件发送者是谁
        
        Returns:
            {string} -- 返回发送者的名字信息
        """
        user = User.query_mail_sender()
        if user:
            return u'当前发送者为 %s' % user.name
        else:
            return u'当前未设置发送者'

    @staticmethod
    def delete_user(name):
        user = User.query_user(name)
        if user:
            session.delete(user)
            session.commit()
            return u'删除 %s 的用户成功' % name
        else:
            return u'瞎删你mb'

    @staticmethod
    def user_exist(name):
        """查询指定用户是否存在

        Arguments:
            name {string} -- 查询的用户名，用户名在数据库中是唯一的，并且为微信名
        """
        user = User.query_user(name)
        sender = u'是发送者' if user.sender else u'不是发送者'
        group_info = None
        if user.group:
            group = Group.query_group_name(user.group)
            if group:
                group_info = u'分组为(id=%s-%s)，' % \
                            (user.group, group.group_name)
            else:
                group_info = u''
        else:
            group_info = u''

        return u'叫 %s(%s) 的用户存在，%s邮箱为 %s，%s' % \
            (name, user.realname, group_info, user.email, sender) \
            if user else u'叫 %s 的用户不存在' % name

    @staticmethod
    def all_user_note(allow_group):
        """返回今天所有人的记录
        """
        users = session.query(User)\
            .filter(User.group == allow_group)\
            .all()
        all_notes = {}
        for u in users:
            print('user = %s, realname = %s' % (u.name, u.realname))
            messages = Message.query_today_message(u.name).all()
            print('has %d message' % len(messages))
            all_notes[u.realname] = messages
        return all_notes

    def __str__(self):
        return '%s(%s)' % (self.name, self.email)
        

class Message(Base):

    __tablename__ = 'message'

    id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    sender = Column(String(50), ForeignKey('user.name'))
    message = Column(String(200))
    date_create = Column(DateTime, default=datetime.now)

    @staticmethod
    def add_message(sender, message):
        m = Message(sender=sender, message=message)
        session.add(m)
        session.commit()
        if m in session:
            return u'添加成功'
        else:
            return u'添加记录失败'

    @staticmethod
    def update_message(id, sender, message):
        """创建或者更新一条记录
        
        Arguments:
            id {string} -- 如果需要更新的话会指定一个记录的 id，创建则不传递这个字段
            sender {string} -- 发送者的名字
            message {string} -- 一条记录的内容
        
        Returns:
            [string] -- 创建或者更新的结果文字
        """
        m = session.query(Message) \
                .filter(and_(Message.sender == sender, Message.id == id)) \
                .first()
        if m is None:
            return u'id = %s 的记录不存在' % id
        else:
            m.message = message
            session.commit()
            return u'记录更新成功，id 为 %s' % m.id

    @staticmethod
    def delete_message(msg_id, sender):
        """
        删除一条指定 id 的消息

        Arguments:
            id {string} -- 删除消息的 id
            sender {[type]} -- 确保删除的消息是自己的
        """
        msg = session.query(Message) \
                .filter(and_(Message.sender == sender, Message.id == msg_id)) \
                .first()
        if msg is None:
            return u'id = %s 的记录不存在' % msg_id
        else:
            session.delete(msg)
            session.commit()
            return u'id = %s 的消息删除成功' % msg_id
            

    @staticmethod
    def query_today_message(sender):
        """
        指定用户今日的全部日志

        Arguments:
            sender {string} -- 查询日志的用户名
        """
        now = datetime.now()
        today = datetime(now.year, now.month, now.day, \
                hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
        return session.query(Message) \
                .filter(and_(Message.sender == sender, Message.date_create > today))

    @staticmethod
    def check_today_message(allow_group):
        """
        检查当前所有用户的日志情况
        """ 
        msg = u''
        for user in User.all_users(allow_group):
            msg += u'%s' % user.name
            message_count = len(Message.query_today_message(user.name).all())
            msg += u' 今日%d条日志已添加\n' % message_count \
                if message_count > 0 else u' 今日日志未添加\n'
        if msg:
            return msg

    @staticmethod
    def check_empty_message(allow_group):
        """
        检查今日组内每个人的消息是否都添加

        Returns:
            [Boolean] -- 返回 bool 代表当前是否都添加完
        """
        checked = True
        for user in User.all_users(allow_group):
            message_count = len(Message.query_today_message(user.name).all())
            if message_count <= 0:
                checked = False
                break
        return checked

    @staticmethod
    def query_weekly_message(sender):
        """
        查询每周用户为 sender 名下所有消息记录。
        """
        first_day_of_week = first_date_of_week()
        return session.query(Message) \
                .filter(and_(Message.sender == sender, Message.date_create > first_day_of_week))

    @staticmethod
    def week_messages(sender):
        """
        本周的指定用户的全部日志

        Arguments:
            sender {string} -- 查询本周日志的用户名

        Returns:
            [Message] -- 本周指定用户的所有日志
        """
        s = ''
        for m in Message.query_weekly_message(sender):
            s += 'id=%s, content=%s-%s\n' \
                % (m.id, m.message, m.date_create.strftime("%Y-%m-%d"))
        return s

    @staticmethod
    def today_message(sender):
        s = ''
        for m in Message.query_today_message(sender):
            s += 'id=%s, content=%s\n' % (m.id, m.message)

        return  u'今日无%s的记录' % sender if len(s) <= 0 else s

class Report(Base):
    """
    每周日报的 orm 模型类
    """
    __tablename__ = 'weekly_report'

    report_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    reporter = Column(String(50), ForeignKey('user.name'))

    origin_report = Column(Text, default=None)
    checked = Column(Boolean, default=False)
    # 用户可以更新周报，但是永远不会改变原始记录
    fix_report = Column(Text, default=None)

    # 周报的时间间隔记录
    start_date = Column(DateTime, default=first_date_of_week)
    end_date = Column(DateTime, default=datetime.now)

    next_week_todo = Column(Text, default=None)
    project_title = Column(String(40), default=None)
    description = Column(String(40), default=None)

    @staticmethod
    def create_report(reporter, origin_report, todo, \
        project_title=None, description=None):
        """
        创建一个指定用户的原始周报。

        Arguments:
            reporter {string} -- 周报是为谁创建的
            origin_report {string} -- 周报的内容，其中 ‘-’开头的行为一组记录的关键词
            todo {string} -- 下周代办的内容，多条代办以中文逗号分隔
            project_title {string} -- 项目名，在邮件中展示用 默认值见代码
            description {string} -- 项目的描述，在邮件中展示用 默认值见代码
        Raises:
            Exception -- 插入失败的话返回异常

        Returns:
            [None] -- 成功无返回
        """
        title = project_title if project_title else u'尚德机构企业版App'
        desc = description if description else u'尚德机构 iOS-App'

        if Report.query_weekly_report(reporter):
            raise DBError('report')
        report = Report(reporter=reporter, origin_report=origin_report, \
            next_week_todo=todo, project_title=title, description=desc)
        session.add(report)
        session.commit()
        if report in session:
            return report.report_id
        else:
            raise DBError('report')

    @staticmethod
    def query_weekly_report(reporter):
        """
        查询本周周报

        Arguments:
            reporter {string} -- 周报的查询者

        Returns:
            [Reporter | None] -- 返回本周周报或者 none
        """
        first_day_of_week = first_date_of_week()
        return session.query(Report) \
                .filter(and_(Report.reporter == reporter, \
                    Report.start_date >= first_day_of_week)) \
                .first()

    @staticmethod
    def week_date_duration():
        """
        辅助函数返回当前本周一到周五区间的文字
        """
        style = '%Y.%m.%d'
        first_day = first_date_of_week().strftime(style)
        now = datetime.now().strftime(style)
        return u'%s-%s' % (first_day, now)

    def report_checked(self):
        """
        设置用户本周的周报为通过 review
        """
        self.checked = True
        if not self.fix_report:
            self.fix_report = self.origin_report
        session.commit()

    def update_report(self, done=None, \
                todo=None, title=None, desc=None):
        """
        更新本周的周报

        Keyword Arguments:
            done {string} -- 周报的主体内容 (default: {None})
            todo {string} -- 周报的主体内容 (default: {None})
            title {string} -- 标题 (default: {None})
            desc {string} -- 描述 (default: {None})
        """
        if done or todo or title or desc:
            if done:
                self.fix_report = done
            if todo:
                self.next_week_todo = todo
            if title:
                self.project_title = title
            if desc:
                self.description = desc
            session.commit()
            return u'%s：更新周报成功' % self.reporter
        else:
            return u'%s：瞎更 nmb' % self.reporter


class Group(Base):
    """
    用户分组的 orm 模型类
    """
    __tablename__ = 'group'

    group_id = Column(BigInteger().with_variant(Integer, "sqlite"), primary_key=True)
    group_name = Column(String(50))

    @staticmethod
    def query_group_name(gid):
        """查询指定 id 的分组

        Arguments:
            gid {int} -- 分组的 id

        Returns:
            [Group] -- 查询到的分组模型或者 None
        """
        return session.query(Group) \
                .filter(Group.group_id == gid)\
                .first()


Base.metadata.create_all(engine)
