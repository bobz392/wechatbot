#!/usr/bin/python
#-*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText
from email.header import Header
 
mail_host="smtp.263.net"  
mail_user="zhoubo@sunlands.com"   
mail_pass="1397160zb"  
 
sender = 'zhoubo@sunlands.com'
receivers = ['huangyaqing@sunlands.com']  
 
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
message['From'] = Header("菜鸟教程", 'utf-8')
message['To'] =  Header("测试", 'utf-8')
 
subject = 'Python SMTP 邮件测试'
message['Subject'] = Header(subject, 'utf-8')
 
print("sending")
try:
    smtpObj = smtplib.SMTP() 
    smtpObj.debuglevel = 4
    smtpObj.connect(mail_host, 25)   
    smtpObj.login(mail_user, mail_pass)  
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException:
    print("Error: 无法发送邮件")




 
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
