#! /usr/bin/env python2.7
# coding=utf-8

import os, sys
import json
import requests
from config import Config
reload(sys)
sys.setdefaultencoding('utf-8')
class JenkinsModel(object):

    def __init__(self, tag, base, sender=None):
        self.tag = tag
        self.base = base
        if sender:
            self.sender = '%s' % sender
        else:
            self.sender = ''


class JenkinsXiaoMi(object):

    def __init__(self):
        self.jenkins_dict = dict()
        self.is_running = False
        self.install_tags = dict()
        self.fir_token = Config.fir_token
        self.fir_id = Config.fir_id

    def has_jenkins_task(self):
        return len(self.jenkins_dict) > 0

    def create_fir_check(self, device, git_tag, sender):
        tag_key = 'company:jenkins_%s_%s' % (device, git_tag)
        self.install_tags[tag_key] = sender

    def query_fir_check(self):
        print('query')
        msg = None
        for fir_check, sender in self.install_tags.items():
            msg += fir_check + ' - ' + sender + '\n'
        print(msg)
        return u'%s' % msg

    def add2jenkins(self, device_model, git_tag, base='master', sender=None):
        print('type of sender = %s' % type(sender))
        if self.is_running:
            return u"正在打包中。请明天加入任务"
        msg = None
        _device = '%s' % device_model
        _tag = '%s' % git_tag
        _sender = self.to_str(sender)

        if Config.modules.get(_device) is None:
            return u'未知的 device: %s' % device_model

        jenkins_model = self.jenkins_dict.get(_device)
        if jenkins_model is None:
            jenkins_model = JenkinsModel(_tag, base, _sender)
            msg = u'已经创建 %s %s 的任务' % (_device, _tag)
        else:
            jenkins_model.tag = _tag
            jenkins_model.base = base
            jenkins_model.sender = _sender
            msg = u'已经更新 %s %s 的任务' % (_device, _tag)
        self.jenkins_dict[_device] = jenkins_model
        return msg

    def exec_command_queue(self, update_pod=True):
        self.is_running = True
        if update_pod:
            pod_path = Config.git_path + '/MiHome'
            os.system('cd %s; pod _1.6.1_ repo update' % pod_path)
        for device, jenkins_model in self.jenkins_dict.items():
            self.__exec_command(device, jenkins_model.tag, jenkins_model.base)
            self.create_fir_check(device, jenkins_model.tag, jenkins_model.sender)
        self.jenkins_dict = dict()
        self.is_running = False
        print('所有 repo 都已经处理完')

    def query_device_name(self, repo):
        repo = '%s' % repo
        found_device = None
        for device, rp in Config.modules.items():
            print(device, rp)
            if rp == repo:
                found_device = device
                break
        if found_device:
            return u'repo: %s 对应 device 为: %s' % (repo, found_device)
        return u'Unknown git repo: %s' % repo

    def __exec_command(self, device, tag, base):
        if Config.device_repo_dict[device] is None:
            return

        print('開始處理合作開發的代碼')
        git_co_path = '%s%s' \
            % (Config.git_co_path, Config.device_repo_dict.get(device))
        if not Config.device_git_existed(device):
            print('合作开发代码不存在')
            os.system('git -C %s clone %s' \
                % (Config.git_co_path, Config.modules.get(device)))
        os.system('git -C %s reset --hard' % git_co_path)
        os.system('git -C %s fetch origin' % git_co_path)
        os.system('git -C %s checkout %s' % (git_co_path, tag))
        os.system('git -C %s pull origin %s' % (git_co_path, tag))

        print('開始處理主工程')
        git_path = Config.git_path
        os.system('git -C %s reset --hard' % git_path)
        print('base = %s' % base)
        if base == 'master':
            os.system('git -C %s checkout master' % git_path)
            os.system('git -C %s pull origin master --rebase' % git_path)
        else:
            os.system('git -C %s checkout %s' % (git_path, base))
            os.system('git -C %s pull origin %s --rebase' % (git_path, base))

        branch_name = 'jenkins_%s_%s' % (device, tag)
        os.system('git -C %s push origin --delete %s' % (git_path, branch_name))
        os.system('git -C %s branch -D %s' % (git_path, branch_name))
        os.system('git -C %s checkout -b %s' % (git_path, branch_name))

        print('開始處理 jenkins 脚本')
        os.system('cd %s;sh \
            ./make_device_package.sh %s %s %s' %
                  (Config.git_package_path, device, tag, branch_name))

    def request_fir_info(self):
        if not self.install_tags:
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
                sender = None
                if changelog:
                    changelog = self.to_str(changelog)
                    print('最新的 change log: %s' % changelog)
                    
                    for fir_check, s in self.install_tags.items():
                        if changelog.startswith('%s' % fir_check):
                            check_log = fir_check
                            sender = s
                            break
                if check_log:
                    del self.install_tags[check_log]
                    get_release_url = 'http://api.fir.im/apps/%s?api_token=%s' \
                        % (self.fir_id, self.fir_token)
                    r = requests.get(get_release_url)
                    if r.status_code == 200:
                        json_data = json.loads(r.content)
                        master_release_id = \
                            json_data.get('master_release_id', None)
                        if master_release_id:
                            master_release_id = self.to_str(master_release_id)
                            master_release_id = '%s' % master_release_id
                            msg = '@%s:%s下载地址: https://fir.im/tes5?release_id=%s' \
                                % (sender, changelog, master_release_id)
                            print(msg)
                            return unicode(msg)
                else:
                    print('最新的 change log: %s 不在 tag list 中，没有打包历史' % changelog)
            except ValueError as e:
                print('value error %s', e)

        return None

    def to_str(self, unicode_or_str):
        if isinstance(unicode_or_str, unicode):
            value = unicode_or_str.encode('utf-8')
        else:
            value = unicode_or_str
        return value

jenkins = JenkinsXiaoMi()

if __name__ == "__main__":
    sender = u'王八蛋'
    print(type(jenkins.to_str(sender)))
    jenkins.install_tags['company:jenkins_MJCatEye_0.3.7'] = jenkins.to_str(sender)
    s = jenkins.request_fir_info()
    print(s)
    # git_co_path = '/Users/zhoubobo/Work/xiaomi/operation/%s' \
    #         % jenkins.device_repo_dict.get('ChuangMi')
    # tag = '0.0.70'
    # os.system('git -C %s reset --hard' % git_co_path)
    # os.system('git -C %s fetch origin' % git_co_path)
    # print(os.system('git -C %s checkout %s' % (git_co_path, tag)))

    # print(len(jenkins.install_tags))
    # jenkins.install_tags.remove('company:jenkins_Xiaovv_1.0.8')
    # print(len(jenkins.install_tags))
