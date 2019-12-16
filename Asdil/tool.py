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
                   2019/5/21:
    version = 1.7.2.9
-------------------------------------------------
"""
__author__ = 'Asdil'
import os
import shutil
import subprocess
import zipfile
import gzip
#from progressbar import progressbar
from tqdm import tqdm
import psutil
import time

# 获取目标目录文件
def getFiles(path, extension=None, key=None):
    if extension is not None:
        l = -len(extension)
        ret = [pathJoin(path, each) for each in os.listdir(path) if each[l:] == extension]
    elif key is not None:
        ret = [pathJoin(path, each) for each in os.listdir(path) if key in each]
    else:
        ret = [pathJoin(path, each) for each in os.listdir(path)]
    return ret

# 获取文件名
def getNames(path, extension=None, key=None):
    if extension is not None:
        l = -len(extension)
        ret = [each for each in os.listdir(path) if each[l:] == extension]
    elif key is not None:
        ret = [each for each in os.listdir(path) if key in each]
    else:
        ret = [each for each in os.listdir(path)]
    return ret

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
def subprocessCheckAll(cmd):
    subprocess.check_call(cmd, shell=True)

def subprocessCall(cmd):
    subprocess.call(cmd, shell=True)

# 执行命令获取返回值
def subprocessPopen(cmd):
    #subprocessCall(cmd)  # 报错用
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
        _, _, _, name = splitPath(srcfile)
        if dstfile[-len(name):] == name:
            fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        else:
            fpath = dstfile

        if not os.path.exists(fpath):
            os.makedirs(fpath)  # 创建路径

        dstfile = pathJoin(fpath, name)
        shutil.copyfile(srcfile, dstfile)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstfile))


# 剪切文件
def cutFile(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!" % srcfile)
        assert os.path.isfile(srcfile) is True
    else:
        fpath, fname = os.path.split(dstfile)    # 分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                 # 创建路径
        shutil.move(srcfile, dstfile)          # 复制文件
        print("cut %s -> %s" % (srcfile, dstfile))


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

# 字典累加
def add_dic(dica, dicb):
    """
    :param dica:   字典a
    :param dicb:   字典b
    :return:       字典累加
    """
    dic = {}
    for key in dica:
        if dicb.get(key):
            dic[key] = dica[key] + dicb[key]
        else:
            dic[key] = dica[key]
    for key in dicb:
        if dica.get(key):
            pass
        else:
            dic[key] = dicb[key]
    return dic


# 拆分列表
def splitList(_list, slice):
    """
    :param _list:  列表
    :param slice:  拆分块的大小
    :return:       拆分后的列表
    """
    return [_list[i:i + slice] for i in range(0, len(_list), slice)]

# 压缩文件
def zipFile(file_path, output = None, rename = None, type=3):
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
    if type==1:
        azip.write(file_path, name_extension, compress_type=zipfile.ZIP_LZMA)

    elif type==2:
        azip.write(file_path, name_extension, compress_type=zipfile.ZIP_BZIP2)
    else:
        azip.write(file_path, name_extension, compress_type=zipfile.ZIP_DEFLATED)
    azip.close()
    print("{} -> {}".format(file_path, pathJoin(output, rename + '.zip')))

# 解压文件
def unzipFile(file_path, output=None):
    """
    :param file_path:  zip文件完整路径
    :return:
    """
    path, name, _, name_extension = splitPath(file_path)
    azip = zipfile.ZipFile(file_path)
    if output is None:
        azip.extractall(path=output)
        output = pathJoin(path, name)
    else:
        azip.extractall(path=output)
        output = pathJoin(output, name)
    azip.close()

    print("{} ->> {}".format(file_path, output))

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


# gzip文件
def gzipFile(file_path, output=None, rename=None, del_file=False):
    """
    :param file_path: 文件路径
    :param output:    输出路径
    :param rename:    重命名
    :param del_file:  是否删除源文件
    :return:
    """
    assert os.path.exists(file_path)
    path, name, _, name_extension = splitPath(file_path)
    if rename is None:
        rename = name
    if output is None:
        output = path
    rename += '.gz'
    out_path = pathJoin(output, rename)
    with open(file_path, 'rb') as f_in:
        with gzip.open(out_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    if del_file:
        os.remove(file_path)
    print('{} ->> {}'.format(file_path, out_path))

# 解压gz文件
def gunzipFile(file_path, output=None, rename=None, del_file=False):
    """
    :param file_path: 文件路径
    :param output:    输出路径
    :param rename:    重命名
    :param del_file:  是否删除源文件
    :return:
    """
    assert os.path.exists(file_path)
    path, name, _, name_extension = splitPath(file_path)
    if rename is None:
        rename = name
    if output is None:
        output = path
    if rename[-3:] == '.gz':
        rename = rename[:-3]
    out_path = pathJoin(output, rename)
    with gzip.open(file_path, 'rb') as f_in:
        data = f_in.read().decode('utf8')
        with open(out_path, 'w') as f_out:
            f_out.write(data)
    if del_file:
        os.remove(file_path)
    print('{} ->> {}'.format(file_path, out_path))

# 进度条
#def bar(length):
    """
    :param length:  int or list or dict
    :return:        processbar
    """
#    if isinstance(length, int):
#        return progressbar(range(length), redirect_stdout=True)
#    elif isinstance(length, list):
#        return progressbar(range(len(length)), redirect_stdout=True)
#    elif isinstance(length, dict):
#        return progressbar(range(len(length.keys())), redirect_stdout=True)
#    else:
#        print('输入错误, 请输入int, list, dict')
# 进度条
def bar(data):
    if isinstance(data, int):
        return tqdm(range(data))
    elif isinstance(data, list) or isinstance(data, dict):
        return tqdm(data)
    elif isinstance(data, iter):
        return tqdm(list(data))
    else:
        print('输入错误, 请输入int, list, dict')

def until(y=None, m=None, d=None, H=None, M=None, S=None, logger=None):
    import time
    import datetime
    if y:
        y = int(y)
        m = int(m)
        d = int(d)
        H = int(H)
        M = int(M)
        S = int(S)
        try:
            startTime = datetime.datetime(y, m, d, H, M, S)
        except:
            if logger:
                logger.info('年月日时分秒输入错误')
            print('年月日时分秒输入错误')
            assert 1 == 2
        if startTime < datetime.datetime.now():
            logger.info('开始时间在当前时间之前')
            print('开始时间在当前时间之前')
            assert 2 == 3

        second = (startTime - datetime.datetime.now()).seconds
        minute = second // 60
        second = second % 60
        hour = minute // 60
        minute = minute % 60
        day = hour // 24
        hour = hour % 24

        print(f'将于{day}天{hour}小时{minute}分{second}秒 后运行')
        if logger:
            logger.info(f'将于{day}天{hour}小时{minute}分{second}秒 后运行')

        while datetime.datetime.now() < startTime:
            time.sleep(1)
        print('到达预定时间开始运行程序')
        if logger:
            logger.info('到达预定时间开始运行程序')
    else:
        if d or H or M or S:
            if H is None:
                H = 0
            if M is None:
                M = 0
            if S is None:
                S = 0
            seconds = 0
            time_dic = {'day': 86400,
                        'hour': 3600,
                        'min': 60}
            if d:
                seconds = (time_dic['day']*int(d) + time_dic['hour']*int(H) + time_dic['min']*int(M) + int(S))
                print(f'将于{d}天{H}小时{M}分{S}秒 后运行')
                if logger:
                    logger.info(f'将于{d}天{H}小时{M}分{S}秒 后运行')
            elif H:
                seconds = (time_dic['hour'] * int(H) + time_dic['min'] * int(M) + int(S))
                print(f'将于{H}小时{M}分{S}秒 后运行')
                if logger:
                    logger.info(f'将于{H}小时{M}分{S}秒 后运行')
            elif M:
                seconds = (time_dic['min'] * int(M) + int(S))
                print(f'将于{M}分{S}秒 后运行')
                if logger:
                    logger.info(f'将于{M}分{S}秒 后运行')
            else:
                seconds = int(S)
                print(f'将于{S}秒 后运行')
                if logger:
                    logger.info(f'将于{S}秒 后运行')
            time.sleep(seconds)
            print('到达预定时间开始运行程序')
            if logger:
                logger.info('到达预定时间开始运行程序')
        else:
            print('错误！ 定时任务没有指定时间')
            if logger is not None:
                logger.info('错误！ 定时任务没有指定时间')
                assert 3 == 4


# 获取进程pid
def get_process_id(name):
    child = subprocess.Popen(["pgrep", "-f", name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]
    response = response.decode().strip().split('\n')
    if len(response) == 1 and len(response[0]) == 0:
        return []
    return response


# cpu使用率
def monitor_memery_cpu(pids, second=10, out_path=None, show=False):
    proc = psutil.Process(int(pids))
    info = ['cpu rate\tmemory use']
    while True:
        try:
            cpu = psutil.cpu_percent()
            memory = proc.memory_info().rss / 1024 / 1024
        except:
            break
        if show:
            print(f'cpu 使用率: {cpu}%  memory 使用量 {round(memory, 2)}MB')
        info.append(f'{cpu}\t{memory}')
        time.sleep(second)
    if out_path is not None:
        with open(out_path, 'w') as f:
            f.write('\n'.join(info))


# 读取数据
def read(path, sep='\n'):
    with open(path, 'r') as f:
        return f.read().strip().split(sep)
    
# 合并列表，返回公共列表
def mergeCommelementList(lsts):
    '''
    把公共元素的列表合并，返回合并后的结果list
    '''
    sets = [set(lst) for lst in lsts if lst]
    merged = 1
    while merged:
        merged = 0
        results = []
        while sets:
            common, rest = sets[0], sets[1:]
            sets = []
            for x in rest:
                if x.isdisjoint(common):
                    sets.append(x)
                else:
                    merged = 1
                    common |= x
            results.append(common)
        sets = results
    return sets






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
    print("函数: zipFile(file_path, output, rename, type)  压缩文件(zip) type(1-3)数字越小压缩率越高")
    print("函数: unzipFile(file_path, output)   解压文件(zip)")
    print("函数: zipDir(file_dir, output, rename)  压缩文件夹(zip)")
    print("函数: unzipDir(file_dir, output, rename) 解压文件夹(zip)")
    print("函数: getFiles(path, extension=None) 获取文件夹中的文件")
    print("函数: bar(length) 返回进度条迭代器")
    print("函数: add_dic(dica, dicb) 字典数字累加")
    print("函数 until(y, m, d, H, M, S, logger) 预定时间跑程序")
    print("函数 get_process_id(name)获取进程pid返回[],没有进程返回[]列表")
    print("函数monitor_memery_cpu(pids, second=10, out_path=None, show=False) 打印或者写入进程cpu内存使用情况")
    print("函数read(path, sep='\n') 读取数据")
    print("函数mergeCommelementList合并有相同元素的列表")
