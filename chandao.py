#! /usr/bin/env python2.7
#coding=utf-8

from model import User, Message
import requests
import time

class Chandao(object):
    """ 禅道发送的 support

    需要依赖 request 来发送，同时需要用户自己配置 task id 等相关信息后才能发送
    """

    def __init__(self, sender):
        self.sender = sender
        self.consumed = 8
        self.left = 100
        self.user = None
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
            }

    def check_condition(self):
        """检查当前用户能否发禅道的条件
        cookie 中
            za - user name
            zentaosid - 禅道的 session id

        Return:
            如果返回有文本的话，说明不符合条件，需要用户修改对应的信息
            返回 None 则可以发送禅道
        """
        user = User.query_user(self.sender)
        if user is None:
            return u'用户(%s)不存在' % self.sender
        elif user.chandao_name is None or user.chandao_password is None:
            return u'%s 禅道的用户名和密码为空' % self.sender
        else: 
            return None

    
    def send(self, consumed=None, left=None):
        """
        发送一个禅道日志的请求
        
        Keyword Arguments:
            consumed {int} -- 当天任务记录多少时间 (default: {每天工作时长 8 小时})
            left {int} -- 任务还剩余多少时间 (default: {剩余默认100小时})
        
        warring 目前这个逻辑没有生效
        """
        if consumed:
            self.consumed = consumed
        if left:
            self.left = left
            
        user = User.query_user(self.sender)
        today_messages = Message.query_today_message(self.sender)
        work = u''
        for idx, msg in enumerate(today_messages):
                work += u'%s、%s；' % (idx + 1, msg.message)
        print('prepar send')
        if len(work) <= 0:
            return u'%s 今天的日志不存在' % self.sender
        else:
            cookie = self.login()            
            if cookie is None:
                print('login failed')
                return u'%s 禅道登录失败' % self.sender
            else:
                print('prepar success')
                payload = self.create_payload(user, work)
                cookies = self.create_cookie(user, cookie)
                url = 'http://pm.shangdejigou.cn/effort-createForObject-task-%s.html?onlybody=yes' \
                    % user.chandao_object_id
                r = requests.post(url, data=payload, cookies=cookies)
                content = r.content
                print('chandao send status %s', r)
                print('content = %s' % r.content)
                if r.status_code == 200 and '<script>self.location=\'/user-login' not in content:
                    return u'%s 禅道发送完成' % user.name
                else:
                    return u'%s 禅道发送失败, %s' % (user.name, content)

    
    def login(self):
        """
        由于 session 的维护方式不稳定。
        所以帮助用户登录自己的禅道获取最新的 session 。
        """
        url = 'http://pm.shangdejigou.cn/user-login.html'
        user = User.query_user(self.sender)
        if user:
            login_payload = {}
            login_payload['account'] = user.chandao_name
            login_payload['password'] = user.chandao_password
            login_payload['keepLogin[]'] = 'on'
            login_payload['referer'] = 'http://pm.shangdejigou.cn/my-task.html'
            with requests.Session() as s:
                resp = s.post(url, data=login_payload)
                print(resp)
                print(resp.content)
                if resp.status_code == 200 and \
                    '<script>parent.location=\'http://pm.shangdejigou.cn/my-task.html' in resp.content:
                    return s.cookies.get_dict()
                else:
                    return None
        else:
            return None

    def create_payload(self, user, work):
        """
        禅道请求的 post 中所携带的 payload 拼接。
        """
        date = time.strftime('%Y-%m-%d', time.localtime())
        
        payload = {}
        for idx in xrange(1, 2):
            id_key = 'id[%d]' % idx
            payload[id_key] = idx
            
            date_key = 'dates[%d]' % idx
            payload[date_key] = date
            
            consumed_key = 'consumed[%d]' % idx
            payload[consumed_key] = '%d' % self.consumed
            
            left_key = 'left[%d]' % idx
            payload[left_key] = '%d' % self.left

            object_key = 'objectType[%d]' % idx
            payload[object_key] = 'task'

            object_id_key = 'objectID[%d]' % idx
            payload[object_id_key] = user.chandao_object_id

            work_key = 'work[%d]' % idx
            payload[work_key] = work
        return payload

    def create_cookie(self, user, login_cookies):
        """禅道请求的 post 中所携带的 cookie 拼接

        Return:
            返回 cookie jar
        """
        jar = requests.cookies.RequestsCookieJar()
        domain = '.pm.shangdejigou.cn'
        for k, v in login_cookies.items():
            jar.set(k, v, domain=domain, path='/')
        return jar