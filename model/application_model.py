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
            'status': int(0),
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

        return self.select(table, fileds, condition_data)

    def get_application_token_url(self, app_id, chn_id):
        table = 'application'
        fileds = ['callback_url', 'callback_token']
        condition_data = {
            'app_id': app_id,
            'chn_id': chn_id
        }

        return self.select(table, fileds, condition_data)

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

    def list_application_by_chnid(self, chn_id):
        table = 'application'
        fileds = ['app_id', 'app_name', 'app_secret', 'pkg_name', 'platform', 'status', 'description', 'deduction', 'divide']
        condition_data = {
            'chn_id': chn_id
        }

        return self.select(table, fileds, condition_data)

    def list_appid_by_chnid(self, chn_id):
        table = 'application'
        fileds = ['app_id']
        condition_data = {
            'chn_id': chn_id
        }

        return self.select(table, fileds, condition_data)

    def list_application_all(self):
        table = 'application'
        fileds = ['app_id', 'app_name', 'app_secret', 'pkg_name', 'platform', 'status', 'chn_id', 'description', 'deduction', 'divide']

        return self.select(table, fileds)


    def set_applicaiton_status(self, status, app_id):
        table = 'application'
        data = {
            'status': int(status)
        }
        condition_data = {
            'app_id': app_id
        }

        return self.update(table, data, condition_data)

    def verify_app_sign(self, app_id, sign):
        table = 'application'
        fields = ['callback_token', 'callback_url', 'chn_id']
        condition_data = {
            'app_id': app_id,
            'sign': sign
        }

        return self.select(table, fields, condition_data)

    def set_app_income(self, click_id):
        get_offerid = 'SELECT offer_id FROM track_click WHERE click_id=%s'
        offer_data = self._conn_read.query(get_offerid, click_id)[0]

        get_payout = 'SELECT payout FROM offer WHERE offer_id=%s'
        payout_data = self._conn_read.query(get_payout, offer_data['offer_id'])[0]

        sql = 'UPDATE application SET income=income+%f WHERE app_id=(SELECT app_id FROM offer WHERE offer_id="%s")' % (float(payout_data['payout']), offer_data['offer_id'])

        return self._conn_write.execute_rowcount(sql)

    def get_app_callbackurl(self, app_id):
        table = 'application'
        fields = ['callback_url']
        condition_data = {
            'app_id': app_id
        }

        return self.select(table, fields, condition_data)

    def set_applicaiton_tranform(self, app_id, deduction, divide):
        table = 'application'
        data = {
            'deduction': float(deduction),
            'divide': float(divide)
        }
        condition_data = {
            'app_id': app_id
        }
        return self.update(table, data, condition_data)

    def get_application_tranform(self, app_id):
        table = 'application'
        fields = ['deduction', 'divide']
        condition_data = {
            'app_id': app_id
        }
        return self.select(table, fields, condition_data)

    def get_application_income(self, app_id):
        table = 'application'
        fields = ['income']
        condition_data = {
            'app_id': app_id
        }
        return self.select(table, fields, condition_data)

    def get_app_income_by_chnid(self, chn_id):
        sql = 'SELECT app_id,app_name,income,(SELECT FORMAT(SUM(post_install),0) total FROM install_click_relation WHERE app_id=app_id) as post_install,(SELECT FORMAT(SUM(recv_install),0) total FROM install_click_relation WHERE app_id=app_id) as recv_install,(SELECT FORMAT(SUM(recv_click),0) total FROM install_click_relation WHERE app_id=app_id) as recv_click,(SELECT FORMAT(SUM(valid_click),0) total FROM install_click_relation WHERE app_id=app_id) as valid_click FROM application where chn_id=%s'

        return self._conn_read.query(sql, chn_id)
