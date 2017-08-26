# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime
import time

class ClickModel(BaseDB):

    def set_valid_clickid(self, click_id):
        sql = 'UPDATE track_click SET valid=%s,updatetime=%s WHERE click_id=%s'

        return self._conn_write.execute_rowcount(sql, 1, datetime.now(), click_id)

    def get_info_by_clickid(self, click_id):
        table = 'track_click'

        fileds = ['app_id', 'app_click_id', 'ad_id', 'offer_id']

        condition_data = {
            'click_id': click_id
        }

        return self.select(table, fileds, condition_data)[0]

    def create_record(self, click_id, ad_id, app_id, app_click_id, offer_id):
        table = 'track_click'

        data = {
            'click_id': click_id,
            'ad_id': ad_id,
            'app_id': app_id,
            'app_click_id': app_click_id,
            'offer_id': offer_id,
            'valid': 0,
            'createdate': datetime.now()
        }

        return self.insert(table, data)

    def get_trackurl(self, offer_id):
        sql = 'select track_url, ad_id from advertise where ad_id=(select advertise_id from offer where offer_id=%s)'

        return self._conn_read.query(sql, offer_id)[0]

    def get_clickid(self, app_click_id):

        table = 'track_click'

        fields = ['click_id']

        condition_data = {
            'app_click_id': app_click_id
        }

        return self.select(table, fields, condition_data)[0]

    def check_unique(self, app_click_id):

        table = 'track_click'

        fields = ['app_click_id']

        condition_data = {
            'app_click_id': app_click_id
        }

        return self.select(table, fields, condition_data)

    def update_callback_status(self, status, click_id):
        table = 'track_click'
        data = {
            'callback_status': int(status)
        }
        condition_data = {
            'click_id': click_id
        }
        return self.update(table, data, condition_data)
