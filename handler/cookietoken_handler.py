# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

import base64
import time
import json
import random
import string
import hashlib
import hmac

from pbkdf2 import PBKDF2
from model.admin_model import AdminModel

class XSRFTokenHandler(tornado.web.RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""
    @tornado.gen.coroutine
    def get(self):
        token = self.xsrf_token
        # print token
        self.write(token)

class AdminTokenHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        cur_time = time.time()
        end_time = int(cur_time - cur_time%86400)
        default_expires = 24
        access_token = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        access_Hashsign = Hashsign()
        access_sign = access_Hashsign.sign(access_token, str(end_time))
        try:
            db_conns = self.application.db_conns
            admodel = AdminModel(db_conns['read'], db_conns['write'])
            row = admodel.set_secret_sign(access_token, access_sign, 'vue_user', default_expires)
            if row:
                self.write(access_sign)
        except Exception as e:
            message = {
                'retcode': -1,
                'retmsg': 'token created failure'
            }
            self.write(message)

    @tornado.gen.coroutine
    def post(self):
        token = self.request.headers['_token']
        access_Hashsign = Hashsign()
        print token


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

class Hashsign(object):

    def sign(self,signdata, timestamp):
        '''
        @param signdata: 需要签名的字符串
        '''
        md5 = hashlib.md5(timestamp)
        md5.update(signdata)
        signn = md5.hexdigest()
        return signn

    def checktimeout(self, timestamp):
        current_time = time.time()
        time_range = current_time - timestamp # second
        print time_range

    def compare(self, a, b):
        return hmac.compare_digest(a, b)
