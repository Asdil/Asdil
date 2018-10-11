# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Asdil
   Description :
   Author :        Asdil
   date：          2018/10/9
-------------------------------------------------
   Change Activity:
                   2018/10/10:
    version = 0.5
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
    assert type(path) is str
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


# 修改Txt文件
def reWriteTxt(filePath, key, newstr):
    # 读取
    content = ""
    with open(filePath, "r", encoding="utf-8") as f:
        for line in f:
            if key in line:
                line = newstr + '\n'
            content += line
    # 写入
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(content)


# 列表交集
def interSet(l1, l2):
    assert type(l1) is list
    assert type(l2) is list
    return list(set(l1).intersection(set(l2)))


# 列表差集
def diffSet(l1, l2):
    assert type(l1) is list
    assert type(l2) is list
    return list(set(l1).difference(set(l2)))


# 并集
def unionSet(l1, l2):
    assert type(l1) is list
    assert type(l2) is list
    return list(set(l1).union(set(l2)))


# 检查文件夹是否存在，如果存在则删除重新创建
def createDir(path):
    """
    :param path:    文件夹路径
    :param type:    文件夹不存在是否报错  True报错， False不报错,并创建文件夹
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    return False

# 合并字典
def combinDic(*args):
    ret = {}
    if len(args) == 1:
        dicts = args[0]
        assert type(dicts) is list  # 断言是个列表
        for _dict in dicts:
            ret = dict(ret, **_dict)
    else:
        for _dict in args:
            assert type(_dict) is dict
        for _dict in args:
            ret = dict(ret, **_dict)
    return ret


# 帮助文档
def hp():
    print("函数: pathJoin(path1, path2)合并文件")
    print("函数: subprocessPopen(cmd)执行shell命令")
    print("函数: subprocessCall(cmd)执行shell命令获取返回值")
    print("函数: splitPath(path)分离目录和文件")
    print("函数: copyFile(srcfile, dstfile)复制文件")
    print("函数: cutFile(srcfile,dstfile)剪切文件")

    print("函数: reWriteTxt(filePath, key, newstr) 修改文件")
    print("函数: interSet(l1, l2) list去交集")
    print("函数: diffSet(l1, l2)  list取差集")
    print("函数: unionSet(l1, l2) list取并集")
    print("函数: createDir(path)  创建文件夹")
    print("函数: combinDic(*args)  合并多个字典合 ([dict, dict]) 或者(dict, dict)")

help()