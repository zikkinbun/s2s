# _*_ coding:utf-8_*_
import tornado.web

class PageNotFoundHandler(tornado.web.RequestHandler):

    def get(self):
        return self.write_error(404)
