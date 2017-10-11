# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import base64
import time
import json
import random
import string
from pbkdf2 import PBKDF2

from base_handler import BaseHandler
from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from utils.constants_utils import BaseConstant
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils
from model.admin_model import AdminModel

class XSRFTokenHandler(BaseHandler):
    """专门用来设置_xsrf Cookie的接口"""

    def __init__(self, *request, **kwargs):
        super(XSRFTokenHandler, self).__init__(request[0], request[1])
        self.cmdid = 36

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['tag'] = json_body.get('tag')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

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
