# _*_ coding:utf-8_*_
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    # def __init__(self, *request, **kwargs):
    #     super(BaseHandler, self).__init__(request[0], request[1])
    #     self.set_header("Content-Type", "application/json")
    #     self.tracker = self.application.tracker
    #     self.sys_logger = self.application.sys_logger
    #     self.params = dict()
    #     self.res = dict()

    def get_current_user(self):
        return self.get_secure_cookie("user_id", 0)

    def set_current_user(self, user_id):
        if user_id:
            self.set_secure_cookie('user_id', tornado.escape.json_encode(user_id))
        else:
            self.clear_cookie("user_id")

    def clear_current_user(self):
        self.clear_cookie("user_id")
