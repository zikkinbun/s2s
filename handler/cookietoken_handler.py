# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

import base64
import time
from pbkdf2 import PBKDF2
from model.admin_model import AdminModel


class XSRFTokenHandler(tornado.web.RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""
    @tornado.gen.coroutine
    def get(self):
        token = self.xsrf_token
        print token
        self.write(token)

class AdminTokenHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        cur_time = time.time()
        end_time = cur_time-cur_time%86400
        access_token = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        access_secret = access_token + '&' + end_time


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

def RSAsign(object):

    def sign(self,signdata):
        '''''
        @param signdata: 需要签名的字符串
        '''

        h=SHA.new(signdata)
        signer = pk.new(Gl.privatekey)
        signn=signer.sign(h)
        signn=base64.b64encode(signn)
        return  signn

    '''''
    RSA验签
    结果：如果验签通过，则返回The signature is authentic
         如果验签不通过，则返回"The signature is not authentic."
    '''
    def checksign(self,rdata):

        signn=base64.b64decode(rdata.pop('sign'))
        signdata=self.sort(rdata)
        verifier = pk.new(Gl.publickey)
        if verifier.verify(SHA.new(signdata), signn):
            print "The signature is authentic."
        else:
            print "The signature is not authentic."
