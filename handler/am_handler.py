# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from base import BaseHandler
from cookietoken_handler import EncryptPassword
from offer_handler import AdvertiseTransOffer
from channel_handler import ChannelStatus

from pymysql.err import ProgrammingError
from datetime import datetime
import os
import json


class AMSginup(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        am_name = self.get_argument('am_name', None)
        if am_name is None:
            raise tornado.web.MissingArgumentError('am_id')
        passwd = self.get_argument('passwd', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')
        _passwd = EncryptPassword(passwd)._hash_password(passwd)
        try:
            query = 'insert into am (`name`,`passwd`,`income`,`output`,`total`,`createdate`) values ("%s","%s","%f","%f","%f","%s")' % (am_name,_passwd,float(0),float(0),float(0),datetime.utcnow())
            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()
            if row:
                msg = {
                    'code': 0,
                    'msg': 'AM account created successfully'
                }
                self.write(msg)
            else:
                self.write_error(500)
        except ProgrammingError as e:
            print e

class AMtoMultiOffer(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = self.get_argument('app_id', None)
        channeler_id = self.get_argument('channeler_id', None)
        rule_id = self.get_argument('rule_id', None)

        verify_channel = ChannelStatus()
        if verify_channel.verifyStatusApp(channeler_id, app_id):
            tranform = AdvertiseTransOffer()
            getoffer = tranform.getRuleAdvertise(rule_id)
            tranform.tranRuleOffer(app_id)
            msg = {
                'code': 0,
                'msg': 'Offer create successfully'
            }
            self.write(msg)
        else:
            self.write_error(500)

class AMtoOneOffer(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = self.get_argument('app_id', None)
        ad_id = self.get_argument('ad_id', None)
        channeler_id = self.get_argument('channeler_id', None)
        rule_id = self.get_argument('rule_id', None)

        verify_channel = ChannelStatus()
        if verify_channel.verifyStatusApp(channeler_id, app_id):
            tranform = AdvertiseTransOffer()
            getoffer = tranform.getONEAdvertise(rule_id)
            tranform.tranONEOffer(app_id, ad_id)
            msg = {
                'code': 0,
                'msg': 'Offer创建成功'
            }
            self.write(msg)
        else:
            self.write_error(500)


class AMChannelOper(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        status = self.get_argument('status', None)
        if status is None:
            raise tornado.web.MissingArgumentError('status')
        channeler_id = self.get_argument('channeler_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('channeler_id')

        channel = ChannelStatus()
        status = channel.setStatus(status, channeler_id)
        if status['code'] == 6000 or status['code'] == '6000':
            message = {
                'code': 0,
                'msg': 'channeler status update successfully'
            }
            self.write(message)
        else:
            self.write_error(500)

class AMChanneler(BaseHandler):

    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        am_id = self.get_argument('am_id', None)
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')
        channeler_id = self.get_argument('channeler_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('channeler_id')

        try:
            query = 'update channeler set am_id="%s" where channeler_id="%s"' % (int(am_id), channeler_id)
            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()
            if row != 0 or row != '0':
                message = {
                    'code': 0,
                    'msg': 'getting your channeler'
                }
                self.write(message)
            else:
                message = {
                    'code': 4001,
                    'msg': 'have been your channeler'
                }
                self.write(message)
        except ProgrammingError as e:
            print e

class AMAppOper(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        channeler_id = self.get_argument('channeler_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('channeler_id')

        # cookie_secret = self.get_cookie('__cookies_token__')
        # print cookie_secret

        # 验证是否该下游存在这个APP
        try:
            query = 'select app_id, status from application where channeler_id="%s" and app_id="%s"' % (channeler_id,app_id)
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            if data:
                if data['status'] is None:
                    query = 'update application set status="%d" where app_id="%s"' % (1,app_id)
                    row = cursor.execute(query)
                    connection.commit()
                    if row != 0 or row != '0':
                        message = {
                            'code': 0,
                            'msg': 'APP active successfully'
                        }
                        self.write(message)
                    else:
                        message = {
                            'code': 4002,
                            'msg': 'APP has already actived'
                        }
                        self.write(message)
                else:
                    message = {
                        'code': 4002,
                        'msg': 'APP has already actived'
                    }
                    self.write(message)
            else:
                message = {
                        'code': 4003,
                        'msg': 'APP is not existed'
                    }
                self.write(message)

        except ProgrammingError as e:
            print e

class AMLogin(BaseHandler):

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
             query = 'select passwd,status from am where name="%s"' % (username)
             cursor = connection.cursor()
             cursor.execute(query)
             data = cursor.fetchone()

             if not EncryptPassword(data['passwd']).auth_password(passwd):
                message = {
                    'code': 4004,
                    'msg': 'wrong password, please check it'
                }
                #  print message
                self.write(message)
             else:
                if data['status'] == 1 or data['status'] == 0:
                    message = {
                        'code': 0,
                        'is_actived': 1,
                        'msg': 'success'
                    }
                    self.write(message)
                else:
                    message = {
                        'code': 4005,
                        'is_actived': 0,
                        'msg': 'failure'
                        }
                    self.write(message)
        except err.ProgrammingError as e:
            print e
