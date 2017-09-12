#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import *

def send_mail(mail_text):
    mail_server = 'smtp.sina.com'
    mail_server_port = 465

    mail_user = 'silas_stock@sina.com'
    mail_pass = 'stock1234'
    from_addr = 'silas_stock@sina.com'
    #to_addr = ['bochuaned@163.com','lewang@dccsh.icbc.com.cn','hjqin@dccsh.icbc.com.cn'] #to_addr可放入多个邮箱，以逗号隔开
    to_addr = ['bochuaned@163.com']
    #发送邮件形式和内容
    msg = MIMEText(mail_text,'html','utf-8')
    msg['From'] = 'silas_stock@sina.com'
    msg['To'] = Header('stock group','utf-8')
    #发送主题
    subject = datetime.now().strftime("%Y-%m-%d") + "行情分析"
    msg['Subject'] = Header(subject,'utf-8')
    try:
        smtp = smtplib.SMTP_SSL(mail_server,mail_server_port)
        smtp.login(mail_user,mail_pass)
        smtp.sendmail(from_addr,to_addr,msg.as_string())
        smtp.quit()
        print('邮件发送成功')
    except smtplib.SMTPException,e:
        print e
        print('Error:邮件发送失败！！！')