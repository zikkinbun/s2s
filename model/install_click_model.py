# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime
import time

class InstallClickModel(BaseDB):

    def set_install_click(self, offer_id, ad_id, app_id):
        """
            初始化当前记录
        """
        table = 'install_click_relation'
        data = {
            'offer_id': offer_id,
            'ad_id': ad_id,
            'app_id': app_id,
            'recv_install': 0,
            'post_install': 20,
            'recv_click': 0,
            'valid_click': 0,
            'updatetime': datetime.now()
        }
        return self.insert(table, data)

    def update_recv_install(self, offer_id, app_id):
        table = 'install_click_relation'
        incr_data = {
            'recv_install': 1,
        }
        condition_data = {
            'offer_id': offer_id,
            'app_id': app_id
        }
        return self.update(table, incr_data=incr_data, condition_data=condition_data)

    def update_post_install(self, offer_id, app_id):
        table = 'install_click_relation'
        incr_data = {
            'post_install': 1,
        }
        condition_data = {
            'offer_id': offer_id,
            'app_id': app_id
        }
        return self.update(table, incr_data=incr_data, condition_data=condition_data)

    def update_recv_click(self, offer_id, app_id):
        table = 'install_click_relation'
        incr_data = {
            'recv_click': 1,
        }
        condition_data = {
            'offer_id': offer_id,
            'app_id': app_id
        }
        return self.update(table, incr_data=incr_data, condition_data=condition_data)

    def update_valid_click(self, offer_id, app_id):
        table = 'install_click_relation'
        incr_data = {
            'valid_click': 1,
        }
        condition_data = {
            'offer_id': offer_id,
            'app_id': app_id
        }
        return self.update(table, incr_data=incr_data, condition_data=condition_data)

    def get_post_recv_install(self, offer_id, app_id):
        table = 'install_click_relation'
        fields = ['post_install', 'recv_install']
        condition_data = {
            'offer_id': offer_id,
            'app_id': app_id
        }
        return self.select(table, fields, condition_data)

    def count_post_install(self, app_id):
        sql = 'SELECT FORMAT(SUM(post_install),0) total FROM install_click_relation WHERE app_id=%s'
        return self._conn_read.query(sql, app_id)[0]

    def count_recv_install(self, app_id):
        sql = 'SELECT FORMAT(SUM(recv_install),0) total FROM install_click_relation WHERE app_id=%s'
        return self._conn_read.query(sql, app_id)[0]

    def count_recv_click(self, app_id):
        sql = 'SELECT FORMAT(SUM(recv_click),0) total FROM install_click_relation WHERE app_id=%s'
        return self._conn_read.query(sql, app_id)[0]

    def count_valid_click(self, app_id):
        sql = 'SELECT FORMAT(SUM(valid_click),0) total FROM install_click_relation WHERE app_id=%s'
        return self._conn_read.query(sql, app_id)[0]
