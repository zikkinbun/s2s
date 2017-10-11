# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils

import sign_api
import json


class OfferHandler(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(OfferHandler, self).__init__(request[0], request[1])
        self.cmdid = 19

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['page_size'] = json_body.get('page_size')
        self.params['page'] = json_body.get('page')
        self.params['sign'] = json_body.get('sign')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class ListAllOffer(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(ListAllOffer, self).__init__(request[0], request[1])
        self.cmdid = 20

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['page_size'] = json_body.get('page_size')
        self.params['page'] = json_body.get('page')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')
