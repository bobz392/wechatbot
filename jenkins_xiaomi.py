#! /usr/bin/env python2.7
# coding=utf-8

import os
# import sys


class JenkinsXiaoMi(object):

    def __init__(self):
        self.jenkins_dict = dict()
        self.is_running = False

        self.device_repo_dict = {
            'MGCamera': 'MGCamera_iOS',
            'MXDevices': 'MXDevices',
            'Lumi': 'Mijia-Dailybuild-Lumi',
            'Xiaovv': 'Xiaovv',
            'HTPrinter': 'ht_ios_for_mi',
            'ismartalarm': 'miPluginCamera',
            'MJCatEye': 'MJCatEye',
            'MIOWLDoorRing': 'MiHomePlugin_MIDingLing',
            'Repeater': 'Repeater',
            'DunCateye': 'dun-cateye-ios',
            'ChuangMi': 'ipc-plug-ios',
        }

        self.modules = {
            'ChuangMi': 'ssh://git@dev.imilab.com:222/ipc-plug/ipc-plug-ios.git',
            'MIOWLDoorRing': 'git@github.com:MADV360/MiHomePlugin_MIDingLing.git',
            'Lumi': 'git@github.com:lumigit/Mijia-Dailybuild-Lumi.git',
            'ismartalarm': 'git@github.com:hualaikeji/miPluginCamera.git',
            'XinAnVehicle': 'git@github.com:ZhangPan0825/XinAnVehicle.git',
            'MJCatEye': 'git@github.com:derekhuangxu/MJCatEye.git',
            'SimCamCamera': 'git@github.com:XingTuZhiKong/SimCamCamera.git',
            'DunCateye': 'git@github.com:idunmi/dun-cateye-ios.git',
            'HTPrinter': 'git@github.com:Hannto/ht_ios_for_mi.git',
            'MXDevices': 'git@github.com:552322771/MXDevices.git',
            'MGCamera': 'git@github.com:laughmaker/MGCamera_iOS.git',
            'Xiaovv': 'git@github.com:hongshiforgit/Xiaovv.git'
        }

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
        if self.device_repo_dict[device] is None:
            return

        git_path = '/Users/zhoubobo/Work/xiaomi/mihomeinternal'
        print('開始處理主工程')
        os.system('git -C %s reset --hard' % git_path)
        os.system('git -C %s checkout master' % git_path)
        os.system('git -C %s pull origin master --rebase' % git_path)
        branch_name = 'jenkins_%s_%s' % (device, tag)
        os.system('git -C %s checkout -b %s' % (git_path, branch_name))
        print('開始處理合作開發的代碼')
        git_coo_path = '/Users/zhoubobo/Work/xiaomi/operation/%s' % self.device_repo_dict.get(device)
        os.system('git -C %s reset --hard' % git_coo_path)
        os.system('git -C %s fetch origin' % git_coo_path)
        os.system('git -C %s checkout %s' % (git_coo_path, tag))
        print('開始處理 jenkins 脚本')
        os.system('cd /Users/zhoubobo/Work/xiaomi/MiHomePackageTool;sh ./make_device_package.sh %s %s %s' %
                  (device, tag, branch_name))


jenkins = JenkinsXiaoMi()
