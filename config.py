# coding=utf-8

import os

class Config(object):

    #### 关于 wxpy 使用的名字需要 utf-8 format
    ##

    # 当前的管理员账号微信名字
    admin = u'M_zhou'
    # 启用监听特定的组的名字
    group_name = u'米家iOS合作开发沟通群'
    # 长时间不发消息会导致微信把你踢下线，这里给另外一个无用的微信发送随意的消息来保活
    keep_alive_user = u'阿力木'
    # 打包的时间数组
    build_times = ['06:00', '23:00']
    # group 的标识，不需要更变
    group_identity = '3'
    # 主工程的路径
    git_path = '/Users/zhoubobo/Desktop/mihomeinternal'
    # 协作开发的工程目录（厂商的设备，这个目录需要和主工程同级）
    git_co_path = '/Users/zhoubobo/Desktop/operation/'
    # 打包工具目录
    git_package_path = '/Users/zhoubobo/Desktop/MiHomePackageTool'
    # 上传 fir 相关
    fir_token = 'ce8c5bc4174a562917c538fc704d90c1'
    fir_id = '5c64c7e1ca87a82dc88f257c'

    ##
    ####

    device_repo_dict = {
        'MGCamera': 'MGCamera_iOS',
        'MXDevices': 'MXDevices',
        'Lumi': 'Mijia-Dailybuild-Lumi',
        'Xiaovv': 'Xiaovv',
        'HTPrinter': 'ht_ios_for_mi',
        'ismartalarm': 'miPluginCamera',
        'MJCatEye': 'MJCatEye',
        'XinAnVehicle': 'XinAnVehicle',
        'MIOWLDoorRing': 'MiHomePlugin_MIDingLing',
        'Repeater': 'Repeater',
        'DunCateye': 'dun-cateye-ios',
        'ChuangMi': 'ipc-plug-ios',
        'YDCatY': 'YDCatY'
    }

    modules = {
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

    @staticmethod
    def device_git_existed(device):
        device_git = Config.modules[device]
        if device_git:
            dgs = device_git.split('/')
            folder = Config.git_co_path + dgs[len(dgs)-1].replace('.git', '')
            print(folder)
            return os.path.isdir(folder)
        return False


if __name__ == "__main__":
    print(Config.device_git_existed('SimCamCamera'))