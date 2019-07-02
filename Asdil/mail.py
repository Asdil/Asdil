# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     email
   Description :
   Author :        Asdil
   date：          2018/11/14
-------------------------------------------------
   Change Activity:
                   2018/11/14:
-------------------------------------------------
"""
__author__ = 'Asdil'
import re
from mailthon import postman, email


class Mail():
    def __init__(self, host, address, pwd):
        """
        :param host:     POP3/IMAP/SMTP/Exchange服务
        :param address:  邮箱地址
        :param pwd:      授权码wtqngyeotfiybhii
        """
        flag, name = self._check(address)
        if not flag:
            print('邮箱格式不合法')
            assert 1 == 2
        self.p = postman(host=host, auth=(address, pwd))
        self.address = address
        self.name = name
        self.ok = None

    def _check(self, address):
        re_email = re.compile("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$")
        if re_email.match(address):
            m = re.match(r'^([a-zA-Z\.0-9]+)@[a-zA-Z0-9]+\.[a-zA-Z]{3}$', address)
            return True, m.group(1)
        return False, None

    def send(self, content, to, subject='提示信息'):
        flag, _ = self._check(to)
        if not flag:
            print('邮箱格式不合法')
            assert 1 == 2

        content = content.replace('\n', '<br>')
        content = '<p>' + content + '<p>'
        r = self.p.send(email(
            content=content,
            subject=subject,
            sender='{} <{}>'.format(self.name, self.address),
            receivers=[to],
        ))
        if not r.ok:
            print('发送失败')
            self.ok = False
        else:
            self.ok = True
def hp():
    print('Mail(host, address, pwd) 初始化')
    print('send(content, to, subject) 发送邮件返回bool')
    print("""example: \np = Mail('smtp.qq.com', 'xxx@qq.com', 'xxx')\np.send('测试邮件', 'yyy@126.com', '程序运行提示')""")
