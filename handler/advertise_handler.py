# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from handler.base_handler import BaseHandler
from model.advertise_model import AdvertiseModel
import sign_api

from pymysql import err
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

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.api_name = 'Admix'

    def verifyPullstatus(self):
        exist = connection.cursor()
        exist.execute('select is_pulled from advertiser where api_name="%s"' % self.api_name)
        is_pulled = exist.fetchone()['is_pulled']
        # exist.close()
        # connection.close()
        if is_pulled == 1 or is_pulled == '1':
            return True
        else:
            return False

    def setStatus(self, api_name, is_pulled):
        query = 'update advertiser set is_pulled=%s where api_name=%s' % (is_pulled, api_name)
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
        except err.ProgrammingError as e:
            print e
        # finally:
        #     connection.close()

    def getAdxmiOffer(self, app_id, page_size):
        datas = None
        page = 1
        url = 'http://ad.api.yyapi.net/v2/offline'
        default_params = {
            'app_id': app_id,
            'page_size': page_size,
            'page': page
        }
        if self.verifyPullstatus():
            r = requests.get(url, default_params)
            if r.status_code == '200' or r.status_code == 200:
                datas = json.loads(r.text)
                if datas['offers'] == [] or datas['offers'] == '[]':
                    self.setStatus(self.api_name, 0)
                    msg = {
                        'code': 1001,
                        'msg':"This advertiser's API is closed."
                    }
                    return msg
                else:
                    for data in datas['offers']:
                        ad_id = ''.join(random.sample(string.digits, 8))
                        ader_id = 1

                        cursor = connection.cursor()

                        device = data[u'mandatory_device']
                        device_query = 'insert IGNORE into `device` (`ad_id`,`imei`,`mac`,`andid`,\
                        `idfa`,`udid`) values ("%s","%s","%s","%s","%s","%s")' % (ad_id,device['imei'],\
                        device['mac'],device['andid'],device['idfa'],device['udid'])

                        new_device = cursor.execute(device_query)

                        advertise_query = 'insert IGNORE into `advertise` (`ad_id`,`ad_name`,`ader_id`,`ader_offer_id`,\
                        `pkg_name`,`region`,`get_price`,`os`,`os_version`,`creatives`,`payout_type`,\
                        `icon_url`,`preview_url`,`track_url`,`click`,`installed`,`income`,`access_price`,`put_price`,`updatetime`) values ("%s","%s","%d","%s","%s",\
                        "%s","%f","%s","%s","%s","%s","%s","%s","%s","%d","%f","%f","%f","%f","%s")' % (ad_id,data[u'name'],ader_id,\
                        data[u'id'],data[u'package'],data[u'country'],data[u'payout'],data[u'os'],\
                        data[u'os_version'],data[u'creative'],data[u'payout_type'],data[u'icon_url'],\
                        data[u'preview_url'],data[u'trackinglink'],0,0.0,0.0,0.0,0.0,datetime.utcnow())
                        # print advertise_query

                        new_advertise = cursor.execute(advertise_query)

                    page_range = int(datas['total'])/int(datas['page_size']) + 1
                    next_page = page + 1
                    for i in range(next_page ,page_range):
                        params = {
                            'app_id': app_id,
                            'page_size': page_size,
                            'page': i
                        }
                        # print params
                        r = requests.get(url, params)
                        if r.status_code == '200' or r.status_code == 200:
                            datas = json.loads(r.text)
                            # print i
                            for data in datas['offers']:
                                ad_id = ''.join(random.sample(string.digits, 8))
                                ader_id = 1
                                device = data[u'mandatory_device']
                                device_query = 'insert IGNORE into `device` (`ad_id`,`imei`,`mac`,`andid`,\
                                `idfa`,`udid`) values ("%s","%s","%s","%s","%s","%s")' % (ad_id,device['imei'],\
                                device['mac'],device['andid'],device['idfa'],device['udid'])

                                new_device = cursor.execute(device_query)

                                advertise_query = 'insert IGNORE into `advertise` (`ad_id`,`ad_name`,`ader_id`,`ader_offer_id`,\
                                `pkg_name`,`region`,`get_price`,`os`,`os_version`,`creatives`,`payout_type`,\
                                `icon_url`,`preview_url`,`track_url`,`click`,`installed`,`income`,`access_price`,`put_price`,`updatetime`) values ("%s","%s","%d","%s","%s",\
                                "%s","%f","%s","%s","%s","%s","%s","%s","%s","%d","%f","%f","%f","%f","%s")' % (ad_id,data[u'name'],ader_id,\
                                data[u'id'],data[u'package'],data[u'country'],data[u'payout'],data[u'os'],\
                                data[u'os_version'],data[u'creative'],data[u'payout_type'],data[u'icon_url'],\
                                data[u'preview_url'],data[u'trackinglink'],0,0.0,0.0,0.0,0.0,datetime.utcnow())

                                new_advertise = cursor.execute(advertise_query)
                    connection.commit()
                    connection.close()

