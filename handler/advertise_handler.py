# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from handler.base_handler import BaseHandler
from model.advertise_model import AdvertiseModel, AdvertiserModel
import sign_api

from pymysql import err
from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import string
import requests

class Advertises(object):

    """
        对接上游 API,拉取 OFFER 下的广告信息
    """

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.advermodel = AdvertiseModel(self.db_conns['read'], self.db_conns['write'])
        self.advertermodel = AdvertiserModel(self.db_conns['read'], self.db_conns['write'])
        self.api_name = 'Admix'

    def verifyPullstatus(self):
        data = self.advertermodel.get_pull_status(self.api_name)
        is_pulled = data['is_pulled']
        if int(is_pulled) == 1 or is_pulled == '1':
            return True
        else:
            return False

    def setStatus(self, api_name, is_pulled):
        try:
            row = self.advertermodel.set_pull_status(self.api_name, is_pulled)
            if row:
                message = {
                    'retcode': 0,
                    'retmsg': 'update status success'
                }
                return message
            else:
                message = {
                    'retcode': 2006,
                    'retmsg': 'databases operate error'
                }

        except Exception as e:
            print e

    def getAdxmiOffer(self, app_id, page_size):
        datas = None
        page = 1
        url = 'http://ad.api.yyapi.net/v2/offline'
        default_params = {
            'app_id': app_id,
            'page_size': page_size,
            'page': page
        }
        if self.verifyPullstatus():
            r = requests.get(url, default_params)
            if r.status_code == '200' or r.status_code == 200:
                datas = json.loads(r.text)
                if datas['offers'] == [] or datas['offers'] == '[]':
                    self.setStatus(self.api_name, 0)
                    msg = {
                        'retcode': 2001,
                        'retmsg':"This advertiser's API is closed."
                    }
                    return msg
                else:
                    for data in datas['offers']:
                        ad_id = ''.join(random.sample(string.digits, 8))
                        ader_id = 1

                        device = data[u'mandatory_device']
                        new_device = self.advermodel.create_device_info(ad_id, device)
                        new_advertise = self.advermodel.create_Admix_advertise(ad_id, ader_id, data)

                    page_range = int(datas['total'])/int(datas['page_size']) + 1
                    next_page = page + 1
                    for i in range(next_page ,page_range):
                        params = {
                            'app_id': app_id,
                            'page_size': page_size,
                            'page': i
                        }
                        # print params
                        r = requests.get(url, params)
                        if r.status_code == '200' or r.status_code == 200:
                            datas = json.loads(r.text)
                            # print i
                            for data in datas['offers']:
                                ad_id = ''.join(random.sample(string.digits, 8))
                                ader_id = 1
                                device = data[u'mandatory_device']
                                new_device = self.advermodel.create_device_info(ad_id, device)
                                new_advertise = self.advermodel.create_Admix_advertise(ad_id, ader_id, data)

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
                return data
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
        if not api_name:
            raise tornado.web.MissingArgumentError('api_name')
        name = json.loads(self.request.body)['name']
        if not name:
            raise tornado.web.MissingArgumentError('name')
        resp_callback_url = json.loads(self.request.body)['resp_callback_url']
        if not resp_callback_url:
            raise tornado.web.MissingArgumentError('resp_callback_url')
        resp_callback_token = json.loads(self.request.body)['resp_callback_token']
        if not resp_callback_url:
            raise tornado.web.MissingArgumentError('resp_callback_token')
        is_pulled = json.loads(self.request.body)['is_pulled'] # 控制定时拉取任务
        if not is_pulled:
            raise tornado.web.MissingArgumentError('is_pulled')

        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiserModel(db_conns['read'], db_conns['write'])
            data = advermodel.check_duplicate_advertiser(api_name)
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
