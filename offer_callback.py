# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado import gen

# import pymongo
# from tornado_mysql import pools
from pools import POOL
from mysql import connection
from click_handler import createClickUrl

import sign_api

from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random

class OfferCallback(tornado.web.RequestHandler):
    """
        下游给过来的callback_url
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
        for data in valid_datas:
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
