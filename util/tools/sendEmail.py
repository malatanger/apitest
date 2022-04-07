# coding:utf-8
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from config.confManage import mail_manage
from scripts.log import Log

Log()


def send_email(title, url):
    # 第三方 SMTP 服务

    mail_host = mail_manage(ml='${mail_host}$')  # 设置服务器
    mail_user = mail_manage(ml='${mail_user}$')  # 用户名
    mail_pass = mail_manage(ml='${mail_pass}$')  # 口令
    sender = mail_manage(ml='${sender}$')
    receivers = mail_manage(ml='${receivers}$')  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_msg = """
    <p>测试报告发送</p>
    <p><a href="{}">点我查看测试报告</a></p>
    """.format(url)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("13688400244@sina.cn", )
    message['To'] = Header("井松", 'utf-8')

    message['Subject'] = Header(title, 'utf-8')
    try:
        logging.debug("初始化邮件服务..")
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        logging.debug("发送邮件中..")
        smtpObj.sendmail(sender, receivers, message.as_string())
        logging.debug("邮件发送成功")
    except:
        raise


if __name__ == '__main__':
    send_email("报告", "https://www.runoob.com/")
