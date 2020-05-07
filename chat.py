#! /usr/bin/env python2.7
# coding=utf-8

import requests
import hashlib
import urllib
# import urllib2
import base64
import json
import time


class TencentChat(object):

    def __init__(self):
        api_key = 'WLkqnOl9uw0pi3Hu'
        api_id = 2115758591
        self.apiplat = AiPlat(api_id, api_key)

    def request(self, text):
        self.apiplat.data.clear()
        str_text = text.encode('UTF-8')
        print('request ' + str_text)
        _type = 1
        rsp = self.apiplat.getNlpTextTrans(str_text, _type)
        if rsp['ret'] == 0:
            print(json.dumps(rsp, encoding="UTF-8",
                             ensure_ascii=False, sort_keys=False, indent=4))
            print('----------------------API SUCC----------------------')
            return unicode(rsp['data']['answer'])
        else:
            print(json.dumps(rsp, encoding="UTF-8",
                             ensure_ascii=False, sort_keys=False, indent=4))

            print('----------------------API FAIL----------------------')
            return None


def genSignString(parser):
    uri_str = ''

    for key in sorted(parser.keys()):
        uri_str += "%s=%s&" % (key, urllib.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=WLkqnOl9uw0pi3Hu'
    print(sign_str)

    hash_md5 = hashlib.md5(sign_str)
    return hash_md5.hexdigest().upper()


url_preffix = 'https://api.ai.qq.com/fcgi-bin/'


class AiPlat(object):
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.data = {}

    def invoke(self, params):
        self.url_data = urllib.encode(params)
        req = urllib.Request(self.url, self.url_data)
        try:
            rsp = urllib.urlopen(req)
            str_rsp = rsp.read()
            dict_rsp = json.loads(str_rsp)
            return dict_rsp
        except urllib.URLError as e:
            dict_error = {}
            if hasattr(e, "code"):
                dict_error = {}
                dict_error['ret'] = -1
                dict_error['httpcode'] = e.code
                dict_error['msg'] = "sdk http post err"
                return dict_error
            if hasattr(e, "reason"):
                dict_error['msg'] = 'sdk http post err'
                dict_error['httpcode'] = -1
                dict_error['ret'] = -1
                return dict_error
        else:
            dict_error = {}
            dict_error['ret'] = -1
            dict_error['httpcode'] = -1
            dict_error['msg'] = "system error"
            return dict_error

    def set_params(self, key, value):
        self.data[key] = value

    def getNlpTextTrans(self, text, type):
        self.url = url_preffix + 'nlp/nlp_textchat'
        self.set_params('app_id', self.app_id)
        self.set_params('session', '%d' % int(time.time()))
        self.set_params('question', text)
        self.set_params('time_stamp', int(time.time()))
        self.set_params('nonce_str', '%d' % int(time.time()))
        sign_str = genSignString(self.data)
        self.set_params('sign', sign_str)
        print(self.data)
        return self.invoke(self.data)


if __name__ == '__main__':
    str_text = u'@ALEX 你叫啥'
    str_text = str_text.replace(u'@ALEX ', u'')
    print(type(str_text))
    print(str_text.encode('utf8') == '你叫啥')
    print(str_text == u'你叫啥')
    chat = TencentChat()
    s = chat.request(str_text)
    print(s)
