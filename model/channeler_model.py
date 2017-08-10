# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class ChannelModel(BaseDB):

    def signup_chaneler(self, username, passwd, email, contact, status, chn_id):
        table = 'channeler'
        data = {
            'name': username,
            'passwd': passwd,
            'email': email,
            'contact': contact,
            'status': status,
            'chn_id': chn_id,
            'is_login': int(1),
            'sign_up_date': datetime.now()
        }

        return self.insert(table, data)

    def get_channeler_status(self, chn_id):
        table = 'channeler'
        fileds = ['status']

        condition_data = {
            'chn_id': chn_id
        }

        return self.select(table, fileds, condition_data)[0]

    def set_channeler_status(self, status, am_id, chn_id):
        table = 'channeler'
        data = {
            'status': status,
            'am_id': am_id
        }
        condition_data = {
            'chn_id': chn_id
        }

        return self.update(table, data, condition_data)

    def verify_app_status(self, chn_id, app_id):
        sql = 'select a.status as chn_status, b.status as app_status from channeler a, application b where a.chn_id=%s and b.chn_id=%s and b.app_id=%s'

        return self._conn_read.query(sql, chn_id, chn_id, app_id)[0]

    def get_login_chner(self, username, passwd):
        table = 'channeler'
        fields = ['chn_id', 'passwd', 'status']

        condition_data = {
            'name': username
        }

        return self.select(table, fields, condition_data)[0]

    def set_login_time(self, *arg):
        table = 'channeler'
        if chn_id:
            data = {
                'login_time': datetime.now()
            }
            condition_data = {
                'chn_id': chn_id
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
            raise Exception
