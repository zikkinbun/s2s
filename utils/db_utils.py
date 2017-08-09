# _*_ coding:utf-8_*_
from functools import wraps
import torndb

class TornDBConnector(object):
    '''
    简单的torndb操作类, 用于单独建立和销毁数据库连接
    '''

    def __init__(self, host, db, user, passwd):
        self.conn = torndb.Connection(host, db, user, passwd)

    def __enter__(self):
        '''
        '''
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def query(self, sql, *args):
        return self.conn.query(sql, *args)

    def execute_lastrowid(self, sql):
        return self.conn.execute_lastrowid(sql)

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
