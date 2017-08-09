# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from base_handler import BaseHandler
from cookietoken_handler import EncryptPassword
from offer_handler import AdvertiseTransOffer
from channel_handler import ChannelStatus

from model.application_model import ApplicationModel
from model.channeler_model import ChannelModel
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
            db_conns = self.application.db_conns
            AMmodel = AccountManagerModel(db_conns['read'], db_conns['write'])
            row = AMmodel.signup_am(name, _passwd)
            if row:
                msg = {
                    'retcode': 0,
                    'retmsg': 'AM account created successfully'
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
        chn_id = self.get_argument('chn_id', None)
        rule_id = self.get_argument('rule_id', None)

        verify_channel = ChannelStatus()
        if verify_channel.verifyStatusApp(chn_id, app_id):
            tranform = AdvertiseTransOffer()
            getoffer = tranform.getRuleAdvertise(rule_id)
            tranform.tranRuleOffer(app_id)
            msg = {
                'retcode': 0,
                'retmsg': 'Offer create successfully'
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
        chn_id = self.get_argument('chn_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('chn_id')
        am_id = self.get_argument('am_id', None)
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')

        db_conns = self.application.db_conns
        chnmodel = ChannelModel(db_conns['read'], db_conns['write'])
        row = chnmodel.set_channeler_status(int(status), am_id, chn_id)
        if row:
            message = {
                'retcode': 0,
                'retmsg': 'channeler status update successfully'
            }
            self.write(message)
        else:
            self.write_error(500)

class AMAppOper(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = self.get_argument('chn_id', None)
        if channeler_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        # cookie_secret = self.get_cookie('__cookies_token__')
        # print cookie_secret

        # 验证是否该下游存在这个APP
        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_detail(app_id, chn_id)
            if data:
                if data['status'] is None:
                    row = appmodel.set_applicaiton_status(app_id)
                    message = {
                        'retcode': 0,
                        'retmsg': 'APP active successfully'
                    }
                    self.write(message)
                else:
                    message = {
                        'retcode': 4002,
                        'retmsg': 'APP has already actived'
                    }
                    self.write(message)
            else:
                message = {
                        'retcode': 4003,
                        'retmsg': 'APP is not existed'
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
        # username = tornado.escape.json_decode(self.current_user)

        passwd = self.get_argument('password', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')

        try:
            db_conns = self.application.db_conns
            AMmodel = AccountManagerModel(db_conns['read'], db_conns['write'])
            data = AMmodel.login_am(username, passwd)

            if not EncryptPassword(data['passwd']).auth_password(passwd):
                message = {
                    'retcode': 4004,
                    'retmsg': 'wrong password, please check it'
                }
                #  print message
                self.write(message)
            else:
                if int(data['status']) == 1:
                    message = {
                        'retcode': 0,
                        'retdata': {
                            'am_id': data['id'],
                            'is_logined': 1,
                        },
                        'retmsg': 'success'
                    }
                    try:
                        row = AMmodel.set_login_time(username)
                        if row:
                            self.set_current_user(data['id'])
                        self.write(message)
                    except err.ProgrammingError as e:
                        print e
                else:
                    message = {
                        'retcode': 4005,
                        'retdata': {
                            'is_logined': 0,
                        },
                        'retmsg': 'failure'
                        }
                    self.write(message)
        except err.ProgrammingError as e:
            print e
