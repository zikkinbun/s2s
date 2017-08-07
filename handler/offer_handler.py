# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

# import pymongo
# from tornado_mysql import pools
from base import BaseHandler
from db.mysql import connection
from db.serializers import OfferSerializer
from click_handler import CreateClickUrl
from rule_handler import SpecailRule

import sign_api

from pymysql import err
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

        # xsrf_token = self.check_xsrf_cookie()

        # 验证签名
        try:
            query = 'select callback_url, callback_token from channeler where sign="%s"' % sign
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            sign_url = data['callback_url'] + '&sign=%s' % sign
            # print data
            verify_sign = sign_api.verifySinature(sign_url, data['callback_token'])
            # base_url = data[0][2]
        except Exception as e:
            msg = {
                'code': 3001,
                'msg': '签名错误'
            }
            self.write(msg)

        # 验证下游的 APP 状态是否可用
        try:
            query = 'select a.channeler_id,a.status,b.status as channeler_status from application a, channeler b where a.app_id="%s" and b.sign="%s"' % (app_id, sign)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            # print data
            if not data:
                msg = {
                    'code': 3002,
                    'msg': 'app_id not exists, please check your app_id'
                }
                self.write(msg)
            elif data['status'] == 0 or data['status'] is None:
                msg = {
                    'code': 3003,
                    'msg': "Application didn't pass the verification, please contact your accout manager"
                }
                self.write(msg)
            elif data['channeler_status'] == 0 or data['channeler_status'] is None:
                msg = {
                    'code': 3004,
                    'msg': "Channeler didn't pass the verification, please contact your accout manager"
                }
                self.write(msg)
            else:
                verify_app = True
        except Exception as e:
            msg = {
                'code': 3005,
                'msg': 'Data request Error'
            }
            self.write(msg)

        # print verify_sign, verify_app
        if verify_sign and verify_app:
            query = 'select `offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,`category`,\
                `icon_url`,`preview_url`,`click_url`,`os`,`os_version`,`region`,`payout`,`payout_currency`,\
                `payout_type`,`creatives` from offer where app_id="%s"' % app_id
            # print query
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            serializers = OfferSerializer(data)
            # print serializers
            response = {
                'status': 0,
                'msg': 'OK',
                'offer': serializers
            }
            self.write(response)

class AdvertiseTransOffer(object):

    def __init__(self):
        self.data = None

    def getONEAdvertise(self, ad_id):
        try:
            query = 'select ad_id,ad_name,pkg_name,region,category,icon_url,preview_url,get_price,payout_type,os,\
                os_version,creatives,description,status from advertise where ad_id="%s"' % ad_id
            cursor = connection.cursor()
            cursor.execute(query)
            self.data = data = cursor.fetchall()
            return data
        except err.ProgrammingError as e:
            print e

    def getRuleAdvertise(self, rule_id):
        sR = specailRule()
        rule_value = sR.getRule(rule_id)

        if re.search(ur'[0-9]', rule_value):
            try:
                query = 'select ad_id,ad_name,pkg_name,region,category,icon_url,preview_url,get_price,payout_type,os,\
                os_version,creatives,description,status from advertise where get_price%s' % (rule_value[2:])
                cursor = connection.cursor()
                cursor.execute(query)
                self.data = data = cursor.fetchall()
                if data:
                    return data
            except err.ProgrammingError as e:
                print e
        elif re.search(ur'[CPASI]', rule_value):
            # print rule_value
            try:
                query = 'select ad_id,ad_name,pkg_name,region,category,icon_url,preview_url,get_price,payout_type,os,\
                os_version,creatives,description,status from advertise where payout_type="%s"' % (rule_value[4:])
                # print query
                cursor = connection.cursor()
                cursor.execute(query)
                self.data = data = cursor.fetchall()
                if data:
                    return data
                else:
                    message = {
                        'code': 3006,
                        'msg': 'have no this OFFER'
                    }
            except err.ProgrammingError as e:
                print e
        else:
            msg = {
                'code': 3006,
                'msg': '重新选择规则'
            }
            return msg

    def tranONEOffer(self, app_id, ad_id):
        if self.checkDuplication(app_id, data['ad_id']):
            message = {
                'code': 3007,
                'msg': 'offer hava been existed'
            }
            return message
        else:
            offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

            pid = random.randint(0,10)
            _url = createClickUrl(app_id, offer_id, pid)
            click_url = _url.createUrl()
            try:
                query = 'insert into `offer` (`offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,\
                    `icon_url`,`preview_url`,`category`,`os`,`os_version`,`payout`,\
                    `payout_type`,`click_url`,`creatives`,`region`,`active`,`createdate`) values ("%s","%s","%s","%s","%s",\
                    "%s","%s","%s","%s","%s","%f","%s","%s","%s","%s","1","%s")' % (offer_id,self.data[0]['ad_name'],\
                    app_id,ad_id,self.data[0]['pkg_name'],self.data[0]['icon_url'],\
                    self.data[0]['preview_url'],self.data[0]['category'],self.data[0]['os'],\
                    self.data[0]['os_version'],self.data[0]['get_price'],self.data[0]['payout_type'],\
                    click_url,self.data[0]['creatives'],self.data[0]['region'],datetime.utcnow())
                    # print query
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            except err.ProgrammingError as e:
                print e
            finally:
                connection.close()

    def tranRuleOffer(self, app_id):

        for data in self.data:
            if self.checkDuplication(app_id, data['ad_id']):
                continue
            else:
                offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                pid = random.randint(0,10)
                _url = createClickUrl(app_id, offer_id, pid)
                click_url = _url.createUrl()
                try:
                    query = 'insert IGNORE into `offer` (`offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,`icon_url`,`preview_url`,`category`,`os`,`os_version`,`payout`,`payout_type`,`click_url`,`creatives`,`region`,`active`,`createdate`) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%f","%s","%s","%s","%s","1","%s")' % (offer_id,data['ad_name'],app_id,data['ad_id'],data['pkg_name'],data['icon_url'],data['preview_url'],data['category'],data['os'],data['os_version'],data['get_price'],data['payout_type'],click_url,data['creatives'],data['region'],datetime.utcnow())
                    # print query
                    cursor = connection.cursor()
                    cursor.execute(query)
                    connection.commit()
                except err.ProgrammingError as e:
                    print e
        # connection.close()

    def checkDuplication(self, app_id, ad_id):
        try:
            query = 'select offer_id from offer where app_id="%s" and advertise_id="%s"' % (app_id,ad_id)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            if data:
                return True
            else:
                return False
        except err.ProgrammingError as e:
            print e

class ListRunningOffer(BaseHandler):
    pass

class ListAllOffer(BaseHandler):
    pass

    # def post(self):
    #     try:
    #         query = 'select '
