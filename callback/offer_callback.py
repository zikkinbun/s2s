# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado import gen

# import pymongo
from db.mysql import connection
from db.redis_pool import r
from handler.click_handler import createClickUrl

import sign_api

from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import requests

class OfferCallback(tornado.web.RequestHandler):
    """
        下游给过来的callback_url
        http://127.0.0.1:8001/callback?sign={sign}&click_id={user_id}
    """

    @tornado.gen.coroutine
    def get(self):
        click = searchValidClick()
        callback_url, sign, app_click_id = click.getValidClick()
        url_parse = urlparse(callback_url)
        click_url = callback_url.replace(url_parse.query, 'click_id=%s' % app_click_id)
        url = click_url + '&sign=%s' % sign
        # print url
        client = tornado.httpclient.AsyncHTTPClient() # 异步回调
        headers = tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"})
        request = tornado.httpclient.HTTPRequest(url, "GET", headers)
        response = yield client.fetch(request)
        self.write(response.body)

class searchValidClick(object):

    def getClick(self):
        callback_url = None
        sign = None
        app_click_id = None

        try:
            valid_click_query = 'select click_id, app_click_id, app_id from track_click where valid="%d"' % int(1)
            cursor = connection.cursor()
            cursor.execute(valid_click_query)
            valid_datas = cursor.fetchall()
            for data in valid_datas:
                callback_url_query = 'select callback_url,sign from channeler where channeler_id=(select channeler_id from application where app_id="%s")' % (data['app_id'])
                cursor.execute(callback_url_query)
                dataset = cursor.fetchall()
                callback_url = dataset['callback_url']
                sign = dataset['sign']
                app_click_id = data['app_click_id']
                
            return callback_url, sign, app_click_id
        except err.ProgrammingError as e:
            print e

    def callback(self, click_id, sign, callback_url):
        params = {
            'click_id': click_id,
            'sign': sign
        }
        try:
            r = requests.get(url, params=params)
        except requests.exceptions.HTTPError as e:
            print e
