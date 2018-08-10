#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-

import smtplib

from email.mime.text import MIMEText
from email.header import Header
from model import Message, User, Report


class Mail(object):
    """
    邮件发送的基类。
    定义了一些替换符号和发送的实际逻辑。
    """
    content_replacement = u'[!~~~!]'
    name_replacement = u'[!~!~!~!]'
    color_replacement = u'[~~~~~~~]'

    def __init__(self):
        self.subject = None
        self.receivers = []
        self.sender_from = None
        self.sender_password = None

    def send(self, mail_body):
        if self.receivers and self.sender_from \
                and self.sender_password:
            mail_host="smtp.263.net"
            message = MIMEText(mail_body, 'html', 'utf-8')
            message['From'] = Header(self.sender_from)
            message['To'] = Header(','.join(self.receivers)) 
            if self.subject:
                message['Subject'] = Header(self.subject, 'utf-8')
            
            smtp = smtplib.SMTP() 
            try:
                smtp.debuglevel = 4
                smtp.connect(mail_host, 25)   #465
                smtp.login(self.sender_from, self.sender_password)  
                smtp.sendmail(self.sender_from, self.receivers, message.as_string())
                return u'邮件发送成功\n'
            except smtplib.SMTPException:
                return u'邮件发送失败\n'
        else:
            return u'邮件发送者或者接收者没有填写'

class DailyMail(Mail):
    """
    每日站报的 mail 发送。
    """
    def __init__(self):
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

    def build_daily_report_html(self, info, \
        sender='zhoubo@sunlands.com', pwd='qwerty123', empty_holder=None):
        trs = u''
        print('%s, %s' % (sender, pwd))
        user_idx = 0
        for user, messages in info.items():
            divs = u''
            
            for index, message in enumerate(messages):
                new_div = self.div
                dst = u'%d、%s' % (index + 1, message.message)
                new_div = new_div.replace(self.content_replacement, dst)
                divs += new_div

            if not divs and empty_holder:
                new_div = self.div
                new_div = new_div.replace(self.content_replacement, empty_holder)
                divs = new_div

            new_tr = self.tr
            new_tr = new_tr.replace(self.name_replacement, user)
            new_tr = new_tr.replace(self.content_replacement, divs)
            if (user_idx % 2) == 0:
                new_tr = new_tr.replace(self.color_replacement, u'')
            else:
                new_tr = new_tr.replace(self.color_replacement, self.highlight)
            
            trs += new_tr
            user_idx += 1
            
        mail_body = self.body
        mail_body = mail_body.replace(self.content_replacement, trs)
        self.receivers = ['yf-sunwei@sunlands.com', 'rd-staff.list@sunlands.com']
        self.subject = '【今日站报】尚研-员工平台组-iOS'
        self.sender_from = sender
        self.sender_password = pwd
        return self.send(mail_body)


class WeeklyMail(Mail):
    """
    周报的构建 class
    """

    def __init__(self):

        self.content_header_replacement = u'[~~!header!~~]'
        self.content_body_replacement = u'[~~!body!~~]'
        self.weekly_finish_replacement = u'[~~!weekly_finish!~~]'
        self.weekly_todo_replacement = u'[~~!weekly_todo!~~]'

        self.reporter_name_replacement = u'[~~!weekly_name!~~]'
        self.weekly_description_replacement = u'[~~!weekly_description!~~]'
        self.weekly_title_replacement = u'[~~!weekly_title!~~]'
        self.weekly_date_replacement = u'[~~!weekly_date!~~]'
        
        self.content_header_p = u'''
                <p style="font-size: 16px;font-family: 宋体">
                    <span style="font-size: 18px;color: rgb(51, 51, 51)">[~~!header!~~]</span>
                </p>'''
        self.content_body_p = u'''
                <p class="MsoListParagraph" style="margin-left: 32px">
                    <span style="font-size:14px;font-family:Wingdings">Ø<span style="font-variant-numeric: normal;font-variant-east-asian: normal;font-stretch: normal;font-size: 9px;line-height: normal;font-family: &#39;Times New Roman&#39;">&nbsp;&nbsp; </span></span><span style="font-size:14px;font-family:SimSun">[~~!body!~~]</span>
                </p>'''

        self.report_template_path = r'report_template.html'
        self.receivers = ['yf-sunwei@sunlands.com', 'rd-staff.list@sunlands.com']
        

    def build_weekly_report_html(self, sender):
        with open(self.report_template_path, 'r') as f:
            html = unicode(f.read(), "utf-8")
            user = User.query_user(sender)
            report = Report.query_weekly_report(sender)

            if user and report:
                week_duration = Report.week_date_duration()
                html = html.replace(self.reporter_name_replacement, user.realname)
                html = html.replace(self.weekly_title_replacement, report.project_title)
                html = html.replace(self.weekly_description_replacement, report.description)
                html = html.replace(self.weekly_date_replacement, week_duration)
                contents = report.origin_report.splitlines()

                self.subject = u'工作周报-%s-技术-尚武研-员工平台-iOS-%s' \
                    % (user.realname, week_duration)
                self.sender_from = user.email
                self.sender_password = user.password

                finish_contents = u''
                for content in contents:
                    if content.startswith('-'):
                        header = self.content_header_p
                        header = header.replace(self.content_header_replacement, \
                            u'%s' % content[1:])
                        finish_contents += header
                    else:
                        body = self.content_body_p
                        body = body.replace(self.content_body_replacement, content)
                        finish_contents += body
                html = html.replace(self.weekly_finish_replacement, finish_contents)
                todo_texts = report.next_week_todo.split(u'，')

                next_week_todo = u''
                for todo in todo_texts:
                    new_todo = self.content_body_p
                    new_todo = new_todo.replace(self.content_body_replacement, todo)
                    next_week_todo += new_todo
                html = html.replace(self.weekly_todo_replacement, next_week_todo)
                return self.send(html)
            else:
                return u'用户 %s 不存在或者本周周报还未生成' % sender
