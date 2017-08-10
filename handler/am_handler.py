# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from base_handler import BaseHandler
from cookietoken_handler import EncryptPassword
from offer_handler import AdvertiseTransOffer
from channel_handler import ChannelStatus

from model.application_model import ApplicationModel
from model.am_model import AccountManagerModel
from model.channeler_model import ChannelModel
from pymysql.err import ProgrammingError
from datetime import datetime
import os
import json
from urlparse import urlparse
from urllib import unquote_plus


class AMSginup(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        am_name = json.loads(self.request.body)['am_name']
        if am_name is None:
            raise tornado.web.MissingArgumentError('am_name')
        passwd = json.loads(self.request.body)['passwd']
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')
        _passwd = EncryptPassword(passwd)._hash_password(passwd)
        # print _passwd
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

class AMtoMultiOffer(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')
        rule_id = json.loads(self.request.body)['rule_id']
        if rule_id is None:
            raise tornado.web.MissingArgumentError('rule_id')

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
        status = json.loads(self.request.body)['status']
        if status is None:
            raise tornado.web.MissingArgumentError('status')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')
        am_id = json.loads(self.request.body)['am_id']
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
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
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

        except Exception as e:
            message = {
                'retcode': 4003,
                'retmsg': 'APP is not existed'
            }
            self.write(message)

class AMLogin(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = json.loads(self.request.body)['username']
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        # username = tornado.escape.json_decode(self.current_user)

        passwd = json.loads(self.request.body)['passwd']
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')
        # print passwd

        # token = self.get_cookie('_xsrf')
        # print token

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
                        # print row
                        if row:
                            self.set_current_user(data['id'])
                        self.write(message)
                    except Exception as e:
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
        except Exception as e:
            if e == 'list index out of range':
                message = {
                    'retcode': 4006,
                    'retmsg': 'this user is not existed'
                }
                self.write(message)
