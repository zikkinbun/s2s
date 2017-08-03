# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
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
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            self.write('Your ID is %s' % channeler_id)
        except err.ProgrammingError as e:
            msg = {
                'code': 6001,
                'mode': '/signup/',
                'msg': e
            }
            return msg
        finally:
            connection.close()

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
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            message = {
                'code': 6000,
                'msg': 'Your Signature is %s' % sign
            }
            self.write(message)
        except err.ProgrammingError as e:
            print e


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
                    'msgcode': 6000,
                    'msgdata': 'APP创建成功',
                    'App_id': app_id,
                    'App_secret': app_secret
                    }
                self.write(msg)
            else:
                msg = {
                    'msgcode': 6002,
                    'msgdata': 'APP创建失败'
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
            query = 'update channeler set status=%d where channeler_id=%s' % (int(status), channeler_id)
            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()
            if row:
                msg = {
                    'msgcode': 6000,
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
