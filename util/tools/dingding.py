# coding:utf-8
# @Time    : 2021/9/2 11:46 PM
# @Author  : 余少琪
# @FileName: dingding.py
# @email   : 1603453211@qq.com


import base64
import hashlib
import hmac
import time
import urllib.parse

from dingtalkchatbot.chatbot import DingtalkChatbot, FeedLink

from config.confManage import dingding_manage


class DingTalkSendMsg(object):

    def __init__(self):
        self.timestap = str(round(time.time() * 1000))
        self.sign = self.get_sign()
        self.webhook = dingding_manage("${webhook}$") + "&timestamp=" + self.timestap + "&sign=" + self.sign
        self.xiaoding = DingtalkChatbot(self.webhook)

    def get_sign(self):
        """
        根据时间戳 + sgin 生成密钥
        :return:
        """
        secret = dingding_manage("${secret}$")
        string_to_sign = '{}\n{}'.format(self.timestap, secret).encode('utf-8')
        hmac_code = hmac.new(secret.encode('utf-8'), string_to_sign, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return sign

    def send_text(self, msg, mobiles=None):
        """
        发送文本信息
        :param msg: 文本内容
        :param mobiles: 艾特用户电话
        :return:
        """
        if not mobiles:
            self.xiaoding.send_text(msg=msg, is_at_all=True)
        else:
            if isinstance(mobiles, list):
                self.xiaoding.send_text(msg=msg, at_mobiles=mobiles)
            else:
                raise TypeError("mobiles类型错误 不是list类型.")

    def send_link(self, title, text, message_url, pic_url):
        """
        发送link通知
        :return:
        """
        try:
            self.xiaoding.send_link(title=title, text=text, message_url=message_url, pic_url=pic_url)
        except Exception:
            raise

    def send_markdown(self, title, msg, mobiles=None):
        """

        :param mobiles:
        :param title:
        :param msg:
        markdown 格式
        '#### 自动化测试报告\n'
            '> ' + str(msg) + '\n\n'
                            '> ![图片](https://img1.baidu.com/it/u'
                            '=424332266,'
                            '2532715190&fm=26&fmt=auto&gp=0.jpg)\n '
                            '> ###### ' + get_now_time() +
            '[测试报告](https://blog.csdn.net/weixin_43865008/article'
            '/details/120079270?spm=1001.2014.3001.5501) \n'
        :return:
        """
        if not mobiles:
            self.xiaoding.send_markdown(title=title, text=msg, is_at_all=True)
        if isinstance(mobiles, list):
            self.xiaoding.send_markdown(title=title, text=msg, at_mobiles=mobiles)
        else:
            raise TypeError("mobiles类型错误 不是list类型.")

    @staticmethod
    def feed_link(title, message_url, pic_url):

        return FeedLink(title=title, message_url=message_url, pic_url=pic_url)

    def send_feed_link(self, *arg):
        try:
            self.xiaoding.send_feed_card(list(arg))
        except Exception:
            raise


if __name__ == '__main__':
    #     title = '自动化测试', text = '自动化测试报告',
    #     message_url = 'https://blog.csdn.net/weixin_43865008/article/details/120079270?spm=1001'
    #     '.2014.3001.5501',
    # pic_url = "https://img2.baidu.com/it/u=841211112,1898579033&fm=26&fmt=auto&gp=0.jpg"

    d = DingTalkSendMsg()
    a = d.feed_link("1", message_url='https://blog.csdn.net/weixin_43865008/article/details/120079270?spm=1001',
                    pic_url="https://img2.baidu.com/it/u=841211112,1898579033&fm=26&fmt=auto&gp=0.jpg")
    b = d.feed_link("2", message_url='https://blog.csdn.net/weixin_43865008/article/details/120079270?spm=1001',
                    pic_url="https://img2.baidu.com/it/u=841211112,1898579033&fm=26&fmt=auto&gp=0.jpg")
    d.send_feed_link(a, b)

    d.send_text("3", [13688400244])
