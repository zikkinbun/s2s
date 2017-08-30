# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from model.application_model import ApplicationModel
from model.advertise_model import AdvertiseModel
from model.offer_model import OfferModel
from model.channeler_model import ChannelModel
from model.rule_model import RuleModel

from base_handler import BaseHandler
from click_handler import CreateClickUrl
from rule_handler import SpecailRule

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
import sign_api

from datetime import datetime
import os
import re
import json
import random
import string


class OfferHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        """
            查看任务
            判断条件：签名正确，账号状态为激活状态
        """
        verify_sign = None
        verify_app = None

        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        page_size = json.loads(self.request.body)['page_size']
        if page_size is None:
            raise tornado.web.MissingArgumentError('page_size')

        page = json.loads(self.request.body)['page']
        if page is None:
            raise tornado.web.MissingArgumentError('page')

        sign = json.loads(self.request.body)['accesskey']
        if sign is None:
            raise tornado.web.MissingArgumentError('accesskey')

        chn_id = ''
        db_conns = self.application.db_conns
        # 验证签名
        try:
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.verify_app_sign(app_id, sign)
            chn_id = data[0]['chn_id']
            sign_url = data[0]['callback_url'] + '&sign=%s' % sign
            verify_sign = sign_api.verifySinature(sign_url, data[0]['callback_token'])
            # base_url = data[0][2]
        except Exception as e:
            msg = {
                'retcode': 3001,
                'retmsg': 'Sign Error'
            }
            self.write(msg)

        # 验证下游的 APP 状态是否可用
        try:
            chnermodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = chnermodel.verify_app_status(chn_id, app_id)
            # print data
            if not data:
                msg = {
                    'retcode': 3002,
                    'retmsg': 'app_id not exists, please check your app_id'
                }
                self.write(msg)
            elif int(data['app_status']) == 0 and int(data['app_status']) is None:
                msg = {
                    'retcode': 3003,
                    'retmsg': "Application didn't pass the verification, please contact your accout manager"
                }
                self.write(msg)
            elif data['chn_status'] == 0 or data['chn_status'] is None:
                msg = {
                    'retcode': 3004,
                    'retmsg': "Channeler didn't pass the verification, please contact your accout manager"
                }
                self.write(msg)
            elif int(data['app_status']) == 1 and int(data['chn_status']) == 1:
                verify_app = True
            else:
                self.write_error(500)
        except Exception as e:
            msg = {
                'retcode': 3005,
                'retmsg': 'Data request Error'
            }
            self.write(msg)

        # print verify_sign, verify_app
        if verify_sign and verify_app:
            offermodel = OfferModel(db_conns['read'], db_conns['write'])
            data = offermodel.get_offer_by_app(app_id, sign, page_size, page)
            # print serializers
            response = {
                'retcode': 0,
                'retmsg': 'OK',
                'retdata': {
                    'offers': data
                }
            }
            self.write(response)
        else:
            self.write_error(500)

class ListAllOffer(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # page_size = self.get_argument('page_size', None)
        page_size = json.loads(self.request.body)['page_size']
        if not page_size:
            raise tornado.web.MissingArgumentError('page_size')
        # page = self.get_argument('page', None)
        page_size = json.loads(self.request.body)['page']
        if not page:
            raise tornado.web.MissingArgumentError('page')
        try:
            db_conns = self.application.db_conns
            offermodel = OfferModel(db_conns['read'], db_conns['write'])
            data = offermodel.get_all_offer(page_size, page)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'offers': data
                    },
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except Exception as e:
            print e

class AdvertiseTransOffer(object):

    def __init__(self):
        self.data = None
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.rulemodel = RuleModel(self.db_conns['read'], self.db_conns['write'])
        self.offermodel = OfferModel(self.db_conns['read'], self.db_conns['write'])
        self.advermodel = AdvertiseModel(self.db_conns['read'], self.db_conns['write'])

    def getAdvertiseByGetPrice(self, key, value):
        try:
            data = self.advermodel.get_advertise_by_get_price(key, value)
            if data:
                self.data = data
                message = {
                    'retcode': 0,
                    'retmsg': 'catch advertise success'
                }
                return message
            else:
                message = {
                    'retcode': 3006,
                    'retmsg': 'have no this OFFER'
                }
                return message
        except Exception as e:
            print e

    def getAdvertiseByAderID(self, ader_id):
        try:
            data = self.advermodel.get_advertise_by_aderid(ader_id)
            # print data
            if data:
                self.data = data
                message = {
                    'retcode': 0,
                    'retmsg': 'catch advertise success'
                }
                return message
            else:
                message = {
                    'retcode': 3006,
                    'retmsg': 'have no this OFFER'
                }
                return message
        except Exception as e:
            print e

    def tranOffer(self, app_id, divide):

        for data in self.data:
            # print data
            if self.checkDuplication(app_id, data['ad_id']):
                continue
            else:
                offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                pid = random.randint(0,10)
                _url = CreateClickUrl(app_id, offer_id, pid)
                click_url = _url.createUrl()
                row = self.offermodel.trans_offer(offer_id, app_id, click_url, divide, data)

    def checkDuplication(self, app_id, ad_id):
        try:
            data = self.offermodel.check_duplicate_offer(app_id, ad_id)
            # print data
            if data:
                return True
            else:
                return False
        except Exception as e:
            print e
