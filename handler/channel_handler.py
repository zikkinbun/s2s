# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

import sign_api
from base import BaseHandler
from cookietoken_handler import EncryptPassword
from db.mysql import connection

from urlparse import urlparse
from datetime import datetime
from pymysql import err
import base64
import os
import json
import random
import string


class SignupChaneler(tornado.web.RequestHandler):

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

        _passwd = EncryptPassword(passwd)._hash_password(passwd)
        # print _passwd

        # verify = EncryptPassword('$p5k2$2537$.DgQhf0T$n1Inm0WuCOz23Y5FishcJe83NuXcUVpK').auth_password('test123')
        # print verify
        try:
            query = 'insert IGNORE into `channeler` (`name`, `passwd`, `contact`, `email`, `status`,`channeler_id`, `sign_up_date`) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (username, _passwd, contact, email, status, channeler_id, datetime.now())
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


class ChannelStatus(object):

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

class ChannelerLogin(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        # username = tornado.escape.json_decode(self.current_user)

        passwd = self.get_argument('passwd', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')

        try:
             query = 'select channeler_id,passwd,status from channeler where name="%s"' % (username)
             cursor = connection.cursor()
             cursor.execute(query)
             data = cursor.fetchone()
            #  verify = EncryptPassword(data['passwd']).auth_password(passwd)
            #  print verify, type(data['status'])
             if not EncryptPassword(data['passwd']).auth_password(passwd):
                 message = {
                    'code': 6002,
                    'msg': 'wrong password, please check it'
                 }
                #  print message
                 self.write(message)
             else:
                if int(data['status']) == 1 or int(data['status']) == 0:
                    message = {
                        'code': 0,
                        'chn_id': data['channeler_id'],
                        'msg': 'success'
                    }
                    self.write(message)
                else:
                    message = {
                        'code': 6003,
                        'msg': 'login fail, the account occur some exceptions'
                    }
                    # print message
                    self.write(message)
        except err.ProgrammingError as e:
            print e

class ChannelerLogout(BaseHandler):

	def get(self):
		self.clear_current_user()
        # self.redirect(self.get_argument("next", "/v1/chn/login"))
