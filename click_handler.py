# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
from pools import POOL

from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import string

class ClickUrlHandler(tornado.web.RequestHandler):
    """
        用户每访问一次我的click_url 就生成一次 click 记录，包括 click_id,ad_id,app_id，
        可以从下游通过的我们 offer提供的trackinglink做统计，或者我们自己生成 click
    """

    @tornado.gen.coroutine
    def get(self):
        offer_id = self.get_argument('ad_id', None) # offer库发出的offer_id为下游的ad_id
        app_id = self.get_argument('app_id', None)
        app_click_id = self.get_argument('click_id', None)

        click_id = base64.b64encode(os.urandom(12))

        select_query = 'select track_url, ad_id from advertise where ad_id=(select advertise_id from offer where offer_id="%s")' % offer_id
        select_cursor = yield POOL.execute(select_query)
        select_data = select_cursor.fetchall()

        trackinglink = select_data[0][0]
        adver_id = select_data[0][1]

        insert_query = 'insert into track_click (`click_id`,`ad_id`,`app_id`,`app_click_id`,`offer_id`,`createdate`) values ("%s","%s",\
        "%s","%s","%s","%s")' % (click_id,adver_id,app_id,app_click_id,offer_id,datetime.utcnow())
        insert_cursor = yield POOL.execute(insert_query)

        track_link = trackinglink + '&user_id=%s' % click_id
        self.redirect(track_link)


class createClickUrl(object):

    """
        http://api.bensonzhi.com/track?ad=xxxx&app_id=xxxx&pid=xxxx&click_id=xxxx
    """

    def __init__(self, ad_id, app_id, pid):
        self.ad_id = ad_id
        self.app_id = app_id
        self.pid = pid
        self.base_url = 'http://api.bensonzhi.com/v1/track'

    def createUrl(self):
        url = self.base_url + '?ad=%s&app_id=%s&pid=%s' % (self.ad_id, self.app_id, self.pid)
        return url
