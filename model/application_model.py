# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class ApplicationModel(BaseDB):


    def create_applicaiton(self, app_id, app_secret, app_name, pkg_name, category, platform, url, description, chn_id):
        table = 'application'

        data = {
            'app_id': app_id,
            'app_name': app_name,
            'app_secret': app_secret,
            'pkg_name': pkg_name,
            'platform': platform,
            'url': url,
            'category': category,
            'description': description,
            'chn_id': chn_id,
            'click': int(0),
            'install': int(0),
            'cost': float(0),
            'income': float(0),
            'createdate': datetime.now()
        }

        return self.insert(table, data)

    def get_application_detail(self, app_id, chn_id):
        table = 'application'
        fileds = ['app_id', 'app_name', 'app_secret', 'pkg_name', 'platform', 'status']
        condition_data = {
            'app_id': app_id,
            'chn_id': chn_id
        }

        return self.select(table, fileds, condition_data)[0]

    def set_application_detail(self, callback_url , callback_token, sign, app_id, chn_id):
        table = 'application'
        data = {
            'callback_url': callback_url,
            'callback_token': callback_token,
            'sign': sign
        }
        condition_data = {
            'app_id': app_id,
            'chn_id': chn_id
        }
        return self.update(table, data, condition_data)

    def list_application(self, chn_id):
        table = 'application'
        fileds = ['app_id', 'app_name', 'app_secret', 'pkg_name', 'platform', 'status']
        condition_data = {
            'chn_id': chn_id
        }

        return self.select(table, fileds, condition_data)

    def verify_app_sign(self, app_id, sign):
        table = 'application'
        fields = ['callback_token', 'callback_url', 'chn_id']
        condition_data = {
            'app_id': app_id,
            'sign': sign
        }

        return self.select(table, fields, condition_data)[0]

    def set_applicaiton_status(self, status, app_id):
        table = 'application'
        data = {
            'status': status
        }
        condition_data = {
            'app_id': app_id
        }

        return self.update(table, data, condition_data)
