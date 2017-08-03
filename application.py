# _*_ coding:utf-8_*_
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

# import pymongo
# from tornado_mysql import pools

from datetime import datetime
import base64
import os
import json

from callback.advertise_callback import AdvertiseCallback
from callback.offer_callback import OfferCallback
from handler.channel_handler import signupChaneler, setToken, createApplication
from handler.am_handler import AMsetup, AMtoMultiOffer, AMtoOneOffer
from handler.offer_handler import OfferHandler
from handler.click_handler import ClickUrlHandler
from handler.advertise_handler import Advertises, Advertiser
from handler.rule_handler import RuleHandler, selectRule


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/v1/click", AdvertiseCallback),
            (r"/v1/signup", signupChaneler),
            (r"/v1/token", setToken),
            (r"/v1/ader", Advertiser),
            (r"/v1/track", ClickUrlHandler),
            (r"/v1/app", createApplication),
            (r"/v1/offline", OfferHandler),
            (r"/v1/am", AMsetup),
            (r"/v1/am/multioffer", AMtoMultiOffer),
            (r"/v1/am/offer", AMtoOneOffer),
            (r"/v1/callback", OfferCallback),
            (r"/v1/rule", RuleHandler),
            (r"/v1/rule/detail", selectRule),
        ]
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False
        }
        # conn = pymongo.MongoClient("mongodb://db_admin:db_admin2017@112.74.182.80:27017/S2S")
        # self.db = conn.cursor()
        # pools.DEBUG = True
        # self.POOL = pools.Pool(
        #     dict(host='127.0.0.1', port=3306, user='db_admin', passwd='db_admin2015', db='s2s'),
        #     max_idle_connections=1,
        #     max_recycle_sec=3)
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
