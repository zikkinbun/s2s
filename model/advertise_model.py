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

    def get_advertise_by_AderId(self, ader_id, perPage, indexPage):

        if int(indexPage) == 1:
            sql = 'select a.name,b.ad_id,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=%s and b.ader_id=%s limit %d,%d' % (ader_id, ader_id, int(indexPage), int(perPage))
            return self._conn_read.query(sql)
        else:
            index = (int(indexPage) - 1)*perPage
            sql = 'select a.name,b.ad_id,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=%s and b.ader_id=%s limit %d,%d' % (ader_id, ader_id, int(index), int(perPage))
            return self._conn_read.query(sql)

    def get_advertise_all(self, perPage, indexPage):

        if int(indexPage) == 1:
            sql = 'select a.name,b.ad_id,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=b.ader_id limit %d,%d' % (int(indexPage), int(perPage))
            return self._conn_read.query(sql)
        else:
            index = (int(indexPage) - 1)*perPage
            sql = 'select a.name,b.ad_id,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=b.ader_id limit %d,%d' % (int(index), int(perPage))
            return self._conn_read.query(sql)

    def get_total_count_list(self, ader_id):
        sql = 'SELECT COUNT(*) FROM advertise a,advertiser b WHERE a.ader_id=%s AND b.id=%s'
        return self._conn_read.query(sql, ader_id, ader_id)[0]

    def get_total_count_all(self):
        sql = 'SELECT COUNT(*) FROM advertise a,advertiser b WHERE a.ader_id=b.id'
        return self._conn_read.query(sql)[0]

    def set_put_price(self, ad_id, put_price):
        table = 'advertise'

        data = {
            'put_price': put_price
        }

        condition_data = {
            'ad_id': ad_id
        }

        return self.update(table, data, condition_data)
