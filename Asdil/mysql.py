# -*- coding: utf-8 -*-

from pymysqlpool.pool import Pool
import pymysql
class mySql:
    def __init__(self,host, port, user, password, database):
        self.pool = Pool(host=host, port=port, user=user, password=password, db=database)
        self.pool.init()
    def fetchone(self,sql, parama):
        newparama = []
        news = []
        for each in parama:
            if isinstance(each, list):
                newparama.extend(each)
                news.append(','.join(['%s']*len(each)))
            else:
                newparama.append(each)
                news.append('%s')
#         for index,data in enumerate(news):
#             sql = sql.replace('%s', data, 1)
        sql = sql % tuple(news)
        connection = self.pool.get_conn()
        cur = connection.cursor()

        cur.execute(sql, args=tuple(newparama))
        ret = cur.fetchone()
        self.pool.release(connection)
        return

    def fetchall(self,sql, parama):
        newparama = []
        news = []
        for each in parama:
            if isinstance(each, list):
                newparama.extend(each)
                news.append(','.join(['%s']*len(each)))
            else:
                newparama.append(each)
                news.append('%s')
#         for index,data in enumerate(news):
#             sql = sql.replace('%s', data, 1)
        sql = sql % tuple(news)
        connection = self.pool.get_conn()
        cur = connection.cursor()

        cur.execute(sql, args=tuple(newparama))
        ret = cur.fetchall()
        self.pool.release(connection)
        return ret
    def update(self, sql, parama):
        newparama = []
        news = []
        for each in parama:
            if isinstance(each, list):
                newparama.extend(each)
                news.append(','.join(['%s']*len(each)))
            else:
                newparama.append(each)
                news.append('%s')
        sql = sql % tuple(news)
        print(sql)
        connection = self.pool.get_conn()
        cur = connection.cursor()
        cur.execute(sql, args=tuple(newparama))
        connection.commit()
        self.pool.release(connection)
    def hp():
        print('修改')
        print("sql = mySql('127.0.0.1', 3306, 'root', 'juiuijiju', 'mysql')")
        print("cmd = 'update student set name=%s where id=%s'")
        print("sql.update(cmd, ['修改', '3'])")
        print()
        print("插入")
        print("cmd = 'insert into student values(%s)'")
        print("sql.update(cmd, [['3', '三力士']])")
        print()
        print("查询")
        print("cmd = 'select * from student where id in (%s)'")
        print("sql.fetchall(cmd, [['1', '2']])")
        print("sql.fetchone(cmd, [['1', '2']])")
        print()
        print("删除")
        print("cmd = 'delete from student where id=%s'")
        print("sql.update(cmd, ['3',])")
