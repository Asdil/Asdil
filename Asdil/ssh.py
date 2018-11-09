#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     setup
   Description :
   Author :        Asdil
   date：          2018/10/26
-------------------------------------------------
   Change Activity:
                   2018/10/26:
    version = 1.7.1.1
-------------------------------------------------
"""
__author__ = 'Asdil'
import re
import paramiko

#  定义一个类，表示一台远端linux主机


class Linux(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, ip, username, password, timeout=30):
        self.ip = ip
        self.username = username
        self.password = password
        self.timeout = timeout
        # transport和chanel
        self.t = ''
        self.chan = ''
        # 链接失败的重试次数
        self.try_times = 3

    # 调用该方法连接远程主机

    def connect(self):
        while True:
            # 连接过程中可能会抛出异常，比如网络不通、链接超时
            try:
                self.t = paramiko.Transport(sock=(self.ip, 22))
                self.t.connect(username=self.username, password=self.password)
                self.chan = self.t.open_session()
                self.chan.settimeout(self.timeout)
                self.chan.get_pty()
                self.chan.invoke_shell()
                # 如果没有抛出异常说明连接成功，直接返回
                print('连接%s成功' % self.ip)
                # 接收到的网络数据解码为str
                print(self.chan.recv(65535).decode('utf-8'))
                return True
            # 这里不对可能的异常如socket.error, socket.timeout细化，直接一网打尽
            except Exception as e1:
                if self.try_times != 0:
                    print('连接%s失败，进行重试' % self.ip)
                    self.try_times -= 1
                else:
                    print('重试3次失败，结束程序')
                    return False
    # 断开连接

    def close(self):
        self.chan.close()
        self.t.close()

    # 执行命令
    def send(self, cmd, type=0):
        patten = re.compile(r'.*\r\n(.*)\r\n.*')
        cmd += '\r'
        if type == 0:
            try:
                self.chan.send(cmd)
                return True
            except:
                print('执行失败')
                return False
        else:
            try:
                self.chan.send(cmd)
                ret = self.chan.recv(65535)
                ret = ret.decode('utf-8')
                ret = patten.findall(ret)
                if ret:
                    return ret[-1]
                else:
                    print('无返回值')
                    return False
            except:
                print('执行失败')
                return False

def hp():
    print('类: Linux(pip, username, password)定义连接远程主机')
    print('函数: Linux.connect()连接主机 返回True or false')
    print('函数: Linux.close()关闭连接')
    print('函数: Linux.send(cmd， type)执行命令 type=0 无返回值')



