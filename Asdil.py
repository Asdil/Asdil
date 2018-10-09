# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Asdil
   Description :
   Author :        Asdil
   date：          2018/10/9
-------------------------------------------------
   Change Activity:
                   2018/10/9:
-------------------------------------------------
"""
__author__ = 'Asdil'
import os
import shutil
import subprocess


# 合并两个目录
def pathJoin(path1, path2):
    assert type(path1) is str
    assert type(path2) is str
    if path1[-1] != '/':
        path1 += '/'
    if path2[0] == '/':
        path2 = path2[1:]
    return path1+path2


# 执行命令行命令
def subprocessCall(cmd):
    subprocess.check_call(cmd, shell=True)


# 执行命令获取返回值
def subprocessPopen(cmd):
    subprocessCall(cmd)  # 报错用
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return [each for each in out.decode('utf8').splitlines()]


# 拆分目录
def splitPath(path):
    filePath, tmpFileName = os.path.split(path)
    fileName, extension = os.path.splitext(tmpFileName)
    return filePath, fileName, extension, tmpFileName


# 复制文件
def copyFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
        assert os.path.isfile(srcfile) is True
    else:
        fpath, fname = os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                 #创建路径
        shutil.copyfile(srcfile, dstfile)      #复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


# 剪切文件
def cutFile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
        assert os.path.isfile(srcfile) is True
    else:
        fpath, fname = os.path.split(dstfile)    # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                 # 创建路径
        shutil.move(srcfile, dstfile)          # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


# 帮助文档
def help():
    print("函数: pathJoin(path1, path2)合并文件")
    print("函数: subprocessPopen(cmd)执行shell命令")
    print("函数: subprocessCall(cmd)执行shell命令获取返回值")
    print("函数: splitPath(path)分离目录和文件")
    print("函数: copyFile(srcfile, dstfile)复制文件")
    print("函数: cutFile(srcfile,dstfile)剪切文件")




