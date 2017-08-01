# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
from db.pools import POOL

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

        try:
            query = 'insert into channeler (name, passwd, contact, email, am_id, status, channeler_id, sign_up_date  \
                ) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s" )' % (username, passwd, contact, email, \
                am_id, status, channeler_id, datetime.now())
            print query
            cursor = yield POOL.execute(query)
            if cursor:
                self.write('Your ID is %s' % channeler_id)
        except Exception as e:
            msg = {
                'errcode': -2,
                'errmode': '/signup/',
                'errmsg': '数据库插入出错'
            }
            self.write(msg)

class AMsetup(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        am_name = self.get_argument('am_name', None)
        income = self.get_argument('income', None)
        output = self.get_argument('output', None)
        total = self.get_argument('total', None)

        query = 'insert into am (`name`,`income`,`output`,`total`,`createdate`) values ("%s","%f","%f","%f","%s")' % (am_name,float(income),float(output),float(total),datetime.utcnow())
        cursor = yield POOL.execute(query)
        if cursor:
            self.write('AM account created successfully')


class setToken(tornado.web.RequestHandler):

    """
        callback_url = http://your_host/your_script?click_id={user_id}&sub_source_id={chn}&ip={ip}
    """

    @tornado.gen.coroutine
    def post(self):
        sign = None
        channeler_id = self.get_argument('channeler_id', None)
        offer_type = self.get_argument('offer_type', None)
        base_url = self.get_argument('base_url', None)
        callback_token = base64.b64encode(os.urandom(24)) # 包括 app_secret和用户 token
        # callback_url = base_url + 'callback?type=%s&channeler_id=%s' % (offer_type, channeler_id)
        # print callback_url
        url = sign_api.sign_url(base_url, callback_token)
        # print url
        url_parse = urlparse(url)
        query = url_parse.query
        query_array = query.split('&')
        for group in query_array:
            k, v = group.split('=')
            if k == 'sign':
                sign = v

        query = 'update channeler set base_url="%s", callback_url="%s", callback_token="%s", sign="%s" where channeler_id="%s"' % (base_url, base_url, callback_token, sign, channeler_id)
        # print query
        cursor = yield POOL.execute(query)
        if cursor:
            self.write('Your Signature is %s' % sign)

class createApplication(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        app_name = self.get_argument('app_name', None)
        pkg_name = self.get_argument('pkg_name', None)
        category = self.get_argument('category', None)
        platform = self.get_argument('os', None)
        url = self.get_argument('url', None)
        description = self.get_argument('description', None)
        is_stored = self.get_argument('is_stored', None)
        channeler_id = self.get_argument('channeler_id', None)

        app_id = base64.b64encode(os.urandom(16))
        app_secret = base64.b64encode(os.urandom(16))

        query = 'insert into application (app_id,app_name,app_secret,pkg_name,platform,category,\
            url,is_stored,description,channeler_id,createdate) values ("%s","%s","%s","%s","%s","%s",\
            "%s","%s","%s","%s","%s")' % (app_id,app_name,app_secret,pkg_name,platform,category,url,is_stored,\
            description,channeler_id,datetime.utcnow())

        cursor = yield POOL.execute(query)
        if cursor:
            msg = {
                'msgcode': 0,
                'msgdata': 'APP创建成功',
                'App_id': app_id,
                'App_secret': app_secret
            }
            self.write(msg)
        else:
            msg = {
                'msgcode': -1,
                'msgdata': 'APP创建失败'
            }
