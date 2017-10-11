# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class AdminModel(BaseDB):

    def set_secret_sign(self, tag, secret, expires, comment=None):
        table = 'admin'
        data = {
            'tag': tag,
            'access_secret': secret,
            'expires': expires
        }

        self.insert(table, data)

    def get_token(self, token, tag):
        table = 'admin'

        fields = [ 'access_secret', 'expires']

        condition_data = {
            'access_secret': token,
            'tag': tag
        }
        return self.select(table, fields, condition_data)
