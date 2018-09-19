#! /usr/bin/env python2.7
#coding=utf-8

from datetime import datetime, timedelta
from time import strptime
import json
import requests
from model import User, Session


class CheckIn(object):
    """ 
    当前用户的打卡信息查询的 class
    """

    def _query_check_info(self, user):
        """
        检查当前的打卡情况
        """
        if user is not None:
            check_in_url = \
                'http://localhost:8081/request?url=http:%2F%2Fm.ehr.sunlands.com%2Fmobile-web%2Fattendance%2FselectAttendanceData.do&params=%7B%22account%22:%22'\
                    + user.phone_number + '%22,%22accountType%22:%221%22%7D'
            r = requests.get(check_in_url)
            if r.status_code == 200:
                try:
                    key_data = json.loads(r.content)['key']
                    json_data = json.loads(key_data)
                    print('json_data = %s' % json_data)                    
                    check_in_time = json_data.get('checkInTime', None)
                    check_out_time = json_data.get('checkOutTime', None)
                    print('check_in_time = %s' % check_in_time)
                    if check_in_time == u'':
                        return u'@%s 请注意 还没打上班卡\n' % user.name
                    elif check_in_time == check_out_time:
                        now = datetime.now()
                        if now.hour >= 19:
                            check_in_date = datetime.strptime(check_in_time, \
                                "%Y-%m-%d %H:%M:%S")
                            if now - check_in_date >= timedelta(hours=9):
                                return u'@%s 请注意 还没打下班卡\n' % user.name
                            else:
                                can_check_date = check_in_date + timedelta(hours=9)
                                offset_seconds = can_check_date - now
                                offset_mins = int(offset_seconds.seconds / 60)
                                return u'@%s 还没到打下班卡时间，再忍受 %s 分钟\n' % (user.name, offset_mins)
                        else:
                            print('还没到打下班卡时间，上班卡已经打')
                except ValueError as e:
                    print('value error %s', e)
        return None

    def check_all_user(self, allow_group):
        """
        检查所有用户的打卡信息，除非是周末。
        
        Returns:
            [string] -- 返回每个成员的打卡情况，如果没有输出则代表已经打卡。
                        没有消息是好的消息。
        """
        now = datetime.now()
        if now.weekday() == 5 or now.weekday() == 6:
            return None

        msg = u''
        sess = Session()
        for user in User.all_users(allow_group, sess):
            if user.airplane_mode == True:
                continue
            result = self._query_check_info(user)
            if result:
                msg += result
        return msg

    def check_info_just_me(self, allow_group):
        msg = None
