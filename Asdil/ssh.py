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
    version = 1.7.1.7
-------------------------------------------------
"""
__author__ = 'Asdil'
import os
import re
import paramiko
from paramiko import SSHClient
from scp import SCPClient
from Asdil import log
from Asdil import tool
import shutil
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


class Scp:
    def __init__(self, ip, name, pwd, port=22, log_path=None):
        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # 修复
        self.ssh.connect(ip,
                    port=port,
                    username=name,
                    password=pwd)
        self.ip_name = '{}@{}:'.format(str(name), ip)
        self.log = False
        self.log_path = log_path
        if log_path is not None:
            self.log = True
            log.alter_log_ini(log_path)

    def putFile(self, file_path, remote_path, iscut=False):
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)

        scp = SCPClient(self.ssh.get_transport())
        if not os.path.exists(file_path):
            print(f'{file_path} 文件不存在')
            if self.log:
                logger.info(f'{file_path} 文件不存在')

        _, _, _, file_name = tool.splitPath(file_path)
        _, _, _, remote_name = tool.splitPath(remote_path)

        # 可以只是文件夹路径
        if remote_name != file_name:
            remote_path = tool.pathJoin(remote_path, file_name)

        scp.put(file_path, remote_path)
        scp.close()

        if iscut:
            os.remove(file_path)
        print(f'{file_path} -----> {self.ip_name}{remote_path}')
        if self.log:
            logger.info(f'{file_path} -----> {self.ip_name}{remote_path}')

    def putDir(self, file_path, remote_path, iscut=False):
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)

        scp = SCPClient(self.ssh.get_transport())
        if not os.path.exists(file_path):
            print(f'{file_path} 文件夹不存在')
            if self.log:
                logger.info(f'{file_path} 文件夹不存在')

        scp.put(file_path, recursive=True, remote_path=remote_path)
        scp.close()

        if iscut:
            shutil.rmtree(file_path)
        print(f'{file_path} -----> {self.ip_name}{remote_path}')
        if self.log:
            logger.info(f'{file_path} -----> {self.ip_name}{remote_path}')

    def getFile(self, file_path, remote_path):
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)
        scp = SCPClient(self.ssh.get_transport())
        _, _, _, file_name = tool.splitPath(file_path)
        _, _, _, remote_name = tool.splitPath(remote_path)
        # 可以只是文件夹路径
        if remote_name != file_name:
            remote_path = tool.pathJoin(remote_path, file_name)
        scp.get(file_path, remote_path)
        scp.close()
        print(f'{self.ip_name}{file_path} -----> {remote_path}')
        if self.log:
            logger.info(f'{self.ip_name}{file_path} -----> {remote_path}')

    def getDir(self, file_path, remote_path):
        logger = None
        if self.log:
            logger = log.init_log(self.log_path)
        scp = SCPClient(self.ssh.get_transport())
        scp.get(file_path, remote_path, recursive=True)
        scp.close()
        print(f'{self.ip_name}{file_path} -----> {remote_path}')
        if self.log:
            logger.info(f'{self.ip_name}{file_path} -----> {remote_path}')

def hp():
    print('类: Linux(pip, username, password)定义连接远程主机')
    print('函数: Linux.connect()连接主机 返回True or false')
    print('函数: Linux.close()关闭连接')
    print('函数: Linux.send(cmd， type)执行命令 type=0 无返回值')

    print('类: Scp(ip, name, pwd, port=22, log_path=None) 上传下载文件')
    print('函数: Scp.putFile(file_path, remote_path) 上传文件到主机')
    print("scp.putFile('/tmp/bb/ee.txt', '/data7/imputeData/tmp')")
    print('函数: Scp.putDir(file_path, remote_path) 上传文件夹到主机')
    print("scp.putDir('/tmp/bb', '/data7/imputeData/tmp')")
    print('函数: Scp.getFile(file_path, remote_path) 下载文件夹到主机')
    print("scp.getFile('/data7/imputeData/tmp/aa/1.txt', '/tmp')")
    print('函数: Scp.getDir(file_path, remote_path) 下载文件到主机')
    print("scp.getDir('/data7/imputeData/tmp/aa/', '/tmp')")
