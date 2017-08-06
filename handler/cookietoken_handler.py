# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient
import tornado.escape

class XSRFTokenHandler(tornado.web.RequestHandler):
    """专门用来设置_xsrf Cookie的接口"""
    def get(self):
        token = self.xsrf_token
        self.write(token)
