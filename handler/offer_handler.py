# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado import gen

# import pymongo
# from tornado_mysql import pools
from db.pools import POOL
from db.mysql import connection
from db.serializers import OfferSerializer
from click_handler import createClickUrl
from rule_handler import specailRule

import sign_api

from pymysql import err
from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import string

class OfferHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        """
            查看任务
            判断条件：签名正确，账号状态为激活状态
        """
        verify_sign = None
        verify_app = None
        app_id = self.get_argument('app_id', None)
        sign = self.get_argument('sign', None)
        try:
            query = 'select callback_url, callback_token from channeler where sign="%s"' % sign
            cursor = yield POOL.execute(query)
            data = cursor.fetchall()
            sign_url = data[0][0] + '&sign=%s' % sign
            # print data
            verify = sign_api.verifySinature(sign_url, data[0][1])
            # print verify
            # base_url = data[0][2]
        except Exception as e:
            msg = {
                'errcode': -1,
                'errmsg': '签名错误'
            }
            self.write(msg)

        try:
            query = 'select app_id,status from application where app_id="%s"' % app_id
            cursor = yield POOL.execute(query)
            data = cursor.fetchall()
            if not data:
                msg = {
                    'errcode': -100,
                    'errmsg': 'app_id not exists, please check your app_id'
                }
                self.write(msg)
            elif data[0][1] == '1' or data[0][1] == 1:
                msg = {
                    'errcode': -101,
                    'errmsg': "Application didn't pass the verification"
                }
                self.write(msg)
            else:
                verify_app = True
        except Exception as e:
            msg = {
                'errcode': -2,
                'errmsg': '数据请求错误'
            }
            self.write(msg)

        if verify_sign and verify_app:
            query = 'select `offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,`category`,\
                `icon_url`,`preview_url`,`click_url`,`os`,`os_version`,`region`,`payout`,`payout_currency`,\
                `payout_type`,`creatives` from offer where app_id="%s"' % app_id
            # print query
            cursor = yield POOL.execute(query)
            data = cursor.fetchall()
            # print data[0]
            # for d in data:
            #     print d
            serializers = OfferSerializer(data)
            # print serializers
            response = {
                'status': 200,
                'msg': 'OK',
                'offer': serializers
            }
            self.write(response)

    @tornado.gen.coroutine
    def post(self):
        """
            创建任务-->通过app_id转化 adver与offer
        """
        verify = None
        app_id = self.get_argument('app_id', None)
        adver_id = self.get_argument('ad_id', None)
        tranfer = AdvertiseTransOffer(app_id, adver_id)
        data = tranfer.getAdvertise()
        if data:
            tranfer.tranOffer()
            self.write('任务创建成功')



class AdvertiseTransOffer(object):

    def __init__(self):
        self.data = None

    def getONEAdvertise(self, ad_id):
        query = 'select ad_id,ad_name,pkg_name,region,category,icon_url,preview_url,get_price,payout_type,os,\
            os_version,creatives,description,status from advertise where ad_id="%s"' % ad_id
        cursor = connection.cursor()
        cursor.execute(query)
        self.data = data = cursor.fetchall()
        return data

    def getRuleAdvertise(self, rule_id):
        sR = specailRule()
        rule_value = sR.getRule(rule_id)

        query = 'select ad_id,ad_name,pkg_name,region,category,icon_url,preview_url,get_price,payout_type,os,\
            os_version,creatives,description,status from advertise where get_price%s' % (rule_value)
        cursor = connection.cursor()
        cursor.execute(query)
        self.data = data = cursor.fetchall()
        # connection.close()
        return data

    def tranONEOffer(self, app_id, ad_id):
        offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        pid = random.randint(0,10)
        _url = createClickUrl(app_id, offer_id, pid)
        click_url = _url.createUrl()

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
        connection.close()

    def tranRuleOffer(self, app_id):

        # print len(self.data)
        for data in self.data:
            offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

            pid = random.randint(0,10)
            _url = createClickUrl(app_id, offer_id, pid)
            click_url = _url.createUrl()

            query = 'insert IGNORE into `offer` (`offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,`icon_url`,`preview_url`,`category`,`os`,`os_version`,`payout`,`payout_type`,`click_url`,`creatives`,`region`,`active`,`createdate`) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%f","%s","%s","%s","%s","1","%s")' % (offer_id,data['ad_name'],app_id,data['ad_id'],data['pkg_name'],data['icon_url'],data['preview_url'],data['category'],data['os'],data['os_version'],data['get_price'],data['payout_type'],click_url,data['creatives'],data['region'],datetime.utcnow())
            # print query
            try:
                cursor = connection.cursor()
                cursor.execute(query)
                connection.commit()
            except err.ProgrammingError as e:
                print e
        connection.close()