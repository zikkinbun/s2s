# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado import gen

# import pymongo
# from tornado_mysql import pools
from pools import POOL
from mysql import connection
from serializers import OfferSerializer
from click_handler import createClickUrl

import sign_api

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
        verify = None
        app_id = self.get_argument('app_id', None)
        sign = self.get_argument('sign', None)
        try:
            query = 'select callback_url, callback_token, base_url from channeler where sign="%s"' % sign
            cursor = yield POOL.execute(query)
            data = cursor.fetchall()
            verify = sign_api.verifySinature(data[0][0], data[0][1])
            base_url = data[0][2]
        except Exception as e:
            msg = {
                'errcode': -1,
                'errmsg': '签名错误'
            }
            self.write(msg)

        if verify:
            query = 'select `offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,`category`,\
                `icon_url`,`preview_url`,`click_url`,`os`,`os_version`,`payout`,`payout_currency`,\
                `payout_type`,`creatives` from offer where app_id="%s"' % app_id
            cursor = yield POOL.execute(query)
            data = cursor.fetchall()
            serializers = OfferSerializer(data)
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
        offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        tittle = self.get_argument('tittle', None)
        app_id = self.get_argument('app_id', None)
        adver_id = self.get_argument('adver_id', None)
        pkgname = self.get_argument('pkgname', None)
        category = self.get_argument('category', None)
        icon_url = self.get_argument('icon_url', None)
        preview_url = self.get_argument('preview_url', None)
        platform = self.get_argument('os', None)
        os_version = self.get_argument('os_version', None)
        payout = self.get_argument('payout', None)
        payout_type = self.get_argument('payout_type', None)
        creatives = self.get_argument('creatives', None)

        pid = random.randint(0,10)
        _url = createClickUrl(adver_id, app_id, pid)
        click_url = _url.createUrl()

        query = 'insert into offer (`offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,\
            `icon_url`,`preview_url`,`click_url`,`category`,`os`,`os_version`,`payout`,\
            `payout_type`,`creatives`) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s",\
            "%s","%s","%f","%s","%s")' % (offer_id,tittle,app_id,adver_id,pkgname,icon_url,\
            preview_url,click_url,category,platform,os_version,float(payout),payout_type,datetime.utcnow())

        cursor = yield POOL.execute(query)
        if cursor:
            self.write('offer create successfully')

class AdvertiseTransOffer(object):

    def __init__(self, app_id, adver_id):
        self.app_id = app_id
        self.adver_id = adver_id
        self.data = None

    def getAdvertise(self):
        query = 'select ad_id,ad_name,pkg_name,region,category,icon_url,preview_url,get_price,payout_type,os,\
            os_version,creatives,description,status from advertise where ad_id="%s"' % self.adver_id
        cursor = connection.cursor()
        cursor.execute(query)
        self.data = data = cursor.fetchall()
        return data

    def tranOffer(self):
        offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        pid = random.randint(0,10)
        _url = createClickUrl(self.adver_id, self.app_id, pid)
        click_url = _url.createUrl()

        query = 'insert into offer (`offer_id`,`tittle`,`app_id`,`advertise_id`,`pkgname`,\
            `icon_url`,`preview_url`,`category`,`os`,`os_version`,`payout`,\
            `payout_type`,`click_url`,`creatives`,`createdate`) values ("%s","%s","%s","%s","%s",\
            "%s","%s","%s","%s","%s","%f","%s","%s","%s","%s")' % (offer_id,self.data[0]['ad_name'],\
            self.app_id,self.adver_id,self.data[0]['pkg_name'],self.data[0]['icon_url'],\
            self.data[0]['preview_url'],self.data[0]['category'],self.data[0]['os'],\
            self.data[0]['os_version'],self.data[0]['get_price'],self.data[0]['payout_type'],\
            click_url,self.data[0]['creatives'],datetime.utcnow())
        # print query
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

class OfferCallback(tornado.web.RequestHandler):
    """
        http://127.0.0.1:8001/callback?sign={sign}&click_id={user_id}
    """

    def getValidClick(self):
        callback_url = None
        sign = None
        app_click_id = None
        valid_click_query = 'select click_id, app_click_id, app_id from track_click where valid=1'
        cursor = connection.cursor()
        cursor.execute(valid_click_query)
        valid_datas = cursor.fetchall()
        for data in valid_datas:    ``
            callback_url_query = 'select callback_url,sign from channeler where channeler_id=(select channeler_id from application where app_id="%s")' % (data['app_id'])
            cursor.execute(callback_url_query)
            dataset = cursor.fetchall()
            callback_url = dataset[0]['callback_url']
            sign = dataset[0]['sign']
            app_click_id = data['app_click_id']
            # print callback_url, sign
        return callback_url, sign, app_click_id

    @tornado.gen.coroutine
    def get(self):
        callback_url, sign, app_click_id = self.getValidClick()
        url_parse = urlparse(callback_url)
        click_url = callback_url.replace(url_parse.query, 'click_id=%s' % app_click_id)
        url = click_url + '&sign=%s' % sign
        # print url
        client = tornado.httpclient.AsyncHTTPClient() # 异步回调
        headers = tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"})
        request = tornado.httpclient.HTTPRequest(url, "GET", headers)
        response = yield client.fetch(request)
        self.write(response.body)
