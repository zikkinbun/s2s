# _*_ coding:utf-8_*_
from __future__ import division
import tornado.web
import tornado.httpclient

import sign_api
from model.application_model import ApplicationModel
from model.advertise_model import AdvertiseModel
from model.click_model import ClickModel
from model.offer_model import OfferModel
from model.install_click_model import InstallClickModel

from urlparse import urlparse
from datetime import datetime
import base64
import random
import string
import json
import os
import re

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
        # click_id = self.get_argument('click_id', None)
        click_id = json.loads(self.request.body)['click_id']
        if click_id is None:
            raise tornado.web.MissingArgumentError('click_id')
        # chn = self.get_argument('chn', None)
        chn = json.loads(self.request.body)['chn']
        if chn is None:
            raise tornado.web.MissingArgumentError('chn')
        # order = self.get_argument('order', None)
        order = json.loads(self.request.body)['order']
        if order is None:
            raise tornado.web.MissingArgumentError('order')
        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app')
        # ad_id = self.get_argument('ad_id', None)
        ad_id = json.loads(self.request.body)['ad_id']
        if ad_id is None:
            raise tornado.web.MissingArgumentError('ad_id')
        # revenue = self.get_argument('revenue', None)
        revenue = json.loads(self.request.body)['revenue']
        if revenue is None:
            raise tornado.web.MissingArgumentError('revenue')

        # 保存上游回调信息
        db_conns = self.application.db_conns
        appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
        admodel = AdvertiseModel(db_conns['read'], db_conns['write'])
        clickmodel = ClickModel(db_conns['read'], db_conns['write'])
        offermodel = OfferModel(db_conns['read'], db_conns['write'])
        installmodel = InstallClickModel(db_conns['read'], db_conns['write'])

        try:
            click_row = clickmodel.set_valid_clickid(click_id)
            ad_row = admodel.set_income_click(ad_id, revenue)
            app_row = appmodel.set_app_income(click_id)

            if not click_id:
                self.write_error(500)
        except Exception as e:
            self.write_error(500)

        # 统计上游回调的安装和有效点击
        data = clickmodel.get_info_by_clickid(click_id)
        try:
            install_row = installmodel.update_recv_install(data[0]['offer_id'], data[0]['app_id'])
            click_row = installmodel.update_valid_click(data[0]['offer_id'], data[0]['app_id'])
            if not install_row and click_row:
                self.write_error(500)
        except Exception as e:
            print e
            self.write_error(500)

        # 随机扣量验证
        install_data = installmodel.get_post_recv_install(data[0]['offer_id'], data[0]['app_id'])
        formula = (install_data[0]['post_install'])/(install_data[0]['recv_install'])
        # print formula
        # print install_data['post_install'], install_data['recv_install']
        
        # 创建下游异步回调信息
        condition = appmodel.get_application_tranform(data[0]['app_id'])['deduction']
        if formula > (1.0 - condition) or formula <= 0.0:
            # print 'did not callback'
            message = {
                'retcode': 0,
                'retmsg': 'received your callback'
            }
            self.write(message)
        else:
            chn_component = []
            app_callback_url = appmodel.get_app_callbackurl(data[0]['app_id'])
            if app_callback_url:
                url = app_callback_url['callback_url']
                if url:
                    url_parse = urlparse(url)
                    query = url_parse.query
                    component_list = query.split('&')
                    for component in component_list:
                        head_param = component.split('=')
                        if re.search(r'click', head_param[0]):
                            param = head_param[0] + '=' + data[0]['app_click_id']
                            chn_component.append(param)
                        elif re.search(r'revenue', head_param[0]):
                            payout = offermodel.get_offer_by_id(data[0]['offer_id'])
                            param = head_param[0] + '=' + str(payout[0]['payout'])
                            chn_component.append(param)
                        elif re.search(r'app_id', head_param[0]):
                            param = head_param[0] + '=' + data[0]['app_id']
                            chn_component.append(param)
                        elif re.search(r'ad_id', head_param[0]):
                            param = head_param[0] + '=' + data[0]['offer_id']
                            chn_component.append(param)
                        else:
                            param = head_param[0] + '=' + ''
                            chn_component.append(param)
                    chn_callback_url = url_parse.scheme + '://' + url_parse.netloc + url_parse.path + '?' + '&'.join(chn_component)

                    try:
                        client = tornado.httpclient.AsyncHTTPClient() # 异步回调
                        headers = tornado.httputil.HTTPHeaders({"content-type": "application/json charset=utf-8"})
                        request = tornado.httpclient.HTTPRequest(chn_callback_url, "GET", headers)
                        response = yield client.fetch(request)

                        post_row = installmodel.update_post_install(data[0]['offer_id'], data[0]['app_id'])
                        status_row = clickmodel.update_callback_status(response.code, click_id)
                        if status_row:
                            pass
                        else:
                            pass
                    except Exception as e:
                        print e
            else:
                self.write_error(500)
