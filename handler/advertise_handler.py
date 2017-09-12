# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from handler.base_handler import BaseHandler
from model.advertise_model import AdvertiseModel, AdvertiserModel
import sign_api

from urlparse import urlparse
from datetime import datetime

import base64
import os
import json
import random
import string
import requests

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

    @tornado.gen.coroutine
    def post(self):
        ader_id = json.loads(self.request.body)['ader_id']
        if not ader_id:
            raise tornado.web.MissingArgumentError('ader_id')

        page_size = json.loads(self.request.body)['page_size']
        if not page_size:
            raise tornado.web.MissingArgumentError('page_size')

        index = json.loads(self.request.body)['page']
        if not index:
            raise tornado.web.MissingArgumentError('page')

        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
            data = advermodel.get_advertise_by_AderId(ader_id, int(page_size), int(index))
            total = advermodel.get_total_count_list(ader_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'total': total['COUNT(*)'],
                        'advertise': data,
                        'index': index
                    },
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 2007,
                    'retmsg': 'have no advertise'
                }
                self.write(message)
        except Exception as e:
            # print e
            message = {
                'retcode': 2006,
                'retmsg': 'databases oper error'
            }
            self.write(message)

class getAdvertiseByGetPrice(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        key = json.loads(self.request.body)['key']
        # key = self.get_argument('key', None)
        if not key:
            raise tornado.web.MissingArgumentError('key')
        # value = self.get_argument('value', None)
        value = json.loads(self.request.body)['value']
        if not value:
            raise tornado.web.MissingArgumentError('value')
        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
            data = advermodel.get_advertise_by_get_price(key, value)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'advertise': data,
                    },
                    'retmsg': 'success'
                }
                self.write(message)
        except Exception as e:
            message = {
                'retcode': 2006,
                'retmsg': 'databases operate error'
            }
            self.write(message)

class getAdvertiseAll(BaseHandler):

    @tornado.gen.coroutine
    def post(self):

        page_size = json.loads(self.request.body)['page_size']
        if not page_size:
            raise tornado.web.MissingArgumentError('page_size')

        index = json.loads(self.request.body)['page']
        if not index:
            raise tornado.web.MissingArgumentError('page')

        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
            data = advermodel.get_advertise_all(int(page_size), int(index))
            total = advermodel.get_total_count_all()
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'total': total['COUNT(*)'],
                        'advertise': data,
                        'index': index
                    },
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 2007,
                    'retmsg': 'have no advertise'
                }
                self.write(message)
        except Exception as e:
            message = {
                'retcode': 2006,
                'retmsg': 'databases operate error'
            }
            self.write(message)

class Advertiser(BaseHandler):

    """
        广告主录入
    """

    @tornado.gen.coroutine
    def post(self):
        api_name = json.loads(self.request.body)['api_name']
        # api_name = self.get_argument('api_name', None)
        if not api_name:
            raise tornado.web.MissingArgumentError('api_name')

        name = json.loads(self.request.body)['name']
        # name = self.get_argument('name', None)
        if not name:
            raise tornado.web.MissingArgumentError('name')

        resp_callback_url = json.loads(self.request.body)['resp_callback_url']
        # resp_callback_url = self.get_argument('resp_callback_url', None)
        if not resp_callback_url:
            raise tornado.web.MissingArgumentError('resp_callback_url')

        resp_callback_token = json.loads(self.request.body)['resp_callback_token']
        # resp_callback_token = self.get_argument('resp_callback_token', None)
        if not resp_callback_token:
            raise tornado.web.MissingArgumentError('resp_callback_token')

        is_pulled = json.loads(self.request.body)['is_pulled'] # 控制定时拉取任务
        # is_pulled = self.get_argument('is_pulled', None)
        # print is_pulled
        if not is_pulled:
            raise tornado.web.MissingArgumentError('is_pulled')


        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiserModel(db_conns['read'], db_conns['write'])
            data = advermodel.check_duplicate_advertiser(api_name)
            # print data
            if data:
                msg = {
                    'retcode': 2005,
                    'retmsg': 'Advertiser is existed'
                }
                self.write(msg)
            else:
                try:
                    row = advermodel.set_advertiser(api_name, name, resp_callback_url, resp_callback_token, is_pulled)
                    if row:
                        msg = {
                            'retcode': 0,
                            'retmsg': 'Advertiser commit successfully'
                            }
                        self.write(msg)
                except Exception as e:
                    msg = {
                        'retcode': 2006,
                        'retmsg': 'databases oper error'
                    }
                    self.write(msg)
        except Exception as e:
            # print e
            msg = {
                'retcode': 2006,
                'retmsg': 'databases oper error'
            }
            self.write(msg)

class getAdvertiserALL(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiserModel(db_conns['read'], db_conns['write'])
            data = advermodel.get_advertiser()
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'union': data
                    },
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except Exception as e:
            msg = {
                'retcode': 2006,
                'retmsg': 'databases oper error'
            }
            self.write(msg)

class getAdverIncome(BaseHandler):

    def post(self):
        db_conns = self.application.db_conns
        admodel = AdvertiseModel(db_conns['read'], db_conns['write'])
        adermodel = AdvertiserModel(db_conns['read'], db_conns['write'])

        # ader_id = json.loads(self.request.body)['ader_id']
        ader_id = self.get_argument('ader_id', None)
        # if self.request.body == '{}':
        if ader_id is None:
            try:
                ader_data = []
                ader_list = adermodel.get_advertiser()
                for ader in ader_list:
                    aderid = ader['id']
                    advertise = admodel.count_all_advertise_income_by_id(aderid)[0]
                    # print advertise
                    ader_data.append(advertise)
                message = {
                    'retcode': 0,
                    'retdata': ader_data
                }
                self.write(message)
            except Exception as e:
                print e
                raise HTTPError(status_code=500)
        else:
            # ader_id = json.loads(self.request.body)['ader_id']
            ader_id = self.get_argument('ader_id', None)
            try:
                advertise = admodel.count_all_advertise_income_by_id(ader_id)[0]
                message = {
                    'retcode': 0,
                    'retdata': advertise
                }
                self.write(message)
            except Exception as e:
                print e
                raise HTTPError(status_code=500)
