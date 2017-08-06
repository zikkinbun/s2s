# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

import sign_api
from base import BaseHandler
from db.mysql import connection

from urlparse import urlparse
from datetime import datetime
from pymysql import err
import base64
import os
import json
import random
import string


class signupChaneler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        passwd = self.get_argument('passwd', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')
        email = self.get_argument('email', None)
        if email is None:
            raise tornado.web.MissingArgumentError('email')
        contact = self.get_argument('contact', None)
        if contact is None:
            raise tornado.web.MissingArgumentError('contact')

        status = 0 # verifing
        channeler_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        try:
            query = 'insert IGNORE into `channeler` (`name`, `passwd`, `contact`, `email`, `status`,`channeler_id`, `sign_up_date`) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (username, passwd, contact, email, status, channeler_id, datetime.now())
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            message = {
                'code': 0,
                'msg': '%s' % channeler_id
            }
            self.write(message)
        except err.ProgrammingError as e:
            msg = {
                'code': 6001,
                'mode': '/signup/',
                'msg': e
            }
            return msg

class setToken(tornado.web.RequestHandler):

    """
        callback_url = http://your_host/your_script?click_id={user_id}&sub_source_id={chn}&ip={ip}
    """

    @tornado.gen.coroutine
    def post(self):
        sign = None
        channeler_id = self.get_argument('channeler_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('channeler_id')

        # channeler_id = self.get_cookie('user_id', None)
        # if channeler_id is None:
        #     raise tornado.web.MissingArgumentError('channeler_id')

        offer_type = self.get_argument('offer_type', None)
        if offer_type is None:
            raise tornado.web.MissingArgumentError('offer_type')
        base_url = self.get_argument('base_url', None)
        if base_url is None:
            raise tornado.web.MissingArgumentError('base_url')
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
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            message = {
                'code': 0,
                'msg': 'Your Signature is %s' % sign
            }
            self.write(message)
        except err.ProgrammingError as e:
            print e


class createApplication(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        app_name = self.get_argument('app_name', None)
        if app_name is None:
            raise tornado.web.MissingArgumentError('app_name')
        pkg_name = self.get_argument('pkg_name', None)
        if pkg_name is None:
            raise tornado.web.MissingArgumentError('pkg_name')
        category = self.get_argument('category', None)
        if category is None:
            raise tornado.web.MissingArgumentError('category')
        platform = self.get_argument('os', None)
        if platform is None:
            raise tornado.web.MissingArgumentError('platform')
        url = self.get_argument('url', [])
        if url is None:
            raise tornado.web.MissingArgumentError('url')
        description = self.get_argument('description', None)
        if description is None:
            raise tornado.web.MissingArgumentError('description')
        channeler_id = self.get_argument('channeler_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('channeler_id')

        # channeler_id = self.get_argument('channeler_id', None)
        # if channeler_id is None:
        #     raise tornado.web.MissingArgumentError('channeler_id')

        app_id = base64.b64encode(os.urandom(16))
        app_secret = base64.b64encode(os.urandom(16))

        try:
            query = 'insert into application (app_id,app_name,app_secret,pkg_name,platform,category,\
                url,is_stored,description,channeler_id,createdate) values ("%s","%s","%s","%s","%s","%s",\
                "%s","%s","%s","%s","%s")' % (app_id,app_name,app_secret,pkg_name,platform,category,url,is_stored,\
                description,channeler_id,datetime.utcnow())

            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()

            if row:
                msg = {
                    'code': 0,
                    'msg': 'APP is created,please contract your account manager to active your APP',
                    'App_id': app_id,
                    'App_secret': app_secret
                    }
                self.write(msg)
            else:
                msg = {
                    'msgcode': 6002,
                    'msgdata': 'APP created failure'
                }
                self.write(msg)
        except err.ProgrammingError as e:
            print e
        finally:
            connection.close()

class channelStatus(object):

    def getStatus(self, channeler_id):
        try:
            query = 'select status from channeler where channeler_id="%s"' % channeler_id
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            if data:
                return data['status']
        except err.ProgrammingError as e:
            print e

    def setStatus(self, status, channeler_id):
        try:
            query = 'update channeler set status="%d" where channeler_id="%s"' % (int(status), channeler_id)
            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()
            if row:
                msg = {
                    'code': 0,
                }
                return msg
        except err.ProgrammingError as e:
            return e
        # finally:
        #     connection.close()

    def verifyStatusApp(self, channeler_id, app_id):
        """
            验证当前下游的状态和 APP 是否可用
        """
        try:
            status_query = 'select a.status,b.app_id from channeler a, application b where a.channeler_id="%s" and b.channeler_id="%s"' % (channeler_id, channeler_id)
            cursor = connection.cursor()
            cursor.execute(status_query)
            data = cursor.fetchone()

            if int(data['status']) == 1 and data['app_id'] == app_id:
                return True
            else:
                return False
        except err.ProgrammingError as e:
            print e
        # finally:
        #     cursor.close()
        #     connection.close()

class channelerLogin(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        username = tornado.escape.json_decode(self.current_user)

        passwd = self.get_argument('password', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')

        try:
             query = 'select channeler_id,status from channeler where name="%s" and passwd="%s"' % (username, passwd)
             cursor = connection.cursor()
             cursor.execute(query)
             data = cursor.fetchone()
             if data['status'] == 1 or data['status'] == 0:
                 message = {
                    'code': 0,
                    'channeler_id': data['channeler_id'],
                    'msg': 'success'
                 }
                 self.write(message)
             else:
                 message = {
                    'code': 6003,
                    'msg': 'login fail'
                 }
                 self.write_error(message)
        except err.ProgrammingError as e:
            print e

class channelerLogout(BaseHandler):

	def get(self):
		self.clear_current_user()
        self.redirect(self.get_argument("next", "/v1/chn/login"))
