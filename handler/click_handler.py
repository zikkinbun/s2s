# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
from db.mysql import connection

from pymysql.err import ProgrammingError
from datetime import datetime
import base64
import re
import os
import json


class ClickUrlHandler(tornado.web.RequestHandler):
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

            is_existed = self.checkUnique(app_click_id)
            if is_existed == 200 or is_existed == '200':
                click_id = base64.b64encode(os.urandom(12))
                trackinglink, adver_id = self.getTrackUrl(offer_id)
                self.clickRecord(click_id, adver_id, app_id, app_click_id, offer_id)
                track_link = trackinglink + '&user_id=%s' % click_id
                self.redirect(track_link)
            else:
                msg = 'please do not commit the same click_id again'
                self.write(msg)
        else:
            msg = 'You are not using the mobile broswer'
            self.write(msg)

    def checkUnique(self, app_click_id):
        app_click_query = 'select app_click_id from track_click where app_click_id="%s"' % app_click_id
        try:
            cursor = connection.cursor()
            cursor.execute(app_click_query)
            data = cursor.fetchone()
            if data is None or len(data) == 1:
                msg = "200"
                return msg
            elif len(data) > 1:
                msg = "-200"
                return msg
            else:
                msg = "-201"
                return msg
        except ProgrammingError as e:
            print e

    def getClickId(self, app_click_id):

        click_query = 'select click_id from track_click where app_click_id="%s"' % app_click_id
        try:
            cursor = connection.cursor()
            cursor.execute(click_query)
            data = cursor.fetchone()
            click_id = data['click_id']
            if click_id:
                return click_id
            else:
                return None
        except ProgrammingError as e:
            print e

    def getTrackUrl(self, offer_id):
        track_query = 'select track_url, ad_id from advertise where ad_id=(select advertise_id from offer where offer_id="%s")' % offer_id
        try:
            cursor = connection.cursor()
            cursor.execute(track_query)
            data = cursor.fetchone()
            if data:
                track_url = data['track_url']
                ad_id = data['ad_id']
                return track_url, ad_id
            else:
                return None
        except ProgrammingError as e:
            print e


    def clickRecord(self, click_id, adver_id, app_id, app_click_id, offer_id):

        insert_query = 'insert into track_click (`click_id`,`ad_id`,`app_id`,`app_click_id`,`offer_id`,`num`,`createdate`) values ("%s","%s",\
        "%s","%s","%s","%d","%s")' % (click_id,adver_id,app_id,app_click_id,offer_id,1,datetime.utcnow())
        try:
            cursor = connection.cursor()
            cursor.execute(insert_query)
            connection.commit()
        except ProgrammingError as e:
            connection.rollback()
            print e
        finally:
            connection.close()


class createClickUrl(object):

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
