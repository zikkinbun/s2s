# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from base_handler import BaseHandler
from model.click_model import ClickModel

from pymysql.err import ProgrammingError
from datetime import datetime
import base64
import re
import os
import json


class ClickUrlHandler(BaseHandler):
    """
        用户每访问一次我的click_url 就生成一次 click 记录，包括 click_id,ad_id,app_id，
        可以从下游通过的我们 offer提供的trackinglink做统计，或者我们自己生成 click
    """

    @tornado.gen.coroutine
    def get(self):
        req_os = self.request.headers
        if re.search(ur'(iPhone)', str(req_os)) or re.search(ur'(Android)', str(req_os)):
            # offer库发出的offer_id为下游的ad_id
            offer_id = self.get_argument('ad_id', None)
            if offer_id is None:
                raise tornado.web.MissingArgumentError('offer_id')

            app_id = self.get_argument('app_id', None)
            if app_id is None:
                raise tornado.web.MissingArgumentError('app_id')

            app_click_id = self.get_argument('click_id', None)
            if app_click_id is None:
                raise tornado.web.MissingArgumentError('click_id')

            pid = self.get_argument('pid', None)
            if pid is None:
                raise tornado.web.MissingArgumentError('pid')

            is_existed = clickHandler().checkUnique(app_click_id)
            # print is_existed
            if is_existed['retcode'] == 0 or is_existed['retcode'] == '0':
                click_id = base64.b64encode(os.urandom(12))
                trackinglink, ad_id = clickHandler().getTrackUrl(offer_id)
                clickHandler().clickRecord(click_id, ad_id, app_id, app_click_id, offer_id)
                track_link = trackinglink + '&user_id=%s' % click_id
                self.redirect(track_link)
            else:
                message = {
                    'code': 5001,
                    'msg': 'please do not commit the same click_id again'
                }
                self.write(message)
        else:
            message = {
                'code': 5002,
                'msg': 'You are not using the mobile broswer'
            }
            self.write(message)

class clickHandler(object):

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.clickmodel = ClickModel(self.db_conns['read'], self.db_conns['write'])

    def checkUnique(self, app_click_id):

        try:
            data = self.clickmodel.check_duplication(app_click_id)
            if data and len(data) > 1:
                message = {
                    'retcode': 5004,
                    'retmsg': 'this click is not unique'
                }
                return message
            elif data and len(data) == 1:
                message = {
                    'retcode': 0,
                    'retmsg': 'this click is unique'
                }
                return message
            else:
                message = {
                    'retcode': 5005,
                    'retmsg': 'error'
                }
                return message
        except Exception as e:
            message = {
                'retcode': 0,
                'retmsg': 'this click is not existed'
            }
            return message

    def getClickId(self, app_click_id):

        try:
            data = self.clickmodel.get_clickid(app_click_id)
            if data:
                click_id = data['click_id']
                if click_id:
                    return click_id
                else:
                    return None
            else:
                return None
        except Exception as e:
            print e

    def getTrackUrl(self, offer_id):

        try:
            data = self.clickmodel.get_trackurl(offer_id)
            # print data
            if data:
                track_url = data['track_url']
                ad_id = data['ad_id']
                return track_url, ad_id
            else:
                return None
        except Exception as e:
            print e


    def clickRecord(self, click_id, ad_id, app_id, app_click_id, offer_id):

        try:
            row = self.clickmodel.create_record(click_id, ad_id, app_id, app_click_id, offer_id)
            if row:
                message = {
                    'retcode': 0,
                    'retmsg': 'success'
                }
                return message
        except Exception as e:
            print e


class CreateClickUrl(object):

    """
        http://api.bensonzhi.co/track?ad=xxxx&app_id=xxxx&pid=xxxx&click_id=xxxx
    """

    def __init__(self, app_id, ad_id, pid):
        self.ad_id = ad_id
        self.app_id = app_id
        self.pid = pid
        self.base_url = 'http://api.bensonzhi.co/v1/track'

    def createUrl(self):
        url = self.base_url + '?ad_id=%s&app_id=%s&pid=%s' % (self.ad_id, self.app_id, self.pid)
        return url
