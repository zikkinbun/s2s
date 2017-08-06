# _*_ coding:utf-8_*_
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     force_xsrf_cookie = self.xsrf_token
    #     print('Token for {}: {}'.format(self.request.uri, force_xsrf_cookie))

    def get_current_user(self):
        return self.get_secure_cookie("user", 0)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie('user', tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")

    def clear_current_user(self):
        self.clear_cookie("user")
