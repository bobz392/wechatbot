#! /usr/bin/env python2.7
# coding=utf-8

import schedule
from datetime import datetime


class NotifyWork (object):

    def __init__(self):
        self.works = {}
        self.notify_group = None

    def set_group(self, group):
        self.notify_group = group

    def do_notify(self, by_who):
        do_things = self.works.pop(by_who)
        schedule.clear(by_who)
        print('worked')
        if self.notify_group:
            do_things = do_things.replace(u'=at=', u'@')
            notify_content = u'%s' % (do_things)
            self.notify_group.send(notify_content)

    def can_notify(self, by_who):
        return self.works.get(by_who) is None

    def remove_notify(self, by_who):
        if not self.can_notify(by_who):
            self.works.pop(by_who)
            schedule.clear(by_who)
            return u'%s 已移除提醒' % by_who
        return u'%s 瞎删你妹的' % by_who

    def check_notify_time(self, time):
        try:
            date_time = datetime.strptime(time, '%H:%M')
            print(date_time)
            return date_time
        except ValueError as excp:
            print('error')
            return None

    def notify_me_at(self, time, by_who, do_things):
        print(u'at = %s, by_who = %s, do = %s' % (time, by_who, do_things))
        if self.can_notify(by_who) and self.check_notify_time(time) is not None:
            self.works[by_who] = do_things
            s = schedule.every().days.at(time).do(self.do_notify, by_who=by_who).tag(by_who)
            offset = s.next_run - datetime.now()
            return u'%s 已设置 %s 的提醒，还有 %s 这么长时间。' % (by_who, time, offset)

        return u'@%s 你傻不傻' % by_who


notify_work_instance = NotifyWork()

if __name__ == '__main__':
    nw = NotifyWork()
    nw.notify_me_at(u'18:07', u'zhou', u'do nimei')
    import time
    while True:
        schedule.run_pending()
        time.sleep(1)
