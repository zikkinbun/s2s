# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

# import pymongo
# from tornado_mysql import pools
from db import POOL
from serializers import OfferSerializer

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
        app_id = self.get_argument('app_id', None)
        sign = self.get_argument('sign', None)
        page_size = self.get_argument('page_size', None)
        page = self.get_argument('page', None)
        os = self.get_argument('os', None)

        verify = sign_api.getSign(sign)
        # print verify
        if verify:
            sql = 'select a.*,b.app_id,b.format,b.height,b.width,b.url,c.mac,c.idfa,c.udid,c.ip,c.imei  from offer a, catch_package_img b, device c where a.creatives_id = b.id and a.mandatory_device_id = c.id'
            callback_cursor = yield POOL.execute(sql)
            callback_tup_data = callback_cursor.fetchall()
            callback_data = callback_tup_data[0]
            # print len(callback_data)
            # print json.dumps(callback_data)
            data = OfferSerializer(callback_data, page, page_size)

            client = tornado.httpclient.AsyncHTTPClient() # 异步回调
            headers = tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"})
            request = tornado.httpclient.HTTPRequest('http://127.0.0.1:8001', "POST", headers, data)
            response = yield client.fetch(request)
            raise gen.Return(response)
        else:
            self.write("invilid sign parameter, please check")

    @tornado.gen.coroutine
    def post(self):
        offer_req = {
            'adver_id': self.get_argument('adver_id', None),
            'sign': self.get_argument('sign', None)
        }
