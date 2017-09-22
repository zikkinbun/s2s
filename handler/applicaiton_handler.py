# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from urlparse import urlparse
from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils

import os
import urls
import json
import random
import string
import base64
import sign_api

class CreateApplication(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(CreateApplication, self).__init__(request[0], request[1])
        self.cmdid = 4

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_name'] = json_body.get('app_name')
        self.params['pkg_name'] = json_body.get('pkg_name')
        self.params['category'] = json_body.get('category')
        self.params['platform'] = json_body.get('platform')
        self.params['url'] = json_body.get('url')
        self.params['description'] = json_body.get('description')
        self.params['chn_id'] = json_body.get('chn_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class ListApplication(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(ListApplication, self).__init__(request[0], request[1])
        self.cmdid = 3

    def _parse_request(self):
        # json解析
        try:
            # print self.request.body
            # print self.request.body_arguments
            # print type(self.request.body)
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # self.params = json_body.get('chn_id')
        self.params['chn_id'] = json_body.get('chn_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('chn_id')


class ListAllApp(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(ListAllApp, self).__init__(request[0], request[1])
        self.cmdid = 2

    def _parse_request(self):
        pass


class getApplicationDetail(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getApplicationDetail, self).__init__(request[0], request[1])
        self.cmdid = 5

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['chn_id'] = json_body.get('chn_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAppTokenUrl(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAppTokenUrl, self).__init__(request[0], request[1])
        self.cmdid = 6

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['chn_id'] = json_body.get('chn_id')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class UpdateAppCallbackUrl(BaseHandler):

    """
        callback_url = http://your_host/your_script?click_id={user_id}&sub_source_id={chn}&ip={ip}
    """

    def __init__(self, *request, **kwargs):
        super(UpdateAppCallbackUrl, self).__init__(request[0], request[1])
        self.cmdid = 7

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['chn_id'] = json_body.get('chn_id')
        self.params['callback_url'] = json_body.get('callback_url')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class SetCallbackUrl(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(SetCallbackUrl, self).__init__(request[0], request[1])
        self.cmdid = 8

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['chn_id'] = json_body.get('chn_id')
        self.params['callback_url'] = json_body.get('callback_url')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class SetDeductionPartition(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(SetDeductionPartition, self).__init__(request[0], request[1])
        self.cmdid = 9

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['app_id'] = json_body.get('app_id')
        self.params['deduction'] = json_body.get('deduction')
        self.params['divide'] = json_body.get('divide')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAppIncome(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAppIncome, self).__init__(request[0], request[1])
        self.cmdid = 10

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
