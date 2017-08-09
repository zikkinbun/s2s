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
            'createdate': datetime.utcnow(),
            'login_time': datetime.utcnow()
        }

        return self.insert(table, data)

    def login_am(self, name, passwd):
        table = 'am'
        fields = ['id', 'passwd', 'status']

        condition_data = {
            'name': name
        }

        return self.select(table, fields, condition_data)[0]

    def set_login_time(self, am_id=None, username=None):
        table = 'am'
        if am_id:
            data = {
                'login_time': datetime.now()
            }
            condition_data = {
                'id': am_id
            }
            return self.update(table, data, condition_data)
        elif username:
            data = {
                'login_time': datetime.now()
            }
            condition_data = {
                'name': username
            }
            return self.update(table, data, condition_data)
        else:
            break
