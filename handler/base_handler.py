# _*_ coding:utf-8_*_
import tornado.web

from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils

import urls
import json

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self, *request, **kwargs):
        super(BaseHandler, self).__init__(request[0], request[1])
        self.set_header("Content-Type", "application/json")
        self.tracker = self.application.tracker
        self.sys_logger = self.application.sys_logger
        self.params = dict()
        self.res = dict()

    def get_current_user(self):
        return self.get_secure_cookie("user_id", 0)

    def set_current_user(self, user_id):
        if user_id:
            self.set_secure_cookie('user_id', tornado.escape.json_encode(user_id))
        else:
            self.clear_cookie("user_id")

    def clear_current_user(self):
        self.clear_cookie("user_id")

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        try:
            self.tracker.logging_request_header(self)
            self.tracker.logging_request_body(self)
            self._parse_request()
            # 分发 processor
            processor = urls.processor_mapping.get(self.cmdid)
            # print processor
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

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        try:
            self.tracker.logging_request_header(self)
            self.tracker.logging_request_body(self)
            self._parse_request()
            # 分发 processor
            processor = urls.processor_mapping.get(self.cmdid)
            # print processor
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

    def _log(self):
        '''
        '''
        self.application.log_request(self)

    def request_redirect(self, url):
        '''
            重定向
        '''
        self.redirect(url)
