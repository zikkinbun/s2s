# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from handler.base_handler import BaseHandler
from model.advertise_model import AdvertiseModel, AdvertiserModel

import json

class AdvertiseStatus(object):
    """
        广告状态操作
    """

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.advermodel = AdvertiseModel(self.db_conns['read'], self.db_conns['write'])

    def getAdvertise(self, ad_id):
        try:
            data = self.advermodel.get_advertise_by_adid(ad_id)
            if data:
                return data
            else:
                msg = {
                    'retcode': 2002,
                    'retmsg': 'this advertise is not existed'
                }
                return msg
        except Exception as e:
            msg = {
                'retcode': 2002,
                'retmsg': 'this advertise is not existed'
            }
            return msg

    def getDeviceInfo(self, ad_id):
        try:
            data = self.advermodel.get_device_info(ad_id)
            if data:
                return data[0]
            else:
                msg = {
                    'retcode': 2003,
                    'retmsg': 'this advetise have no device info'
                }
                return msg
        except Exception as e:
            msg = {
                'retcode': 2003,
                'retmsg': 'this advetise have no device info'
            }
            return msg


class getAdvertiseById(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAdvertiseById, self).__init__(request[0], request[1])
        self.cmdid = 11

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['ader_id'] = json_body.get('ader_id')
        self.params['page_size'] = json_body.get('page_size')
        self.params['index'] = json_body.get('index')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAdvertiseByGetPrice(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAdvertiseByGetPrice, self).__init__(request[0], request[1])
        self.cmdid = 12

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['key'] = json_body.get('key')
        self.params['value'] = json_body.get('value')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAdvertiseAll(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAdvertiseAll, self).__init__(request[0], request[1])
        self.cmdid = 13

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['page_size'] = json_body.get('page_size')
        self.params['index'] = json_body.get('index')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class Advertiser(BaseHandler):

    """
        广告主录入
    """
    def __init__(self, *request, **kwargs):
        super(Advertiser, self).__init__(request[0], request[1])
        self.cmdid = 14

    def _parse_request(self):
        # json解析
        try:
            json_body = json.loads(self.request.body)
            # print json_body
        except:
            raise BaseException(BaseError.ERROR_COMMON_PARSE_JSON_FAILED)

        # 设定参数字典
        self.params['api_name'] = json_body.get('api_name')
        self.params['name'] = json_body.get('name')
        self.params['resp_callback_url'] = json_body.get('resp_callback_url')
        self.params['resp_callback_token'] = json_body.get('resp_callback_token')
        self.params['is_pulled'] = json_body.get('is_pulled')
        # print self.params
        if not verify_utils.is_dict(self.params):
            raise ParamException('params')

class getAdvertiserALL(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(getAdvertiserALL, self).__init__(request[0], request[1])
        self.cmdid = 15

class getAdverIncome(BaseHandler):

    def __init__(self, *request, **kwargs):
        super(Advertiser, self).__init__(request[0], request[1])
        self.cmdid = 16

    def _parse_request(self):
        # json解析
        if self.request.body == '{}':
            self.params['ader_id'] = 'all'
        else:
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
