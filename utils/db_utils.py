# _*_ coding:utf-8_*_
from functools import wraps
from db import db_setting
import torndb

class TornDBReadConnector(object):
    '''
    简单的torndb操作类, 用于单独建立和销毁数据库连接
    '''

    def __init__(self):
<<<<<<< HEAD
        self.read_conn = torndb.Connection(setting.RELEASE['s2s']['read']['host'], setting.RELEASE['s2s']['read']['database'], setting.RELEASE['s2s']['read']['user'], setting.RELEASE['s2s']['read']['password'])
=======
        self.read_conn = torndb.Connection(db_setting.DEV['s2s']['read']['host'], db_setting.DEV['s2s']['read']['database'], db_setting.DEV['s2s']['read']['user'], db_setting.DEV['s2s']['read']['password'])
>>>>>>> master

    def __enter__(self):
        '''
        '''
        return self.read_conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.read_conn:
            self.read_conn.close()

    def __del__(self):
        if self.read_conn:
            self.read_conn.close()

    def query(self, sql, *args):
        return self.read_conn.query(sql, *args)

    def execute_lastrowid(self, sql):
        return self.read_conn.execute_lastrowid(sql)

class TornDBWriteConnector(object):
    '''
    简单的torndb操作类, 用于单独建立和销毁数据库连接
    '''

    def __init__(self):
<<<<<<< HEAD
        self.write_conn = torndb.Connection(setting.RELEASE['s2s']['write']['host'], setting.RELEASE['s2s']['write']['database'], setting.RELEASE['s2s']['write']['user'], setting.RELEASE['s2s']['write']['password'])
=======
        self.write_conn = torndb.Connection(db_setting.DEV['s2s']['write']['host'], db_setting.DEV['s2s']['write']['database'], db_setting.DEV['s2s']['write']['user'], db_setting.DEV['s2s']['write']['password'])
>>>>>>> master

    def __enter__(self):
        '''
        '''
        return self.write_conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    def __del__(self):
        if self.write_conn:
            self.write_conn.close()

    def query(self, sql, *args):
        return self.write_conn.query(sql, *args)

    def execute_lastrowid(self, sql):
        return self.write_conn.execute_lastrowid(sql)

# def db_operator(func):
#     '''
#     用于修饰数据库操作类(如BaseDB)中的方法, 将异常转化为DBException
#     '''
#     @wraps(func)
#     def _dec(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except Exception, e:
#             # 为了保留原异常栈信息, 需要同时raise traceback对象
#             raise DBException, DBException(e), sys.exc_info()[2]
#         return _dec
