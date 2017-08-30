# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class AccountManagerModel(BaseDB):

    def signup_am(self, name, passwd):
        table = 'am'
        data = {
            'name': name,
            'passwd': passwd,
            'income': float(0),
            'output': float(0),
            'status': int(0),
            'total': float(0),
            'is_login': int(1),
            'createdate': datetime.now(),
            'login_time': datetime.now()
        }

        return self.insert(table, data)

    def login_am(self, name, passwd):
        table = 'am'
        fields = ['id', 'passwd', 'status']

        condition_data = {
            'name': name
        }

        return self.select(table, fields, condition_data)

    def set_login_time(self, username):

        table = 'am'

        data = {
            'login_time': datetime.now()
        }
        condition_data = {
            'name': username
        }

        return self.update(table, data, condition_data)

    def get_am(self):
        table = 'am'
        fields = ['id', 'name']
        return self.select(table, fields)
