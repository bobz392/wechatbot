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
                <td width="75" class="" style="border-width: 1px; border-style: none solid solid; border-color: rgb(221, 221, 221) rgb(223, 226, 229) rgb(223, 226, 229); padding: 6px 13px;">
                    <div class="" style="margin: 0px;">
                        <font color="#141414" face="SimSun" class="">
                            <span class="" style="background-color: rgb(251, 251, 251);">[!~!~!~!]</span>
                        </font>
                    </div>
                </td>
                <td width="425" class="" style="border-width: 1px; border-style: none solid solid none; border-color: rgb(221, 221, 221) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; word-break: break-all;[~~~~~~~]">
                    <div class="" style="margin: 0px;">
                        [!~~~!]
                    </div>
                </td>
                <td width="805" class="" style="border-width: 1px; border-style: none solid solid none; border-color: rgb(221, 221, 221) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px;[~~~~~~~]">
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
                        <td width="799" height="41" class="" style="border-width: 1px; border-style: solid solid solid none; border-color: rgb(223, 226, 229) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; background-color: rgb(247, 247, 247);">
                            <br class="">
                        </td>
                        <td width="419" height="41" class="" style="border-width: 1px; border-style: solid solid solid none; border-color: rgb(223, 226, 229) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; background-color: rgb(247, 247, 247);">
                            <p class="" style="margin: 0px 0px 10px; padding: 0px; text-align: center;">
                                <strong class="">
                                    <span class="" style="font-family: SimSun;">工作内容</span>
                                </strong>
                            </p>
                        </td>
                        <td width="799" height="41" class="" style="border-width: 1px; border-style: solid solid solid none; border-color: rgb(223, 226, 229) rgb(223, 226, 229) rgb(223, 226, 229) rgb(221, 221, 221); padding: 6px 13px; background-color: rgb(247, 247, 247);">
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

    def build_html(self, info):
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
        mail_user="zhoubo@sunlands.com"   
        mail_pass="qwerty123"  
        
        sender = 'zhoubo@sunlands.com'
        # 
        receivers = ['zhoubo@sunlands.com', 'huangyaqing@sunlands.com', 'zhourui@sunland.org.cn', 'yf-luonao@sunlands.com']  
        #  'huangyaqing@sunlands.com
        message = MIMEText(new_body, 'html', 'utf-8')
        message['From'] = Header(sender)
        message['To'] = Header(','.join(receivers)) 
        
        message['Subject'] = Header('【今日站报】尚研-员工平台组-iOS', 'utf-8')
        
        print("sending")
        smtpObj = smtplib.SMTP() 
        try:
            smtpObj.debuglevel = 4
            smtpObj.connect(mail_host, 25)   #465
            smtpObj.login(mail_user, mail_pass)  
            smtpObj.sendmail(sender, receivers, message.as_string())
            print('邮件发送成功')
            return u'邮件发送成功'
        except smtplib.SMTPException:
            print('邮件发送失败')
            return u'邮件发送失败'
            
                


 
# import smtplib
# import sys
# from email.mime.text import MIMEText
# from email.header import Header
 

# # 第三方 SMTP 服务
# mail_host="smtp.263.net"  #设置服务器
# mail_user="huangyaqing@sunlands.com"    #用户名
# mail_pass="hyq123579"   #口令 
 

# staff_email = "zhoubo@sunlands.com"
# hyq_email =  'huangyaqing@sunlands.com'
# purpose = staff_email

# sender = hyq_email
# receivers = [purpose]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
# argvs = sys.argv

# def sendMail(): 
# 	html = """
# 	<p>安装密码：sunlands</p>
# 	<p>变更：123123</p>
# 	<p>下载地址 <a href="http://pgyer.com/umlM">http://pgyer.com/umlM</a></p>
# 	<p>扫描二维码直接下载</p>
# 	<img src="http://www.pgyer.com/app/qrcode/umlM" />
# 	<p>此邮件不用回复</p>
# 	"""

# 	message = MIMEText(html, 'html', 'utf-8') 
# 	subject = '[发包信使]尚德企业版更新了测试包'
# 	message['Subject'] = Header(subject, 'utf-8') 
# 	message['From'] = Header(hyq_email) 
# 	message['To'] = Header(','.join(receivers)) 
	 
# 	try:
# 	    smtpObj = smtplib.SMTP() 
# 	    smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
# 	    smtpObj.login(mail_user, mail_pass)  
# 	    smtpObj.sendmail(sender, receivers, message.as_string())
# 	    print("邮件发送成功")
# 	except smtplib.SMTPException:
# 	    print("Error: 无法发送邮件") 

# print(len(sys.argv))
# print(sys.argv)

# # gitSource = argvs[1]
# # changelog = "暂无"
# # if len(argvs)>=2:
# # 	changelog = argvs[2]

# sendMail()