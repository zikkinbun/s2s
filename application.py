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
from callback.offer_callback import OfferCallback

from handler.channel_handler import SignupChaneler, ChannelerLogin
from handler.am_handler import AMSginup, AMtoMultiOffer, AMChannelOper, AMAppOper, AMLogin
from handler.offer_handler import OfferHandler
from handler.click_handler import ClickUrlHandler
from handler.advertise_handler import Advertises, Advertiser, getAdvertise, getAdvertiseAll
from handler.rule_handler import RuleHandler, SelectRule
from handler.cookietoken_handler import XSRFTokenHandler
from handler.applicaiton_handler import CreateApplication, ListApplication, DetailSetting, ApplicationDetail

from db import setting

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class PageNotFoundHandler(tornado.web.RequestHandler):
    def get(self):
        return self.write_error(404)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/v1/chn/signup", SignupChaneler),
            (r"/v1/chn/login", ChannelerLogin),
            (r"/v1/chn/callback", OfferCallback),
            (r"/v1/app/create", CreateApplication),
            (r"/v1/app/active", AMAppOper),
            (r"/v1/app/list", ListApplication),
            (r"/v1/app/setting", DetailSetting),
            (r"/v1/app/detail", ApplicationDetail),
            (r"/v1/am/signup", AMSginup),
            (r"/v1/am/login", AMLogin),
            (r"/v1/am/createader", Advertiser),
            (r"/v1/am/multioffer", AMtoMultiOffer),
            (r"/v1/am/setstatus", AMChannelOper),
            (r"/v1/am/rule/create", RuleHandler),
            (r"/v1/am/rule/detail", SelectRule),
            (r"/v1/ad/getAdIDlist", getAdvertise),
            (r"/v1/ad/getAdAll", getAdvertiseAll),
            (r"/v1/offline", OfferHandler),
            (r"/v1/click", AdvertiseCallback),
            (r"/v1/track", ClickUrlHandler),
            (r"/v1/token", XSRFTokenHandler),
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
        db_conns['read'] = torndb.Connection(setting.DEV['s2s']['read']['host'], setting.DEV['s2s']['read']['database'], setting.DEV['s2s']['read']['user'], setting.DEV['s2s']['read']['password'])
        db_conns['write'] = torndb.Connection(setting.DEV['s2s']['write']['host'], setting.DEV['s2s']['write']['database'], setting.DEV['s2s']['write']['user'], setting.DEV['s2s']['write']['password'])
        return db_conns


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
