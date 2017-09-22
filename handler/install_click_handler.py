# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils

class getAppInstall(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAppInstall, self).__init__(request[0], request[1])
        self.cmdid = 31

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAppRecvInstall(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAppRecvInstall, self).__init__(request[0], request[1])
        self.cmdid = 32

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAppClick(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAppClick, self).__init__(request[0], request[1])
        self.cmdid = 33

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAppValidClick(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAppValidClick, self).__init__(request[0], request[1])
        self.cmdid = 34

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')
