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

from advertise_handler import *
from channel_handler import *
from offer_handler import *

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/v1/offline", OfferHandler),
            (r"/v1/signup", signupChaneler),
            (r"/v1/token", setToken),
            (r"/v1/ad", Advertises)
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
