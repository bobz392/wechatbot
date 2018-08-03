#!/usr/bin/python
#-*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText
from email.header import Header
from model import Message

class Mail(object):
    
    def __init__(self, *args, **kwargs):
        self.replacement = u'[!~~~!]'
        self.name_replacement = u'[!~!~!~!]'
        self.color_replacement = u'[~~~~~~~]'

        self.highlight = u'background-color: rgb(246, 248, 250);'

        self.tr = u'''
            <tr class="">
                <td width="15" class="" style="border-width: 1px; border-style: none solid solid; border-color: rgb(221, 221, 221) rgb(223, 226, 229) rgb(223, 226, 229); padding: 6px 13px;">
                    <div class="" style="margin: 0px;">
                        <font color="#141414" face="SimSun" class="">
                            <span class="" style="background-color: rgb(251, 251, 251);">[!~!~!~!]</span>
                        </font>
                    </div>
                </td>
                <td width="805" class="" style="border-width: 1px; border-style: none solid solid none; border-color: rgb(221, 221, 221) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; word-break: break-all;[~~~~~~~]">
                    <div class="" style="margin: 0px;">
                        [!~~~!]
                    </div>
                </td>
                <td width="425" class="" style="border-width: 1px; border-style: none solid solid none; border-color: rgb(221, 221, 221) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px;[~~~~~~~]">
                    <br class="">
                </td>
            </tr>
        '''

        self.div = u'<div class="" style="margin: 0px; font-stretch: normal; font-size: 13px; line-height: normal; font-family: &quot;Helvetica Neue&quot;;">[!~~~!]</div>'

        self.body = u'''
        <div>
            <h3>【今日站报】尚研-员工平台组-iOS</h3>
            <table class="customTableClassName" cellspacing="0" cellpadding="0" style="margin-bottom: 10px; border-collapse: collapse; caret-color: rgb(51, 51, 51); color: rgb(51, 51, 51); font-family: verdana, Tahoma, Arial, 宋体, sans-serif; font-size: 14px; text-size-adjust: auto;">
                <thead class="">
                    <tr class="firstRow" style="height: 41px;">
                        <td width="319" height="41" class="" style="border-width: 1px; border-style: solid solid solid none; border-color: rgb(223, 226, 229) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; background-color: rgb(247, 247, 247);">
                            <br class="">
                        </td>
                        <td width="799" height="41" class="" style="border-width: 1px; border-style: solid solid solid none; border-color: rgb(223, 226, 229) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; background-color: rgb(247, 247, 247);">
                            <p class="" style="margin: 0px 0px 10px; padding: 0px; text-align: center;">
                                <strong class="">
                                    <span class="" style="font-family: SimSun;">工作内容</span>
                                </strong>
                            </p>
                        </td>
                        <td width="319" height="41" class="" style="border-width: 1px; border-style: solid solid solid none; border-color: rgb(223, 226, 229) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; background-color: rgb(247, 247, 247);">
                            <p class="" style="margin: 0px 0px 10px; padding: 0px; text-align: center;">
                                <strong class="">
                                    <span class="" style="font-family: SimSun;">问题</span>
                                </strong>
                            </p>
                        </td>
                    </tr>
                </thead>
                <tbody class="">
                    [!~~~!]
                </tbody>
            </table>
            <br />
            <div id="write-custom-companySignature" class="" style="caret-color: rgb(51, 51, 51); color: rgb(51, 51, 51); font-family: verdana, Tahoma, Arial, 宋体, sans-serif; text-size-adjust: auto;">
                <pre class="" style="line-height: normal; font-variant-east-asian: normal;">[Object&nbsp;Object]<br /><br />职业培训领跑者！</pre>
                <pre class="" style="line-height: normal; font-variant-east-asian: normal;">学习是一种信仰！</pre>
            </div>
        </div>
        ''' 

    def build_daily_report_html(self, info, sender='zhoubo@sunlands.com', pwd='qwerty123'):
        trs = u''
        user_idx = 0
        for user, messages in info.items():
            divs = u''
            
            for index, message in enumerate(messages):
                new_div = self.div
                dst = u'%d、%s' % (index + 1, message.message)
                new_div = new_div.replace(self.replacement, dst)
                divs += new_div

            new_tr = self.tr
            new_tr = new_tr.replace(self.name_replacement, user)
            new_tr = new_tr.replace(self.replacement, divs)
            if (user_idx % 2) == 0:
                new_tr = new_tr.replace(self.color_replacement, u'')
            else:
                new_tr = new_tr.replace(self.color_replacement, self.highlight)
            
            trs += new_tr
            user_idx += 1
            
        new_body = self.body
        new_body = new_body.replace(self.replacement, trs)

        mail_host="smtp.263.net"

        receivers = ['yf-sunwei@sunlands.com', 'rd-staff.list@sunlands.com']  
# 'zhoubo@sunlands.com', 'huangyaqing@sunlands.com', 'zhourui@sunland.org.cn', 'yf-luonao@sunlands.com'
        message = MIMEText(new_body, 'html', 'utf-8')
        message['From'] = Header(sender)
        message['To'] = Header(','.join(receivers)) 
        
        message['Subject'] = Header('【今日站报】尚研-员工平台组-iOS', 'utf-8')
        
        smtpObj = smtplib.SMTP() 
        try:
            smtpObj.debuglevel = 4
            smtpObj.connect(mail_host, 25)   #465
            smtpObj.login(sender, pwd)  
            smtpObj.sendmail(sender, receivers, message.as_string())
            return u'邮件发送成功\n'
        except smtplib.SMTPException:
            return u'邮件发送失败\n'
