# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from utils.protocol_utils import ResponseBuilder
from utils.common_utils import ComplexEncoder
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from utils import verify_utils

import base64
import re
import os
import json


class ClickUrlHandler(BaseHandler):
    """
        用户每访问一次我的click_url 就生成一次 click 记录，包括 click_id,ad_id,app_id，
        可以从下游通过的我们 offer提供的trackinglink做统计，或者我们自己生成 click
    """

    def __init__(self, *request, **kwargs):
        super(ClickUrlHandler, self).__init__(request[0], request[1])
        self.cmdid = 30

    def _parse_request(self):

        # headers 匹配
        try:
            headers = self.request.headers
            if re.search(ur'(iPhone)', str(headers)) or re.search(ur'(Android)', str(headers)):
                # json解析
                try:
                    json_body = json.loads(self.request.body)
                    # print json_body
                except:
                    raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

                # 设定参数字典
                self.params['offer_id'] = json_body.get('offer_id')
                self.params['app_id'] = json_body.get('app_id')
                self.params['app_click_id'] = json_body.get('app_click_id')
                self.params['pid'] = json_body.get('pid')
                # print self.params
                if not verify_utils.is_dict(self.params):
                    raise ParamException('params')
            else:
                raise BaseException(BaseError.ERROR_USERAGENT_NOT_MOBILE)
        except:
            raise BaseException(BaseError.ERROR_COMMON_UNKNOWN)

class CreateClickUrl(object):

    """
        http://api.bensonzhi.co/track?ad=xxxx&app_id=xxxx&pid=xxxx&click_id=xxxx
    """

    def __init__(self, app_id, ad_id, pid):
        self.ad_id = ad_id
        self.app_id = app_id
        self.pid = pid
        self.base_url = 'http://api.bensonzhi.co/v1/track'

    def createUrl(self):
        url = self.base_url + '?ad_id=%s&app_id=%s&pid=%s' % (self.ad_id, self.app_id, self.pid)
        return url
