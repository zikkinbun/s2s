# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
from db import POOL

from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import string


class signupChaneler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        sign = None
        username = self.get_argument('username', None)
        passwd = self.get_argument('passwd', None)
        email = self.get_argument('email', None)
        contact = self.get_argument('contact', None)
        status = self.get_argument('status', None)
        am_id = self.get_argument('am_id', None)
        channeler_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))



        query = 'insert into channeler (name, passwd, contact, email, am_id, status, channeler_id, sign_up_date  \
            ) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )' % (username, passwd, contact, email, \
            am_id, status, channeler_id, datetime.now())
        # print query
        cursor = yield POOL.execute(query)
        if cursor:
            self.write('Your ID is %s' % channel_id)

class setToken(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        sign = None
        channeler_id = self.get_argument('channeler_id', None)
        offer_type = self.get_argument('offer_type', None)
        base_url = self.get_argument('base_url', None)
        callback_token = base64.b64encode(os.urandom(24)) # 包括 app_secret和用户 token
        callback_url = base_url + '?type=%s&channeler_id=%s' % (offer_type, channeler_id)
        url = sign_api.sign_url(callback_url, callback_token)

        url_parse = urlparse(url)
        query = url_parse.query
        query_array = query.split('&')
        for group in query_array:
            k, v = group.split('=')
            if k == 'sign':
                sign = v

        query = 'update channeler set base_url="%s", callback_url="%s", callback_token="%s", sign="%s" where channeler_id="%s"' % (base_url, callback_url, callback_token, sign, channeler_id)
        # print query
        cursor = yield POOL.execute(query)
        if cursor:
            self.write('Your Signature is %s' % sign)
