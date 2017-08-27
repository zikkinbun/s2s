# _*_ coding:utf-8_*_
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from datetime import datetime
import os
import sys
import time
import json
import base64
import torndb

from callback.advertise_callback import AdvertiseCallback

from handler.channel_handler import ChannelerLogin
from handler.am_handler import AMSginup, AMChannelOper, AMAppOper, AMLogin, AMChannelSignup, \
    AMListChannel, AMCreateOfferByUnion, AMCountAdIncome, AMIncome
from handler.offer_handler import OfferHandler
from handler.click_handler import ClickUrlHandler
from handler.install_click_handler import getAppInstall, getAppRecvInstall, getAppClick, getAppValidClick
from handler.advertise_handler import Advertises, Advertiser, getAdvertiseById, getAdvertiseAll, getAdvertiseByGetPrice, getAdvertiserALL
from handler.rule_handler import RuleHandler, SelectRule
from handler.cookietoken_handler import XSRFTokenHandler, AdminTokenHandler
from handler.applicaiton_handler import CreateApplication, ListApplication, SetCallbackUrl, getApplicationDetail, \
    ListAllApp, getAppTokenUrl, UpdateAppCallbackUrl, SetDeductionPartition, getAppIncome

from db import setting

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write_error(404)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/v1/chn/login", ChannelerLogin),
            (r"/v1/app/create", CreateApplication),
            (r"/v1/app/active", AMAppOper),
            (r"/v1/app/list", ListApplication),
            (r"/v1/app/listAll", ListAllApp),
            (r"/v1/app/setting", SetCallbackUrl),
            (r"/v1/app/detail", getApplicationDetail),
            (r"/v1/app/getTokenUrl", getAppTokenUrl),
            (r"/v1/app/updateUrl", UpdateAppCallbackUrl),
            (r"/v1/app/SetDP", SetDeductionPartition),
            (r"/v1/am/signup", AMSginup),
            (r"/v1/am/createchn", AMChannelSignup),
            (r"/v1/am/listchn", AMListChannel),
            (r"/v1/am/login", AMLogin),
            (r"/v1/am/setstatus", AMChannelOper),
            (r"/v1/am/createAder", Advertiser),
            (r"/v1/am/createOfferByUnion", AMCreateOfferByUnion),
            (r"/v1/ad/getAdById", getAdvertiseById),
            (r"/v1/ad/getAdAll", getAdvertiseAll),
            (r"/v1/ad/getAdByPrice", getAdvertiseByGetPrice),
            (r"/v1/ad/getAder", getAdvertiserALL),
            (r"/v1/count/getAppInstall", getAppInstall),
            (r"/v1/count/getAppRecvInstall", getAppRecvInstall),
            (r"/v1/count/getAppClick", getAppClick),
            (r"/v1/count/getAppValidClick", getAppValidClick),
            (r"/v1/count/getAppIncome", getAppIncome),
            (r"/v1/count/getAdIncome", AMCountAdIncome),
            (r"/v1/count/getAMIncome", AMIncome),
            (r"/v1/offline", OfferHandler),
            (r"/v1/click", AdvertiseCallback),
            (r"/v1/track", ClickUrlHandler),
            (r"/v1/token", XSRFTokenHandler),
            (r"/v1/getToken", AdminTokenHandler),
            (r".*", PageNotFoundHandler)
        ]
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False,
            "login_url": "/v1/chn/login"
        }
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)

        self.db_conns = self._init_db()

    def _init_db(self):
        """
            初始化数据库
        """
        db_conns = {}
        db_conns['read'] = torndb.Connection(setting.RELEASE['s2s']['read']['host'], setting.RELEASE['s2s']['read']['database'], setting.RELEASE['s2s']['read']['user'], setting.RELEASE['s2s']['read']['password'])
        db_conns['write'] = torndb.Connection(setting.RELEASE['s2s']['write']['host'], setting.RELEASE['s2s']['write']['database'], setting.RELEASE['s2s']['write']['user'], setting.RELEASE['s2s']['write']['password'])
        return db_conns


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
