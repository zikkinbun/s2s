# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from pools import POOL
from mysql import connection

import sign_api

from urlparse import urlparse
from datetime import datetime
import base64
import os
import json
import random
import string
import requests

class Advertises(object):

    """
        对接上游 API,拉取 OFFER 下的广告信息
    """

    def getAdxmiOffer(self, app_id, page_size, page):
        datas = None
        advertises = []
        default_params = {
            'app_id': app_id,
            'page_size': page_size,
            'page': page
        }
        url = 'http://ad.api.yyapi.net/v2/offline'
        r = requests.get(url, default_params)
        if r.status_code == '200' or r.status_code == 200:
            datas = json.loads(r.text)
            # print datas['total'], datas['page']
        page_range = int(datas['total'])/int(datas['page_size']) + 1
        # print page_range
        for data in datas['offers']:
            ad_id = ''.join(random.sample(string.digits, 8))
            ader_id = 1

            advertise = 'insert into `advertise` (`ad_id`,`ad_name`,`ader_id`,`ader_offer_id`,\
                `pkg_name`,`region`,`get_price`,`os`,`os_version`,`creatives`,`payout_type`,\
                `icon_url`,`preview_url`,`track_url`,`updatetime`) values ("%s","%s","%d","%s","%s",\
                "%s","%f","%s","%s","%s","%s","%s","%s","%s","%s")' % (ad_id,data[u'name'],ader_id,\
                data[u'id'],data[u'package'],data[u'country'],data[u'payout'],data[u'os'],\
                data[u'os_version'],data[u'creative'],data[u'payout_type'],data[u'icon_url'],\
                data[u'preview_url'],data[u'trackinglink'],datetime.utcnow())
            cursor = connection.cursor()
            new_record = cursor.execute(advertise)
        connection.commit()
        if int(datas['page']) <= page_range:
            return self.getAdxmiOffer(app_id, page_size, int(page) + 1)
        # 递归完成再关闭游标和链接
        # cursor.close()
        connection.close()

class Advertiser(tornado.web.RequestHandler):

    """
        广告主录入
    """

    @tornado.gen.coroutine
    def post(self):
        api_name = self.get_argument('api_name', None)
        name = self.get_argument('name', None)
        is_pulled = self.get_argument('is_pulled', None) # 控制定时拉取任务

        try:
            query = 'insert into advertiser (api_name, name, is_pulled) values ("%s", "%s", "%d")' % (api_name, name, int(is_pulled))
            # print query
            cursor = yield POOL.execute(query)
        #     print cursor
            if cursor:
                msg = {
                    'code': 0,
                    'msg': 'Add Advertiser successfully'
                }
                self.write(msg)
        except Exception as e:
            msg = {
                'errcode': -2,
                'errmode': '/advertiser/',
                'errmsg': '数据库插入出错'
            }
            self.write(msg)

class AdvertiseCallback(tornado.web.RequestHandler):
    """
        提交给上游的 callback_url和 callback_data 处理
        http://api.bensonzhi.com/click?click_id={user_id}&chn={chn}&order={order}&app_id={app}&ad_id={ad_id}&revenue={revenue}
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

        step_a = 'update track_click set valid=1 where click_id="%s"' % click_id
        step_b = 'update advertise set click=click+1,income=income+"%f" where ader_offer_id="%s"' % (revenue,ad_id)

        cursor_a = yield POOL.execute(step_a)
        cursor_b = yield POOL.execute(step_b)

        print self.request.body
