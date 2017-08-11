# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class AdvertiseModel(BaseDB):

    def get_advertise_by_price(self, params):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'payout_type', 'os', 'os_version', 'creatives', 'description', 'status']

        items = ['SELECT ']
        if not fields:
            items.append('*')
        else:
            for field in fields:
                items.append(field+',')
        sql_str = ''.join(items)
        sql_str = sql_str[0:len(sql_str)-1] + " FROM " + table

        condition_str = ''
        condition_list = [' WHERE get_price']
        condition_list.append(params[1])
        condition_list.append(params[2])
        condition_str = ''.join(condition_list)

        sql = sql_str + condition_str

        return self._conn_read.query(sql)

    def get_advertise_by_payout_type(self, params):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'payout_type', 'os', 'os_version', 'creatives', 'description', 'status']
        condition_data = {
            'payout_type': params[2]
        }

        return self.select(table, fields, condition_data)

    def get_advertise_by_region(self, params):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'payout_type', 'os', 'os_version', 'creatives', 'description', 'status']
        condition_data = {
            'payout_type': rule_value
        }

        return self.select(table, fields, condition_data)

    def set_advertiser(self, api_name, name, callback_url, callback_token, is_pulled):
        table = 'advertiser'

        data = {
            'api_name': api_name,
            'name': name,
            'callback_url': callback_url,
            'callback_token': callback_token,
            'is_pulled': is_pulled
        }

        return self.insert(table, data)

    def check_duplicate_advertiser(self, api_name):
        table = 'advertiser'
        fields = ['name']

        condition_data = {
            'api_name': api_name
        }

        return self.select(table, fields, condition_data)[0]

    def get_advertise_by_AderId(self, ader_id):

        sql = 'select a.name,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=%s and b.ader_id=%s'
        return self._conn_read.query(sql, ader_id, ader_id)

    def get_advertise_all(self):

        sql = 'select a.name,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=b.ader_id'
        return self._conn_read.query(sql)
