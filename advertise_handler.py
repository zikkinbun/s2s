# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

# import pymongo
# from tornado_mysql import pools
from db import POOL

import sign_api

from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import string

class Advertises(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        ad_id = self.get_argument('ad_id', None)
        sign = self.get_argument('sign', None)
        if sign_api.ReverifySign(sign):
            query_1 = 'select '

    @tornado.gen.coroutine
    def post(self):
        ad_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        ad_name = self.get_argument('ad_name', None)
        owner = self.get_argument('owner', None)
        region = self.get_argument('region', None)
        access_price = self.get_argument('access_price', None)
        put_price = self.get_argument('put_price', None)
        status = self.get_argument('status', None)
        updatetime = self.get_argument('updatetime', None)

        query = 'insert into advertises (ad_id, ad_name, owner, region, access_price, put_price, \
            status, updatetime) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % ( \
                ad_id, ad_name, owner, region, access_price, put_price, status, datetime.now())
        cursor = yield POOL.execute(query)
        if cursor:
            self.write('create one piece of advertise successfully')

class Advertiser(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        ader_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        name = self.get_argument('name', None)
        is_pulled = self.get_argument('is_pulled', None)

        query = 'insert into advertiser (ader_id, name, is_pulled) values ("%s", "%s", "%s")' % (ader_id, name, is_pulled)
        cursor = yield POOL.execute(query)
        if cursor:
            self.write('Add Advertiser successfully')

class Advertise_data(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        info = dict()
