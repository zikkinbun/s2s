# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from offer_handler import AdvertiseTransOffer
from channel_handler import channelStatus

from pymysql.err import ProgrammingError
from datetime import datetime
import os
import json


class AMsetup(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        am_name = self.get_argument('am_name', None)
        income = self.get_argument('income', None)
        output = self.get_argument('output', None)
        total = self.get_argument('total', None)

        try:
            query = 'insert into am (`name`,`income`,`output`,`total`,`createdate`) values ("%s","%f","%f","%f","%s")' % (am_name,float(income),float(output),float(total),datetime.utcnow())
            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()
            if row:
                msg = {
                    'code': 4000,
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

        verify_channel = channelStatus()
        if verify_channel.verifyStatusApp(channeler_id, app_id):
            tranform = AdvertiseTransOffer()
            getoffer = tranform.getRuleAdvertise(rule_id)
            tranform.tranRuleOffer(app_id)
            msg = {
                'code': 4000,
                'msg': 'Offer创建成功'
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

        verify_channel = channelStatus()
        if verify_channel.verifyStatusApp(channeler_id, app_id):
            tranform = AdvertiseTransOffer()
            getoffer = tranform.getONEAdvertise(rule_id)
            tranform.tranONEOffer(app_id, ad_id)
            msg = {
                'code': 4000,
                'msg': 'Offer创建成功'
            }
            self.write(msg)
        else:
            self.write_error(500)


class AMChannelOper(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        status = self.get_argument('status', None)
        channeler_id = self.get_argument('channeler_id', None)

        channel = channelStatus()
        status = channel.setStatus(status, channeler_id)
        if status['code'] == 0 or status['code'] == '0':
            message = {
                'code': 4000,
                'msg': '渠道状态更新成功'
            }
            self.write(message)
        else:
            self.write_error(500)
