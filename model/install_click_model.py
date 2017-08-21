# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime
import time

class InstallClickModel(BaseDB):

    def set_install_click(self, offer_id, ad_id, app_id, chn_id, recv_install, post_install, recv_click, valid_click):
        table = 'install_click_relation'
        data = {
            'offer_id': offer_id,
            'ad_id': ad_id,
            'chn_id': chn_id,
            'recv_install': recv_install,
            'post_install': post_install,
            'recv_click': recv_click,
            'valid_click': valid_click,
            'updatetime': datetime.now()
        }
        return self.insert(table, data)

    def update_recv_install(self, recv_install, offer_id, app_id):
        table = 'install_click_relation'
        incr_data = {
            'recv_install': 1,
        }
        condition_data = {
            'offer_id': offer_id,
            'app_id': app_id
        }
        return self.update(table, incr_data=incr_data, condition_data=condition_data)
