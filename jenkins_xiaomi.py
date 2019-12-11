#! /usr/bin/env python2.7
# coding=utf-8

import os
import requests
import json
# import sys


class JenkinsXiaoMi(object):

    def __init__(self):
        self.jenkins_dict = dict()
        self.is_running = False
        self.install_tag_list = []
        self.fir_token = 'ce8c5bc4174a562917c538fc704d90c1'
        self.fir_id = '5c64c7e1ca87a82dc88f257c'

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
            'YDCatY': 'YDCatY'
        }

        self.modules = {
            'ChuangMi': 'ssh://git@dev.imilab.com:222/ipc-plug/ipc-plug-ios.git',
            'MIOWLDoorRing': 'git@githubxiaomi.com:MADV360/MiHomePlugin_MIDingLing.git',
            'Lumi': 'git@githubxiaomi.com:lumigit/Mijia-Dailybuild-Lumi.git',
            'ismartalarm': 'git@githubxiaomi.com:hualaikeji/miPluginCamera.git',
            'XinAnVehicle': 'git@githubxiaomi.com:ZhangPan0825/XinAnVehicle.git',
            'MJCatEye': 'git@githubxiaomi.com:derekhuangxu/MJCatEye.git',
            'SimCamCamera': 'git@githubxiaomi.com:XingTuZhiKong/SimCamCamera.git',
            'DunCateye': 'git@githubxiaomi.com:idunmi/dun-cateye-ios.git',
            'HTPrinter': 'git@githubxiaomi.com:Hannto/ht_ios_for_mi.git',
            'MXDevices': 'git@githubxiaomi.com:552322771/MXDevices.git',
            'MGCamera': 'git@githubxiaomi.com:laughmaker/MGCamera_iOS.git',
            'Xiaovv': 'git@githubxiaomi.com:hongshiforgit/Xiaovv.git',
            'YDCatY': 'git@githubxiaomi.com:zhaolios/YDCatY.git'
        }

    def has_jenkins_task(self):
        return not self.jenkins_dict

    def add2jenkins(self, device_model, tag):
        if self.is_running:
            return u"正在打包中。请明天加入任务"
        msg = None
        _device = '%s' % device_model
        _tag = '%s' % tag

        if self.modules.get(_device) is None:
            return u'未知的 device: %s' % device_model

        get_device = self.jenkins_dict.get(_device)
        if get_device is None:
            msg = u'已经创建 %s %s 的任务' % (_device, _tag)
        else:
            self.jenkins_dict[_device] = _tag
            msg = u'已经更新 %s %s 的任务' % (_device, _tag)
        self.jenkins_dict[_device] = _tag
        print(msg)
        return msg

    def exec_command_queue(self):
        self.is_running = True
        for device, tag in self.jenkins_dict.items():
            print(device, tag)
            self.__exec_command(device, tag)
            self.install_tag_list.append('company: jenkins_%s_%s' \
                % (device, tag))
        self.jenkins_dict = dict()
        self.is_running = False
        print('所有 repo 都已经处理完')

    def query_device_name(self, repo):
        repo = '%s' % repo
        found_device = None
        for device, rp in self.modules.items():
            print(device, rp)
            if rp == repo:
                found_device = device
                break
        if found_device:
            return u'repo: %s 对应 device 为: %s' % (repo, found_device)
        return u'Unknown git repo: %s' % repo
                

    def __exec_command(self, device, tag):
        if self.device_repo_dict[device] is None:
            return

        print('開始處理合作開發的代碼')
        git_co_path = '/Users/zhoubobo/Work/xiaomi/operation/%s' \
            % self.device_repo_dict.get(device)
        os.system('git -C %s reset --hard' % git_co_path)
        os.system('git -C %s fetch origin' % git_co_path)
        os.system('git -C %s checkout %s' % (git_co_path, tag))

        print('開始處理主工程')
        git_path = '/Users/zhoubobo/Work/xiaomi/mihomeinternal'
        os.system('git -C %s reset --hard' % git_path)
        os.system('git -C %s checkout master' % git_path)
        os.system('git -C %s pull origin master --rebase' % git_path)
        branch_name = 'jenkins_%s_%s' % (device, tag)
        os.system('git -C %s push origin --delete %s' % (git_path, branch_name))
        os.system('git -C %s branch -D %s' % (git_path, branch_name))
        os.system('git -C %s checkout -b %s' % (git_path, branch_name))

        print('開始處理 jenkins 脚本')
        os.system('cd /Users/zhoubobo/Work/xiaomi/MiHomePackageTool;sh \
            ./make_device_package.sh %s %s %s' %
                  (device, tag, branch_name))

    def request_fir_info(self):
        if not self.install_tag_list:
            print('不需要检查 fir 信息，因为没有打包历史')
            return None

        check_last_url = 'http://api.fir.im/apps/latest/%s?api_token=%s' \
            % (self.fir_id, self.fir_token)
        r = requests.get(check_last_url)
        if r.status_code == 200:
            try:
                json_data = json.loads(r.content)
                changelog = json_data.get('changelog', None)
                check_log = None
                if changelog:
                    for log in self.install_tag_list:
                        if changelog.startswith(log):
                            check_log = log
                            break
                if check_log:
                    self.install_tag_list.remove(check_log)
                    get_release_url = 'http://api.fir.im/apps/%s?api_token=%s' \
                        % (self.fir_id, self.fir_token)
                    r = requests.get(get_release_url)
                    if r.status_code == 200:
                        json_data = json.loads(r.content)
                        master_release_id = \
                            json_data.get('master_release_id', None)
                        return u'%s下载地址: https://fir.im/tes5?release_id=%s' \
                            % (changelog, master_release_id)
            except ValueError as e:
                print('value error %s', e)

        return None

jenkins = JenkinsXiaoMi()

if __name__ == "__main__":
    jenkins.install_tag_list.append('company: jenkins_ChuangMi_0.0.71')
    print(jenkins.request_fir_info())
    pass
