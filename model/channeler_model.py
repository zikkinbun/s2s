# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class ChannelModel(BaseDB):

    def signup_chaneler(self, username, passwd, email, status, chn_id, am_id):
        table = 'channeler'
        data = {
            'name': username,
            'passwd': passwd,
            'email': email,
            'status': status,
            'chn_id': chn_id,
            'am_id': am_id,
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

        return self.select(table, fileds, condition_data)

    def set_channeler_status(self, status, chn_id):
        table = 'channeler'
        data = {
            'status': status,
        }
        condition_data = {
            'chn_id': chn_id
        }

        return self.update(table, data, condition_data)

    def verify_app_status(self, chn_id, app_id):
        sql = 'select a.status as chn_status, b.status as app_status from channeler a, application b where a.chn_id=%s and b.chn_id=%s and b.app_id=%s'

        return self._conn_read.query(sql, chn_id, chn_id, app_id)

    def get_login_chner(self, username, passwd):
        table = 'channeler'
        fields = ['chn_id', 'passwd', 'status']

        condition_data = {
            'name': username
        }

        return self.select(table, fields, condition_data)

    def set_login_time(self, username):
        table = 'channeler'

        data = {
            'login_time': datetime.now()
        }
        condition_data = {
            'name': username
        }
        return self.update(table, data, condition_data)

    def list_channeler(self, am_id):
        table = 'channeler'

        fileds = ['chn_id', 'name', 'email', 'status']

        condition_data = {
            'am_id': am_id
        }

        return self.select(table, fileds, condition_data)

    def list_chnid(self):
        table = 'channeler'

        fileds = ['chn_id']

        return self.select(table, fileds)
