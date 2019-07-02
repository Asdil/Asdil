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
import os
import time
import logging
import logging.config
import cloghandler
from Asdil import tool


# 修改日志名称
def alter_log_ini(log_path, n_log=20):
    """
    替换文件中的字符串
    :param file: 文件名
    :param old_str: 就字符串
    :param new_str: 新字符串
    :return:     """
    ini = """[loggers]\nkeys=root\n[handlers]\nkeys=hand01\n[formatters]\nkeys=form01\n[logger_root]\nlevel=NOTSET\nhandlers=hand01\n[handler_hand01]\nclass=handlers.ConcurrentRotatingFileHandler\nlevel=NOTSET\nformatter=form01\nargs=\n[formatter_form01]\nformat=%(asctime)s %(levelname)s %(message)s\n"""

    log_ini_path = tool.pathJoin(log_path, 'logging.ini')
    now_date = str(time.strftime("%Y-%m-%d-%H-%I-%M", time.localtime(time.time())))

    log_path = log_path
    if log_path[-1] == '/':
        log_path = log_path[:-1]
    if os.path.exists(log_path) == False:
        os.makedirs(log_path)

    with open(log_ini_path, 'w', encoding="utf-8") as f:
        f.write(ini)

    old_str = 'args='
    new_str = '''args=("{}/{}.log", "a", 1024*2048, {})\n'''.format(log_path, now_date, n_log)
    file_data = ""
    with open(log_ini_path, "r", encoding="utf-8") as f:
        for line in f:

            if old_str in line:
                line = new_str
                file_data += line
            else:
                file_data += line

    with open(log_ini_path, "w", encoding="utf-8") as f:
        f.write(file_data)


# 初始化日志
def init_log(log_path):
    log_ini_path = tool.pathJoin(log_path, 'logging.ini')
    logging.config.fileConfig(log_ini_path)
    log = logging.getLogger()
    return log
