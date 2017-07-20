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

class AdvertiseCallback(tornado.web.RequestHandler):
    """
        提交给上游的 callback_url和 callback_data 处理
        http://api.bensonzhi.co/v1/click?click_id={user_id}&chn={chn}&order={order}&app_id={app}&ad_id={ad_id}&revenue={revenue}

        [I 170719 18:23:55 web:2063] 302 GET /v1/track?ad_id=7h2k1zHd&app_id=EUIXgvfdSFShEk6TchD7Ug==&pid=7&click_id=NdiYASAdi9Teqq6h (127.0.0.1) 7.56ms
        [I 170719 18:24:16 web:2063] 200 GET /v1/click?click_id=1JGsLC4QNb81K26J&chn=&order=YM170719oRjBpVNEd1&app_id=294daae457e8e335&ad_id={ad_id}&revenue=0.56&sign=e31981ce951dc14701495e7783c791f8 (127.0.0.1) 0.58ms
        11 | 1JGsLC4QNb81K26J | NdiYASAdi9Teqq6h | 01372486 | EUIXgvfdSFShEk6TchD7Ug== | 7h2k1zHd | NULL | 2017-07-19 10:23:55 |  NULL
    """

    @tornado.gen.coroutine
    def get(self):
        click_id = self.get_argument('click_id', None)
        chn = self.get_argument('chn', None)
        order = self.get_argument('order', None)
        app_id = self.get_argument('app', None)
        ad_id = self.get_argument('ad_id', None)
        ad_name = self.get_argument('ad_name', None)
        revenue = self.get_argument('revenue', None)

        # print click_id

        step_a = 'update track_click set valid=1 where click_id="%s"' % click_id
        step_b = 'update advertise set click=click+1,income=income+"%f" where ader_offer_id="%s"' % (revenue,ad_id)
        #
        cursor_a = yield POOL.execute(step_a)
        cursor_b = yield POOL.execute(step_b)
        # track = 'http://t.api.yyapi.net/v1/tracking?ad=935696388157612029&app_id=294daae457e8e335&pid=3'

        # print self.request.body
