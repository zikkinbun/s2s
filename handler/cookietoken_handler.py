# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

from pbkdf2 import PBKDF2

class XSRFTokenHandler(tornado.web.RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""
    def get(self):
        token = self.xsrf_token
        self.write(token)

class EncryptPassword(object):

    def __init__(self, password):
        self._password = password

    #定义一个内部使用加密的方法
    def _hash_password(self,password):
        return PBKDF2.crypt(password, iterations=0x2537)

    #使用property装饰器使方法变为属性
    @property
    def password(self):
        return self._password

    #设置加密后给类属性赋值
    @password.setter
    def password(self,password):
        self._password = self._hash_password(password)

    #定义一个密码校验的方法
    def auth_password(self,pwd):
        if self._password is not None:
            return self.password == PBKDF2.crypt(pwd, self.password)
        else:
            return False
