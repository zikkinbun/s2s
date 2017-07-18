# _*_ coding:utf-8_*_
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import sign_api

from tornado.options import define, options
define("port", default=8001, help="run on the given port", type=int)

class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/callback", ServiceHandler),
        ]
        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False
        }
        tornado.web.Application.__init__(self, handlers, debug=True, **settings)

class ServiceHandler(tornado.web.RequestHandler):

    def get(self):
        click_id = self.get_argument('click_id', None)
        sign = self.get_argument('sign', None)

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(tornado.options.options.port)

    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
