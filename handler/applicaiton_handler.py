# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from model.application_model import ApplicationModel
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

    @tornado.gen.coroutine
    def post(self):
        # print self.request.body
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_detail(app_id, chn_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': data[0],
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except Exception as e:
            message = {
                'retcode': 7002,
                'retmsg': 'databases operate error'
            }
            self.write(message)

class getAppTokenUrl(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = json.loads(self.request.body)['app_id']
        # app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        # chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')
        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_token_url(app_id, chn_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'callback_token': data[0]['callback_token'],
                        'callback_url': data[0]['callback_url']
                    },
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 7002,
                    'retdata': {
                        'callback_token': None,
                        'callback_url': None
                    },
                    'retmsg': 'data is none, please reset the url'
                }
                self.write(message)
        except Exception as e:
            message = {
                'retcode': 7002,
                'retdata': {
                    'callback_token': None,
                    'callback_url': None
                },
                'retmsg': 'data is none, please reset the url'
            }
            self.write(message)

class UpdateAppCallbackUrl(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        sign = None
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')
        callback_url = json.loads(self.request.body)['callback_url']
        if callback_url is None:
            raise tornado.web.MissingArgumentError('callback_url')
        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_token_url(app_id, chn_id)
            callback_token = data[0]['callback_token']
            url = sign_api.sign_url(callback_url, callback_token)
            url_parse = urlparse(url)
            query = url_parse.query
            query_array = query.split('&')
            for group in query_array:
                k, v = group.split('=')
                if k == 'sign':
                    sign = v

            row = appmodel.set_application_detail(callback_url, callback_token, sign, app_id, chn_id)
            if row:
                message = {
                    'retcode': 0,
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except Exception as e:
            message = {
                'retcode': 7002,
                'retmsg': 'databases operate error'
            }
            self.write(message)

class SetCallbackUrl(BaseHandler):

    """
        callback_url = http://your_host/your_script?click_id={user_id}&sub_source_id={chn}&ip={ip}
    """

    @tornado.gen.coroutine
    def post(self):
        sign = None
        chn_id = json.loads(self.request.body)['chn_id']
        # chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        app_id = json.loads(self.request.body)['app_id']
        # app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        callback_url = json.loads(self.request.body)['callback_url']
        # callback_url = self.get_argument('callback_url', None)
        if callback_url is None:
            raise tornado.web.MissingArgumentError('callback_url')
        callback_token = base64.b64encode(os.urandom(24)) # 包括 app_secret和用户 token

        url = sign_api.sign_url(callback_url, callback_token)
        # print url
        url_parse = urlparse(url)
        query = url_parse.query
        query_array = query.split('&')
        for group in query_array:
            k, v = group.split('=')
            if k == 'sign':
                sign = v

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.set_application_detail(callback_url, callback_token, sign, app_id, chn_id)
            # print data
            message = {
                'retcode': 0,
                'retdata': {
                    'AppSign': sign,
                },
                'retmsg': 'success'
            }
            self.write(message)
        except Exception as e:
            message = {
                'retcode': 7002,
                'retmsg': 'databases operate error'
            }
            self.write(message)

class SetDeductionPartition(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        # deduction = self.get_argument('deduction', None)
        deduction = json.loads(self.request.body)['deduction']
        if deduction is None:
            raise tornado.web.MissingArgumentError('deduction')

        # divide = self.get_argument('divide', None)
        divide = json.loads(self.request.body)['divide']
        if divide is None:
            raise tornado.web.MissingArgumentError('divide')

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            row = appmodel.set_applicaiton_tranform(app_id, deduction, divide)
            if row:
                message = {
                    'retcode': 0,
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 7002,
                    'retmsg': 'databases operate error'
                }
                self.write(message)
        except Exception as e:
            # print e
            message = {
                'retcode': 7002,
                'retmsg': 'databases operate error'
            }
            self.write(message)

class getAppIncome(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_income(app_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': data[0],
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 7002,
                    'retmsg': 'databases operate error'
                }
                self.write(message)
        except Exception as e:
            # print e
            message = {
                'retcode': 7002,
                'retmsg': 'databases operate error'
            }
            self.write(message)
