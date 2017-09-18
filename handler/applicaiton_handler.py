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

    @tornado.gen.coroutine
    def post(self):
        app_name = json.loads(self.request.body)['app_name']
        if app_name is None:
            raise tornado.web.MissingArgumentError('app_name')
        pkg_name = json.loads(self.request.body)['pkg_name']
        if pkg_name is None:
            raise tornado.web.MissingArgumentError('pkg_name')
        category = json.loads(self.request.body)['category']
        if category is None:
            raise tornado.web.MissingArgumentError('category')
        platform = json.loads(self.request.body)['platform']
        if platform is None:
            raise tornado.web.MissingArgumentError('platform')
        url = json.loads(self.request.body)['url']
        if url is None:
            raise tornado.web.MissingArgumentError('url')
        description = json.loads(self.request.body)['description']
        if description is None:
            raise tornado.web.MissingArgumentError('description')

        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        app_id = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        app_secret = base64.b64encode(os.urandom(16))

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.create_applicaiton(app_id, app_secret, app_name, pkg_name, category, platform, url, description, chn_id)
            msg = {
                'retcode': 0,
                'retdata': {
                    'AppID': app_id,
                    'AppSecret': app_secret
                },
                'retmsg': 'APP is created,please contract your account manager to active your APP',
            }
            self.write(msg)

        except err.ProgrammingError as e:
            msg = {
                'retcode': 7002,
                'retmsg': 'databases operate error'
            }
            self.write(msg)

class ListApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.list_application_by_chnid(chn_id)
            response = {
                'retcode': 0,
                'retdata': data,
                'retmsg': 'success'
            }
            self.write(response)
        except err.ProgrammingError as e:
            print e

class ListAllApp(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(ListAllApp, self).__init__(request[0], request[1])
        self.set_header("Content-Type", "application/json")
        self.tracker = self.application.tracker
        self.sys_logger = self.application.sys_logger
        self.cmdid = 0
        self.timestamp = 0
        self.params = dict()
        self.response = dict()


    @tornado.gen.coroutine
    def post(self):
        # try:
            # db_conns = self.application.db_conns
            # appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            # data = appmodel.list_application_all()
            # if data:
            #     message = {
            #         'retcode': 0,
            #         'retdata': data,
            #         'retmsg': 'success'
            #     }
            #     self.write(message)
            # else:
            #     self.write_error(500)
        # except Exception as e:
        #     message = {
        #         'retcode': 7002,
        #         'retmsg': 'databases operate error'
        #     }
        #     self.write(message)
        try:
            self.tracker.logging_request_header(self)
            self.tracker.logging_request_body(self)
            self._parse_request()

            # 分发 processor
            processor = urls.processor_mapping.get(self.cmdid)
            if not processor:
                # 协议不存在
                raise BaseException(BaseError.ERROR_COMMON_CMD_NOT_EXISTS)
            # 协议处理
            if processor[1]:
                # 内部调用的协议
                raise BaseException(BaseError.ERROR_COMMON_PROTOCOL_FOR_INTERNAL_ONLY)
            processor = processor[0]
            data = yield processor(self).process()

            # 成功
            self.res = ResponseBuilder.build_success(self, data)
        except BaseException, e:
            # 根据捕获的UFOException返回错误信息
            self.res = ResponseBuilder.build_error(self, e)
        except DBException, e:
            # 如果是底层未处理的DBException, 在这里转化为UFOException
            self.tracker.trace_error()
            e = BaseException(BaseError.ERROR_COMMON_DATABASE_EXCEPTION)
            self.res = ResponseBuilder.build_error(self, e)
        except Exception, e:
            self.tracker.trace_error()
            e = BaseException(BaseError.ERROR_COMMON_UNKNOWN)
            self.res = ResponseBuilder.build_error(self, e)

        # 记录响应
        self.tracker.logging_response(self)

        # 响应
        self.write(json.dumps(self.res, cls=ComplexEncoder))
        self.finish()
        # return

    def _parse_request(self):
        '''
        解析请求参数
        '''

        # 从header中解析参数
        try:
            self.cmdid = int(self.request.headers.get('cmdid', 0))
        except:
            raise ParamException('cmdid')

        try:
            self.timestamp = long(self.request.headers.get('timestamp', 0))
        except:
            raise ParamException('timestamp')

        # json解析
        try:
            json_body = json.loads(self.request.body)
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 参数校验
        self.userid = json_body.get('userid')
        if not verify_utils.is_int(self.userid):
            raise ParamException('userid')

        self.userkey = json_body.get('userkey')
        if not verify_utils.is_string(self.userkey):
            raise ParamException('userkey')

        self.params = json_body.get('params')
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

    def _log(self):
        '''
        '''
        self.application.log_request(self)

class getApplicationDetail(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
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
