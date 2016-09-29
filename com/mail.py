# -*- coding: utf-8 -*-
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import os
import smtplib
import getpass
import constant


def main():
    # 邮件服务器地址
    server = 'smtp.pekall.com'

    # 邮件服务器端口
    server_port = '25'

    # 邮件服务器登录账号
    user = 'tt.ss@pekall.com'

    # 发件人邮箱地址
    fro = 'tt.ss@pekall.com'

    # 收件人邮箱地址，多人用逗号分割
    to = 'sof@sina.com'

    # 邮件主题
    subject = constant.MAIL_SUBJECT

    print
    print('-------------------------发送邮件------------------------')
    try:
        pwd = getpass.getpass('输入密码: ')
        server = {'name': server, 'port': server_port, 'user': user, 'pwd': pwd}
        with open('email_content', 'r') as f:
            text = f.read()
        print subject
        print text
        msg = raw_input("确认发送邮件吗?(y/n)")
        if 'N' == str.upper(msg):
            exit(0)
        elif 'Y' == str.upper(msg):
            files = []
            send_mail(server, fro, to, subject, text, files)
    except Exception, e:
        print Exception
        print e


def send_mail(server, fro, to, subject, text, files=[]):
    msg = MIMEMultipart()
    msg['From'] = fro
    msg['Subject'] = Header(subject, 'UTF-8')
    if isinstance(to,list):
       msg['To'] = COMMASPACE.join(to)
    else:
       msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    # 可选plain,html
    msg.attach(MIMEText(text, 'plain', 'UTF-8'))

    # 发送附件
    for file1 in files:
        with open(file1, 'rb') as f:
            r = f.read()
        att = MIMEText(r, 'base64', 'UTF-8')
        att['Content-Type'] = 'application/octet-stream'
        # 设置附件头
        att.add_header("Content-Disposition", "attachment", filename=os.path.basename(file1))
        msg.attach(att)

    print("连接stmp服务器....." + server['name'] + ":" + server['port'])
    smtp = smtplib.SMTP(server['name'], server['port'])
    print("登录stmp服务器.....")
    smtp.login(server['user'], server['pwd'])
    print("发送邮件....." + str(to))
    smtp.sendmail(fro, to, msg.as_string())
    print("发送完毕.....")
    smtp.close()

main()
# python mail.py
