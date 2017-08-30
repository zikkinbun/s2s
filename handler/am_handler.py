# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from cookietoken_handler import EncryptPassword
from offer_handler import AdvertiseTransOffer
from channel_handler import ChannelStatus

from model.application_model import ApplicationModel
from model.advertise_model import AdvertiseModel
from model.am_model import AccountManagerModel
from model.channeler_model import ChannelModel

from datetime import datetime
from urlparse import urlparse
from urllib import unquote_plus
import os
import json
import random
import string


class AMSginup(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        am_name = json.loads(self.request.body)['am_name']
        # am_name = self.get_argument('am_name', None)
        if am_name is None:
            raise tornado.web.MissingArgumentError('am_name')
        passwd = json.loads(self.request.body)['passwd']
        # passwd = self.get_argument('passwd', None)
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
        except Exception as e:
            print e

class AMChannelOper(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        status = json.loads(self.request.body)['status']
        # status = self.get_argument('status', None)
        if status is None:
            raise tornado.web.MissingArgumentError('status')
        chn_id = json.loads(self.request.body)['chn_id']
        # chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        db_conns = self.application.db_conns
        chnmodel = ChannelModel(db_conns['read'], db_conns['write'])
        row = chnmodel.set_channeler_status(int(status), chn_id)
        if row:
            message = {
                'retcode': 0,
                'retmsg': 'channeler status update successfully'
            }
            self.write(message)
        else:
            message = {
                'retcode': 4001,
                'retmsg': 'channeler is already actived'
            }
            self.write(message)

class AMCreateOfferByUnion(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # ader_id = self.get_argument('ader_id', None)
        ader_id = json.loads(self.request.body)['ader_id']
        if ader_id is None:
            raise tornado.web.MissingArgumentError('ader_id')
        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            checkout_data = appmodel.get_application_tranform(app_id)
            # print checkout_data
            if not checkout_data[0]['divide']:
                message = {
                    'retcode': 4010,
                    'retmsg': 'please setting the Deduction and Partition'
                }
                self.write(message)
            else:
                try:
                    AT = AdvertiseTransOffer()
                    catch_advertise = AT.getAdvertiseByAderID(ader_id)
                    # print catch_advertise['retcode']
                    if catch_advertise['retcode'] == 0 or catch_advertise['retcode'] == '0':
                        # print checkout_data[0]['divide']
                        msg = AT.tranOffer(app_id, checkout_data[0]['divide'])
                        message = {
                            'retcode': 0,
                            'retmsg': 'success to create offer'
                        }
                        self.write(message)
                    else:
                        message = {
                            'retcode': 4009,
                            'retmsg': 'catch advertise failed'
                        }
                        self.write(message)
                except Exception as e:
                    print e
                    msg = {
                        'retcode': 4008,
                        'retmsg': 'databases operate error'
                    }
                    self.write(msg)
        except Exception as e:
            print e
            msg = {
                'retcode': 4008,
                'retmsg': 'databases operate error'
            }
            self.write(msg)


class AMAppOper(BaseHandler):
    """

    """

    @tornado.gen.coroutine
    def post(self):
        app_id = json.loads(self.request.body)['app_id']
        # app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        # chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')
        status = json.loads(self.request.body)['status']
        # status = self.get_argument('status', None)
        if status is None:
            raise tornado.web.MissingArgumentError('status')

        # 验证是否该下游存在这个APP
        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_detail(app_id, chn_id)
            # print data
            if data:
                if data[0]['status'] is None:
                    row = appmodel.set_applicaiton_status(status, app_id)
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
        # username = self.get_argument('username', None)
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        # username = tornado.escape.json_decode(self.current_user)

        passwd = json.loads(self.request.body)['passwd']
        # passwd = self.get_argument('passwd', None)
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')
        # print passwd

        try:
            db_conns = self.application.db_conns
            AMmodel = AccountManagerModel(db_conns['read'], db_conns['write'])
            data = AMmodel.login_am(username, passwd)
            # print data[0]['passwd']
            if not EncryptPassword(data[0]['passwd']).auth_password(passwd):
                message = {
                    'retcode': 4004,
                    'retmsg': 'wrong password, please check it'
                }
                #  print message
                self.write(message)
            else:

                if int(data[0]['status']) == 1:
                    message = {
                        'retcode': 0,
                        'retdata': {
                            'am_id': data[0]['id'],
                            'is_logined': 1,
                        },
                        'retmsg': 'success'
                    }
                    try:
                        row = AMmodel.set_login_time(username)
                        # print row
                        if row:
                            self.set_current_user(data[0]['id'])
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
            print e
            message = {
                'retcode': 4006,
                'retmsg': 'this user is not existed'
            }
            self.write(message)

class AMChannelSignup(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        username = json.loads(self.request.body)['username']
        if username is None:
            raise tornado.web.MissingArgumentError('username')
        passwd = json.loads(self.request.body)['passwd']
        if passwd is None:
            raise tornado.web.MissingArgumentError('passwd')
        email = json.loads(self.request.body)['email']
        if email is None:
            raise tornado.web.MissingArgumentError('email')
        am_id = json.loads(self.request.body)['am_id']
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')

        status = 1 # verifing
        chn_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))

        _passwd = EncryptPassword(passwd)._hash_password(passwd)

        try:
            db_conns = self.application.db_conns
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = channelmodel.signup_chaneler(username, _passwd, email, status, chn_id, am_id)
            message = {
                'retcode': 0,
                'retdata': {
                    'chn_id': chn_id
                },
                'retmsg': 'success'
            }
            self.write(message)
        except Exception as e:
            msg = {
                'retcode': 4008,
                'retmsg': 'databases operate error'
            }
            self.write(msg)

class AMListChannel(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        am_id = json.loads(self.request.body)['am_id']
        # am_id = self.get_argument('am_id', None)
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')

        try:
            db_conns = self.application.db_conns
            channelmodel = ChannelModel(db_conns['read'], db_conns['write'])
            data = channelmodel.list_channeler(int(am_id))
            if data:
                message = {
                    'retcode': 0,
                    'retdata': data,
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 4007,
                    'retmsg': 'did not have chn belong to you'
                }
                self.write(message)
        except Exception as e:
            msg = {
                'retcode': 4008,
                'retmsg': 'databases operate error'
            }
            self.write(msg)
            # print e

class AMTestCallback(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # am_id = self.get_argument('am_id', None)
        am_id = json.loads(self.request.body)['am_id']
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')
        # edit_callback_url = self.get_argument('callback_url', None)
        am_id = json.loads(self.request.body)['callback_url']
        if edit_callback_url is None:
            raise tornado.web.MissingArgumentError('callback_url')

        try:
            client = tornado.httpclient.AsyncHTTPClient() # 异步回调
            headers = tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"})
            request = tornado.httpclient.HTTPRequest(edit_callback_url, "GET", headers)
            response = yield client.fetch(request)
        except Exception as e:
            self.write_error(500)

class AMList(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        try:
            db_conns = self.application.db_conns
            AMmodel = AccountManagerModel(db_conns['read'], db_conns['write'])
            data = AMmodel.get_am()
            if data:
                message = {
                    'retcode': 0,
                    'retdata': {
                        'am': data
                    },
                    'resmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except Exception as e:
            msg = {
                'retcode': 4008,
                'retmsg': 'databases operate error'
            }
            self.write(msg)

class AMCountAdIncome(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # ader_id = self.get_argument('ader_id', None)
        ader_id = json.loads(self.request.body)['ader_id']
        if ader_id is None:
            raise tornado.web.MissingArgumentError('ader_id')

        try:
            db_conns = self.application.db_conns
            admodel = AdvertiseModel(db_conns['read'], db_conns['write'])
            data = admodel.count_all_advertise_income_by_id(ader_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': data,
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except Exception as e:
            print e
            msg = {
                'retcode': 4008,
                'retmsg': 'databases operate error'
            }
            self.write(msg)

class AMIncome(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        am_id = self.get_argument('am_id', None)
        if am_id is None:
            raise tornado.web.MissingArgumentError('am_id')

        try:
            db_conns = self.application.db_conns
        except Exception as e:
            print e
            msg = {
                'retcode': 4008,
                'retmsg': 'databases operate error'
            }
            self.write(msg)
