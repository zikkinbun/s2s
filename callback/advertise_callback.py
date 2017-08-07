# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

import sign_api
from db.mysql import connection

from urlparse import urlparse
from datetime import datetime
from pymysql import err
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
        /v1/click?click_id=/VecSQIFsM/Cqo34&chn=&order=YM1707201-zyBGy647&app_id=294daae457e8e335&ad_id=959130194285696871&revenue=0.98&sign=54ddf707b1520da3cb752a93b2b27eff
        11 | 1JGsLC4QNb81K26J | NdiYASAdi9Teqq6h | 01372486 | EUIXgvfdSFShEk6TchD7Ug== | 7h2k1zHd | NULL | 2017-07-19 10:23:55 |  NULL
    """

    @tornado.gen.coroutine
    def get(self):
        click_id = self.get_argument('click_id', None)
        if click_id is None:
            raise tornado.web.MissingArgumentError('click_id')
        chn = self.get_argument('chn', None)
        if chn is None:
            raise tornado.web.MissingArgumentError('chn')
        order = self.get_argument('order', None)
        if order is None:
            raise tornado.web.MissingArgumentError('order')
        app_id = self.get_argument('app', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app')
        ad_id = self.get_argument('ad_id', None)
        if ad_id is None:
            raise tornado.web.MissingArgumentError('ad_id')
        # ad_name = self.get_argument('ad_name', None)
        revenue = self.get_argument('revenue', None)
        if revenue is None:
            raise tornado.web.MissingArgumentError('revenue')
        # print click_id
        try:
            step_a = 'update track_click set valid="%d",updatetime="%s" where click_id="%s"' % (int(1), datetime.utcnow(), click_id)
            step_b = 'update advertise set click=click+"%d",income=income+"%f" where ader_offer_id="%s"' % (int(1), float(revenue), ad_id)
            step_c = 'update application set income=income+"%f", click=click+"%d" where offer_id=(select offer_id from track_click where click_id="%s")' % (int(1), click_id)

            cursor = connection.cursor()
            cursor.execute(step_a)
            cursor.execute(step_b)
            cursor.execute(step_c)
            connection.commit()
        except err.ProgrammingError as e:
            print e
        # finally:
        #     connection.close()
