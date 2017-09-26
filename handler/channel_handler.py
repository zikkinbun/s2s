# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from base_handler import BaseHandler
from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils
from cookietoken_handler import EncryptPassword

import json
import random
import string


class SignupChaneler(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        passwd = self.get_argument('passwd', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')

        status = 0 # verifing
        chn_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        _passwd = EncryptPassword(passwd)._hash_password(passwd)
        print _passwd

class ChannelerLogin(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(ChannelerLogin, self).__init__(request[0], request[1])
        self.cmdid = 17

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['username'] = json_body.get('username')
        self.params['passwd'] = json_body.get('passwd')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class ChannelerLogout(BaseHandler):

	def get(self):
		self.clear_current_user()

class countChnAppIncome(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(countChnAppIncome, self).__init__(request[0], request[1])
        self.cmdid = 18

    def _parse_request(self):
        # json解析
        if self.request.body == '{}':
            self.params['chn_id'] = 'all'
        else:
            try:
                json_body = json.loads(self.request.body)
                # print json_body
            except:
                raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

                # 设定参数字典
            self.params['chn_id'] = json_body.get('chn_id')

            # print self.params
            if not verify_utils.is_dict(self.params):
                raise ParamException('params')
