#! /usr/bin/env python2.7
#coding=utf-8

import os
# import sys

class JenkinsXiaoMi(object):

    def __init__(self):
        self.jenkins_dict = dict()

    def add2jenkins(self, device_model, tag):
        msg = None
        if self.jenkins_dict[device_model] is None:
            msg = u'已经创建 %s %s 的任务' % (device_model, tag)
        else:
            self.jenkins_dict[device_model] = tag
            msg = u'已经更新 %s %s 的任务' % (device_model, tag)
        self.jenkins_dict[device_model] = tag
        print(msg)
        return msg

    def exec_command_queue(self):
        for device, tag in self.jenkins_dict.items():
            print(device, tag)
            self.exec_command(device, tag)

    def exec_command(self, device, tag):
        git_path = '/Users/zhoubobo/Work/xiaomi/mihomeinternal'
        os.system('git -C %s reset --hard' % git_path)
        os.system('git -C %s checkout master' % git_path)
        os.system('git -C %s pull origin master --rebase' % git_path)
        branch_name = 'jenkins_%s_%s' % (device, tag)
        os.system('git -C %s checkout -b %s' % (git_path, branch_name))
        os.system('sh /Users/zhoubobo/Work/xiaomi/MiHomePackageTool/make_device_package.sh %s %s %s' % (device, tag, branch_name))
        

jenkins = JenkinsXiaoMi()