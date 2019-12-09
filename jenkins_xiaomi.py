#! /usr/bin/env python2.7
#coding=utf-8

import os
# import sys

class JenkinsXiaoMi(object):

    def __init__(self):
        self.jenkins_dict = dict()
        self.is_running = False

    def add2jenkins(self, device_model, tag):
        if self.is_running:
            return u"正在打包中。请明天加入任务"
        msg = None
        device = '%s' % device_model
        _tag = '%s' % tag
        get_device = self.jenkins_dict.get(device)
        if get_device is None:
            msg = u'已经创建 %s %s 的任务' % (device, _tag)
        else:
            self.jenkins_dict[device] = _tag
            msg = u'已经更新 %s %s 的任务' % (device, _tag)
        self.jenkins_dict[device] = _tag
        print(msg)
        return msg

    def exec_command_queue(self):
        self.is_running = True
        for device, tag in self.jenkins_dict.items():
            print(device, tag)
            self.__exec_command(device, tag)
        self.jenkins_dict = dict()
        self.is_running = False

    def __exec_command(self, device, tag):
        git_path = '/Users/zhoubobo/Work/xiaomi/mihomeinternal'
        os.system('git -C %s reset --hard' % git_path)
        os.system('git -C %s checkout master' % git_path)
        os.system('git -C %s pull origin master --rebase' % git_path)
        branch_name = 'jenkins_%s_%s' % (device, tag)
        os.system('git -C %s checkout -b %s' % (git_path, branch_name))
        os.system('cd /Users/zhoubobo/Work/xiaomi/MiHomePackageTool;sh ./make_device_package.sh %s %s %s' % (device, tag, branch_name))
        

jenkins = JenkinsXiaoMi()