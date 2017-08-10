# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

import sign_api
from base_handler import BaseHandler
from cookietoken_handler import EncryptPassword
from model.channeler_model import ChannelModel

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from db import setting

from urlparse import urlparse
from datetime import datetime
from pymysql import err
import base64
import os
import json
import random
import string


class SignupChaneler(BaseHandler):

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
        chn_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        _passwd = EncryptPassword(passwd)._hash_password(passwd)
        # print _passwd

        # verify = EncryptPassword('$p5k2$2537$.DgQhf0T$n1Inm0WuCOz23Y5FishcJe83NuXcUVpK').auth_password('test123')
        # print verify
        try:
            db_conns = self.application.db_conns
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = channelmodel.signup_chaneler(username, _passwd, email, contact, status, chn_id)
            message = {
                'retcode': 0,
                'retdata': {
                    'chn_id': chn_id
                },
                'retmsg': 'success'
            }
            self.write(message)
        except err.ProgrammingError as e:
            msg = {
                'retcode': 6001,
                'retdata': {
                    'model': '/signup/'
                },
                'retmsg': 'failure'
            }
            self.write(message)


class ChannelStatus(object):

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()

    def getStatus(self, chn_id):
        try:
            db_conns = self.db_conns
            # sql = 'select a.status as chn_status, b.status as app_status from channeler a, application b where a.chn_id=%s and b.chn_id=%s and b.app_id=%s'

            # data = self._conn_read.query(sql, chn_id, chn_id, app_id)[0]
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = channelmodel.get_channeler_status(chn_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'status': data['status']
                    },
                    'retmsg': 'success'
                }
                return message
        except err.ProgrammingError as e:
            print e

    def setStatus(self, status, chn_id):
        try:
            db_conns = self.db_conns
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            row = channelmodel.set_channeler_status(status, chn_id)
            if row:
                msg = {
                    'retcode': 0,
                    'retmsg': 'success'
                }
                return msg
        except err.ProgrammingError as e:
            return e

    def verifyStatusApp(self, chn_id, app_id):
        """
            验证当前下游的状态和 APP 是否可用
        """
        try:
            db_conns = self.db_conns
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = channelmodel.verify_app_status(chn_id, app_id)
            # print data
            if int(data['chn_status']) == 1 and int(data['app_status']) == 1:
                return True
            else:
                return False
        except err.ProgrammingError as e:
            print e


class ChannelerLogin(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        # chn_id = tornado.escape.json_decode(self.get_current_user)

        passwd = self.get_argument('passwd', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')

        try:
            db_conns = self.application.db_conns
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = channelmodel.get_login_chner(username, passwd)
            #  verify = EncryptPassword(data['passwd']).auth_password(passwd)
            #  print verify, type(data['status'])
            if not EncryptPassword(data['passwd']).auth_password(passwd):
                 message = {
                    'retcode': 6002,
                    'retmsg': 'wrong password, please check it'
                 }
                 self.write(message)
            else:
                if int(data['status']) == 1 or int(data['status']) == 0:
                    message = {
                        'retcode': 0,
                        'retdata': {
                            'chn_id': data['chn_id'],
                        },
                        'retmsg': 'success'
                    }
                    try:
                        row = channelmodel.set_login_time(username)
                        if row:
                            self.set_current_user(data['chn_id'])
                        self.write(message)
                    except err.ProgrammingError as e:
                        print e
                else:
                    message = {
                        'retcode': 6003,
                        'retmsg': 'login fail, the account occur some exceptions'
                    }
                    self.write(message)
        except err.ProgrammingError as e:
            print e

class ChannelerLogout(BaseHandler):

	def get(self):
		self.clear_current_user()
