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
        api_name = 'Admix'
        url = 'http://ad.api.yyapi.net/v2/offline'
        advertises = []
        default_params = {
            'app_id': app_id,
            'page_size': page_size,
            'page': page
        }
        exist = connection.cursor()
        exist.execute('select is_pulled from advertiser where api_name="%s"' % api_name)
        # print exist.fetchone()['is_pulled']
        if exist.fetchone()['is_pulled'] == 1 or exist.fetchone()['is_pulled'] == '1':
            r = requests.get(url, default_params)
            if r.status_code == '200' or r.status_code == 200:
                datas = json.loads(r.text)
                print datas['total']
                if datas['offers'] == [] or datas['offers'] == '[]':
                    not_pulled = connection.cursor()
                    not_pulled.execute('update advertiser set is_pulled="%d" where api_name="%s"' % (0, api_name))
                    connection.commit()
                    not_pulled.close()
                    connection.close()
                else:
                    page_range = int(datas['total'])/int(datas['page_size']) + 1
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
        resp_callback_url = self.get_argument('callback_url', None)
        resp_callback_token = self.get_argument('callback_token', None)
        is_pulled = self.get_argument('is_pulled', None) # 控制定时拉取任务

        cursor = yield POOL.execute('select callback_token from advertiser where api_name="%s"' % api_name)
        # print (cursor.fetchall())[0][0]
        if (cursor.fetchall())[0][0]:
            self.write('广告主已存在')
        else:
            try:
                query = 'insert into advertiser (api_name, name, callback_url, callback_token, \
                is_pulled) values ("%s", "%s", "%s", "%s", "%d")' % (api_name, name, resp_callback_url, \
                resp_callback_token, int(is_pulled))
                cursor = yield POOL.execute(query)
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
