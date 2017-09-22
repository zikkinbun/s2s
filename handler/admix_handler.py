# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
from tornado.web import HTTPError

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from handler.base_handler import BaseHandler
from model.advertise_model import AdvertiseModel, AdvertiserModel

import json
import random
import string
import requests

class Admix(object):

    """
        对接上游 API,拉取 OFFER 下的广告信息
    """

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.advermodel = AdvertiseModel(self.db_conns['read'], self.db_conns['write'])
        self.advertermodel = AdvertiserModel(self.db_conns['read'], self.db_conns['write'])
        self.api_name = 'Admix'

    def verifyPullstatus(self):
        data = self.advertermodel.get_pull_status(self.api_name)
        is_pulled = data[0]['is_pulled']
        if int(is_pulled) == 1 or is_pulled == '1':
            return True
        else:
            return False

    def setStatus(self, api_name, is_pulled):
        try:
            row = self.advertermodel.set_pull_status(self.api_name, is_pulled)
            if row:
                message = {
                    'retcode': 0,
                    'retmsg': 'update status success'
                }
                return message
            else:
                message = {
                    'retcode': 2006,
                    'retmsg': 'databases operate error'
                }

        except Exception as e:
            print e

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
            # r = yield tornado.gen.Task(self.asyncRequest, url, default_params)
            # print r
            if r.status_code == '200' or r.status_code == 200:
                datas = json.loads(r.text)
                # datas = r.json()
                # print datas
                if datas['offers'] == [] or datas['offers'] == '[]':
                    self.setStatus(self.api_name, 0)
                    msg = {
                        'retcode': 2001,
                        'retmsg':"This advertiser's API is closed."
                    }
                    # return msg
                else:
                    for data in datas['offers']:
                        ad_id = ''.join(random.sample(string.digits, 8))
                        ader_id = 1

                        device = data[u'mandatory_device']
                        self.advermodel.create_device_info(ad_id, device)
                        self.advermodel.create_Admix_advertise(ad_id, ader_id, data)

                    page_range = int(datas['total'])/int(datas['page_size']) + 1
                    next_page = page + 1
                    for i in range(next_page ,page_range):
                        params = {
                            'app_id': app_id,
                            'page_size': page_size,
                            'page': i
                        }
                        # print params
                        # r = yield tornado.gen.Task(self.asyncRequest, url, params)
                        r = requests.get(url, params)
                        if r.status_code == '200' or r.status_code == 200:
                            datas = json.loads(r.text)
                            # print i
                            for data in datas['offers']:
                                ad_id = ''.join(random.sample(string.digits, 8))
                                ader_id = 1
                                device = data[u'mandatory_device']
                                self.advermodel.create_device_info(ad_id, device)
                                self.advermodel.create_Admix_advertise(ad_id, ader_id, data)
