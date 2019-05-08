# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fo
   Description :
   Author :        Asdil
   date：          2019/5/8
-------------------------------------------------
   Change Activity:
                   2019/5/8:
-------------------------------------------------
"""
__author__ = 'Asdil'
# 文件操作
import os
import shutil


# 是否是文件夹
def isDir(path):
    return os.path.isdir(path)


# 是否是文件夹
def isFile(path):
    return os.path.isfile(path)


# 是否存在该文件
def isExist(path):
    return os.path.exists(path)


# 删除文件
def delFile(path):
    flag = True
    try:
        os.remove(path)
    except:
        flag = False
    return flag


# 删除文件夹
def delDir(path):
    flag = True
    try:
        shutil.rmtree(path)
    except:
        flag = False
    return flag