class AdvertiseStatus(object):
    """
        广告状态操作
    """

    def getAdvertise(self, ad_id):
        try:
            query = 'select ad_id,ader_offer_id from advertise where ad_id=%s' % ad_id
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            if data:
                return data
            else:
                msg = {
                    'code': 1002,
                    'msg': u'广告不存在'
                }
                return msg
        except err.ProgrammingError as e:
            print e

    def getDeviceInfo(self, ad_id):
        try:
            query = 'select imei,mac,andid,idfa,udid from device where ad_id=%s' % ad_id
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchone()
            if data:
                return data
            else:
                msg = {
                    'code': 1003,
                    'msg': u'该广告没有硬件信息'
                }
                return msg
        except err.ProgrammingError as e:
            print e


class getAdvertise(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        ader_id = json.loads(self.request.body)['ader_id']
        if not ader_id:
            raise tornado.web.MissingArgumentError('ader_id')

        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
            data = advermodel.get_advertise_all(ader_id)

            if data:
                message = {
                    'retcode': 0,
                    'retdata': data,
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                message = {
                    'retcode': 1007,
                    'retmsg': 'have no advertise'
                }
                self.write(message)
        except Exception as e:
                message = {
                    'retcode': 1006,
                    'retmsg': 'databases oper error'
                }
                self.write(message)

class Advertiser(BaseHandler):

    """
        广告主录入
    """

    @tornado.gen.coroutine
    def post(self):
        api_name = json.loads(self.request.body)['api_name']
        if not api_name:
            raise tornado.web.MissingArgumentError('api_name')
        name = json.loads(self.request.body)['name']
        if not name:
            raise tornado.web.MissingArgumentError('name')
        resp_callback_url = json.loads(self.request.body)['resp_callback_url']
        if not resp_callback_url:
            raise tornado.web.MissingArgumentError('resp_callback_url')
        resp_callback_token = json.loads(self.request.body)['resp_callback_token']
        if not resp_callback_url:
            raise tornado.web.MissingArgumentError('resp_callback_token')
        is_pulled = json.loads(self.request.body)['is_pulled'] # 控制定时拉取任务
        if not is_pulled:
            raise tornado.web.MissingArgumentError('is_pulled')

        try:
            db_conns = self.application.db_conns
            advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
            data = advermodel.check_duplicate_advertiser(api_name)
            if data:
                msg = {
                    'retcode': 1005,
                    'retmsg': 'Advertiser is existed'
                }
                self.write(msg)
            else:
                try:
                    row = advermodel.set_advertiser(api_name, name, resp_callback_url, resp_callback_token, is_pulled)
                    if row:
                        msg = {
                            'retcode': 0,
                            'retmsg': 'Advertiser commit successfully'
                            }
                        self.write(msg)
                except Exception as e:
                    msg = {
                        'retcode': 1006,
                        'retmsg': 'databases oper error'
                    }
                    self.write(msg)
        except Exception as e:
            msg = {
                'retcode': 1006,
                'retmsg': 'databases oper error'
            }
            self.write(msg)
