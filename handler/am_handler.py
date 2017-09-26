# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils

import json
import random
import string


class AMSginup(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMSginup, self).__init__(request[0], request[1])
        self.cmdid = 21

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['am_name'] = json_body.get('am_name')
        self.params['passwd'] = json_body.get('passwd')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class AMChannelOper(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMChannelOper, self).__init__(request[0], request[1])
        self.cmdid = 22

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['status'] = json_body.get('status')
        self.params['chn_id'] = json_body.get('chn_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class AMCreateOfferByUnion(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMCreateOfferByUnion, self).__init__(request[0], request[1])
        self.cmdid = 29

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['ader_id'] = json_body.get('ader_id')
        self.params['app_id'] = json_body.get('app_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class AMAppOper(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMAppOper, self).__init__(request[0], request[1])
        self.cmdid = 23

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['status'] = json_body.get('status')
        self.params['chn_id'] = json_body.get('chn_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class AMLogin(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMLogin, self).__init__(request[0], request[1])
        self.cmdid = 24

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

class AMChannelSignup(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMChannelSignup, self).__init__(request[0], request[1])
        self.cmdid = 25

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
        self.params['email'] = json_body.get('email')
        self.params['status'] = json_body.get('status')
        self.params['chn_id'] = json_body.get('chn_id')
        self.params['am_id'] = json_body.get('am_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class AMListChannel(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMListChannel, self).__init__(request[0], request[1])
        self.cmdid = 26

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['am_id'] = json_body.get('am_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')


class AMList(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMList, self).__init__(request[0], request[1])
        self.cmdid = 27

class AMCountAdIncome(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(AMCountAdIncome, self).__init__(request[0], request[1])
        self.cmdid = 28

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['ader_id'] = json_body.get('ader_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class AMIncome(BaseHandler):
    pass

class AMTestCallback(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # am_id = self.get_argument('am_id', None)
        am_id = json.loads(self.request.body)['am_id']
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')
            # edit_callback_url = self.get_argument('callback_url', None)
        callback_url = json.loads(self.request.body)['callback_url']
        if callback_url is None:
            raise tornado.web.MissingArgumentError('callback_url')

        try:
            client = tornado.httpclient.AsyncHTTPClient() # 异步回调
            headers = tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"})
            request = tornado.httpclient.HTTPRequest(edit_callback_url, "GET", headers)
            response = yield client.fetch(request)
        except Exception as e:
            self.write_error(500)
