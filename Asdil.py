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
    version = 1.0.2
-------------------------------------------------
"""
__author__ = 'Asdil'
import os
import shutil
import subprocess
import zipfile

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

# 删除目录
def delDir(path):
    shutil.rmtree(path)

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


# 拆分列表
def splitList(_list, slice):
    """
    :param _list:  列表
    :param slice:  拆分块的大小
    :return:       拆分后的列表
    """
    return [_list[i:i + slice] for i in range(0, len(_list), slice)]

# 压缩文件
def zipFile(file_path, output = None, rename = None):
    """
    :param file_path:  文件绝对路径
    :param output:     是否输入到其它文件夹
    :return:           True, False
    """
    # 拆分成文件路径，文件
    path, name, _, name_extension = splitPath(file_path)
    if rename is None:
        rename = name

    if output is None:
        output = path
    azip = zipfile.ZipFile(pathJoin(output, rename + '.zip'), 'w')
    # 写入zip
    azip.write(file_path, name_extension, compress_type=zipfile.ZIP_DEFLATED)
    azip.close()
    print("{} -> {}".format(file_path, pathJoin(output, rename + '.zip')))

# 解压文件
def unzipFile(file_path):
    """
    :param file_path:  zip文件完整路径
    :return:
    """
    _, _, _, name_extension = splitPath(file_path)
    azip = zipfile.ZipFile(file_path)
    azip.namelist()
    azip.close()
    print("{} ->> {}".format(file_path, file_path[:-4]))

# 压缩文件夹
def zipDir(file_dir, output=None, rename=None):
    """
    :param file_dir:  文件夹路径
    :param output:    输出路径
    :param rename:    重命名
    :return:
    """
    if rename is None:
        tmp = file_dir.strip('/')
        dirs = tmp.strip('/').split('/')
        rename = dirs[-1]
    # 压缩文件夹
    if output is None:
        output = '/' + '/'.join(dirs[:-1])
        print(pathJoin(output, rename))
        shutil.make_archive(pathJoin(output, rename), 'zip', file_dir)
    else:
        shutil.make_archive(pathJoin(output, rename), 'zip', file_dir)
    print("{} -> {}".format(file_dir, pathJoin(output, rename)+'.zip'))

# 解压文件夹
def unzipDir(file_dir, output=None, rename=None):
    """
    :param file_dir:  解压文件夹
    :return:
    """
    path, name, _, _ = splitPath(file_dir)
    if output is None:
        output = path
    if rename is None:
        rename = name
    output = pathJoin(output, rename)

    shutil.unpack_archive(file_dir, output)
    print('{} ->> {}'.format(file_dir, output))



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
    print("函数: delDir(path)     删除文件夹")
    print("函数: combinDic(*args)  合并多个字典合 ([dict, dict]) 或者(dict, dict)")
    print("函数: splitList(_list, slice)  列表按照每块slice大小拆分")
    print("函数: zipFile(file_path, output, rename)  压缩文件(zip)")
    print("函数: unzipFile(file_path)   解压文件(zip)")
    print("函数: zipDir(file_dir, output, rename)  压缩文件夹(zip)")
    print("函数: unzipDir(file_dir, output, rename) 解压文件夹(zip)")




