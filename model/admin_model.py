# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class AdminModel(BaseDB):

    def set_secret_sign(self, secret, sign, name, expires, comment=None):
        table = 'admin'
        data = {
            'name': name,
            'access_secret': secret,
            'access_sign': sign,
            'expires': expires
        }

        self.insert(table, data)

    def get_token(self, token, timestamp):
        table = 'admin'

        fields = {
            'access_secret': token,
            'expires': timestamp
        }

        condition_data = {
            'access_secret': token,
        }
