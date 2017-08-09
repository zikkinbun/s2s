# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

# import pymongo
# from tornado_mysql import pools
from base_handler import BaseHandler
from model.application_model import ApplicationModel
from model.advertise_model import AdvertiseModel
from model.offer_model import OfferModel
from model.channeler_model import ChannelModel
from model.rule_model import RuleModel

from click_handler import CreateClickUrl
from rule_handler import SpecailRule

from utils.db_utils import TornDBConnector
from db import setting
import sign_api

from datetime import datetime
import os
import re
import json
import random
import string


class OfferHandler(BaseHandler):

    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        """
            查看任务
            判断条件：签名正确，账号状态为激活状态
        """
        verify_sign = None
        verify_app = None

        app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        sign = self.get_argument('accesskey', None)
        if sign is None:
            raise tornado.web.MissingArgumentError('accesskey')

        chn_id = ''
        db_conns = self.application.db_conns
        # 验证签名
        try:
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.verify_app_sign(app_id, sign)
            chn_id = data['chn_id']
            sign_url = data['callback_url'] + '&sign=%s' % sign
            verify_sign = sign_api.verifySinature(sign_url, data['callback_token'])
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
            data = offermodel.get_offer_by_app(app_id, sign)
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

class ListRunningOffer(BaseHandler):
    pass

class ListAllOffer(BaseHandler):

    def post(self):
        try:
            db_conns = self.application.db_conns
            offermodel = OfferModel(db_conns['read'], db_conns['write'])
            data = offermodel.get_all_offer()
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
        except err.Exception as e:
            print e

class AdvertiseTransOffer(object):

    def __init__(self):
        self.data = None
        self.db_conns = {}
        self.db_conns['read'] = TornDBConnector(setting.RELEASE['s2s']['read']['host'], setting.RELEASE['s2s']['read']['database'], setting.RELEASE['s2s']['read']['user'], setting.RELEASE['s2s']['read']['password'])
        self.db_conns['write'] = TornDBConnector(setting.RELEASE['s2s']['write']['host'], setting.RELEASE['s2s']['write']['database'], setting.RELEASE['s2s']['write']['user'], setting.RELEASE['s2s']['write']['password'])

    def getRuleAdvertise(self, rule_id):
        rule_value = None
        # sR = SpecailRule()
        # rule_value = sR.getRule(rule_id)
        db_conns = self.db_conns
        try:
            rulemodel = RuleModel(db_conns['read'], db_conns['write'])
            value = rulemodel.get_rule_by_id(rule_id)
            rule_value = value['value']
            # print rule_value
        except Exception as e:
            print e

        if re.search(ur'get_price', rule_value):
            try:
                params = re.split(' ', rule_value)
                # db_conns = self.db_conns
                advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
                self.data = data = advermodel.get_advertise_by_price(params)
                if data:
                    return data
            except err.ProgrammingError as e:
                print e
        elif re.search(ur'payout_type', rule_value):
            # print rule_value
            try:
                params = re.split(' ', rule_value)
                # db_conns = self.application.db_conns
                advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
                # print query
                self.data = data = advermodel.get_advertise_by_payout_type(params)
                if data:
                    return data
                else:
                    message = {
                        'retcode': 3006,
                        'retmsg': 'have no this OFFER'
                    }
            except err.ProgrammingError as e:
                print e
        else:
            msg = {
                'retcode': 3006,
                'retmsg': '重新选择规则'
            }
            return msg

    def tranRuleOffer(self, app_id):

        db_conns = self.db_conns
        offermodel = OfferModel(db_conns['read'], db_conns['write'])
        for data in self.data:
            # print data
            if self.checkDuplication(app_id, data['ad_id']):
                continue
            else:
                offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                pid = random.randint(0,10)
                _url = CreateClickUrl(app_id, offer_id, pid)
                click_url = _url.createUrl()
                row = offermodel.trans_offer_by_rule(offer_id, app_id, click_url, data)

    def checkDuplication(self, app_id, ad_id):
        try:
            db_conns = self.db_conns
            offermodel = OfferModel(db_conns['read'], db_conns['write'])
            data = offermodel.check_duplicate_offer(app_id, ad_id)
            # print data
            if data:
                return True
            else:
                return False
        except Exception as e:
            print e

class ListRunningOffer(BaseHandler):
    pass

class ListAllOffer(BaseHandler):
    pass

    # def post(self):
    #     try:
    #         query = 'select '
