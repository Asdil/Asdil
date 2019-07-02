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
from Asdil import tool


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


# 删除目录下所有文件
def delAllFiles(path, key=None):
    if key == None:
        files = tool.getFiles(path)
    else:
        files = tool.getFiles(path, key=key)
    for _file in files:
        if isFile(_file):
            delFile(_file)
        else:
            delDir(_file)
    return True


# 拷贝目录下所有文件
def copyAllFiles(srcfile, dstfile, key=None, isreplace=False):
    if key is None:
        files = tool.getFiles(srcfile)
    else:
        files = tool.getFiles(srcfile, key=key)
    if isreplace:
        for _file in files:
            if isFile(_file):
                _, _, _, name = tool.splitPath(_file)
                if isExist(_file):
                    delFile(tool.pathJoin(dstfile, name))
                tool.copyFile(_file, dstfile)
            else:
                _, _, _, name = tool.splitPath(_file)
                if isExist(_file):
                    delDir(tool.pathJoin(dstfile, name))
                shutil.copytree(_file, dstfile + f'/{name}')
    else:
        for _file in files:
            if isFile(_file):
                tool.copyFile(_file, dstfile)
            else:
                _,_,_,name = tool.splitPath(_file)
                shutil.copytree(_file, dstfile+f'/{name}')


# 拷贝目录下所有文件
def cutAllFiles(srcfile, dstfile, key=None, isreplace=False):
    if key is None:
        files = tool.getFiles(srcfile)
    else:
        files = tool.getFiles(srcfile, key=key)
    if isreplace:
        for _file in files:
            if isFile(_file):
                _, _, _, name = tool.splitPath(_file)
                if isExist(_file):
                    delFile(tool.pathJoin(dstfile, name))
                tool.cutFile(_file, dstfile)
            else:
                _, _, _, name = tool.splitPath(_file)
                if isExist(_file):
                    delDir(tool.pathJoin(dstfile, name))
                shutil.move(_file, dstfile + f'/{name}')
                print(f'copy {_file} -> dstfile/{name}')
    else:
        for _file in files:
            if isFile(_file):
                tool.cutFile(_file, dstfile)
            else:
                _,_,_,name = tool.splitPath(_file)
                shutil.move(_file, dstfile+f'/{name}')
                print(f'copy {_file} -> dstfile/{name}')


# 拷贝目录下所有文件
def cutAllFiles(srcfile, dstfile, key=None, isreplace=False):
    if key is None:
        files = tool.getFiles(srcfile)
    else:
        files = tool.getFiles(srcfile, key=key)
    if isreplace:
        for _file in files:
            if isFile(_file):
                _, _, _, name = tool.splitPath(_file)
                if isExist(_file):
                    delFile(tool.pathJoin(dstfile, name))
                tool.cutFile(_file, dstfile)
            else:
                _, _, _, name = tool.splitPath(_file)
                if isExist(_file):
                    delDir(tool.pathJoin(dstfile, name))
                shutil.move(_file, dstfile + f'/{name}')
                print(f'cut {_file} -> dstfile/{name}')
    else:
        for _file in files:
            if isFile(_file):
                tool.cutFile(_file, dstfile)
            else:
                _,_,_,name = tool.splitPath(_file)
                shutil.move(_file, dstfile+f'/{name}')
                print(f'cut {_file} -> dstfile/{name}')
