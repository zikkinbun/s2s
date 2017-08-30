# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class AdvertiseModel(BaseDB):

    def get_advertise_by_default_rule_price(self, params):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'put_price','payout_type', 'os', 'os_version', 'creatives', 'description', 'status']

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

    def get_advertise_by_get_price(self, key, value):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'put_price','payout_type', 'os', 'os_version', 'creatives', 'description', 'status']

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
        condition_list.append(key)
        condition_list.append(value)
        condition_str = ''.join(condition_list)

        sql = sql_str + condition_str

        return self._conn_read.query(sql)

    def get_advertise_by_payout_type(self, type):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'put_price', 'payout_type', 'os', 'os_version', 'creatives', 'description', 'status']
        condition_data = {
            'payout_type': type
        }

        return self.select(table, fields, condition_data)

    def get_advertise_by_region(self, value):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'put_price', 'payout_type', 'os', 'os_version', 'creatives', 'description', 'status']
        condition_data = {
            'region': value
        }

        return self.select(table, fields, condition_data)

    def get_advertise_by_adid(self, ad_id):
        table = 'advertise'
        fields = ['ad_id', 'ader_offer_id']
        condition_data = {
            'ad_id': ad_id
        }
        return self.select(table, fields, condition_data)

    def get_advertise_by_AderId(self, ader_id, perPage, indexPage):

        if int(indexPage) == 1:
            sql = 'select a.name,b.ad_id,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=%s and b.ader_id=%s limit %d,%d' % (ader_id, ader_id, int(indexPage), int(perPage))
            return self._conn_read.query(sql)
        else:
            index = (int(indexPage) - 1)*perPage
            sql = 'select a.name,b.ad_id,b.ad_name,b.pkg_name,b.region,b.get_price,b.put_price,b.access_price,b.click,b.installed,b.income from advertiser a,advertise b where a.id=%s and b.ader_id=%s limit %d,%d' % (ader_id, ader_id, int(index), int(perPage))
            return self._conn_read.query(sql)

    def get_advertise_by_aderid(self, ader_id):
        table = 'advertise'
        fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'put_price','payout_type', 'os', 'os_version', 'creatives', 'description', 'status']
        condition_data = {
            'ader_id': int(ader_id)
        }
        return self.select(table, fields, condition_data)


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
        sql = 'UPDATE advertise SET put_price=%f WHERE ad_id=%s' % (put_price, ad_id)
        return self._conn_write.execute_rowcount(sql)

    def get_advertise_info(self, ad_id):
        table = 'advertise'

        fields = ['ad_name', 'pkg_name', 'region', 'status', 'description']

        condition_data = {
            'ad_id': ad_id
        }

        return self.select(table, fields, condition_data)

    def set_income_click(self, ader_offer_id, revenue):

        sql = 'UPDATE advertise SET income=income+%f WHERE ader_offer_id=%s' % (float(revenue), ader_offer_id)

        return self._conn_write.execute_rowcount(sql)

    def create_Admix_advertise(self, ad_id, ader_id, dataset):
        table = 'advertise'

        preview_url = unicode(dataset['preview_url']).replace('%', '').replace(' ', '')
        tittle = unicode(dataset['name']).replace('%', '').replace('+', ' ').replace('"', '')
        data = {
            'ad_id': ad_id,
            'ad_name': tittle,
            'ader_id': ader_id,
            'ader_offer_id': dataset['id'],
            'pkg_name': dataset['package'],
            'region': dataset['country'],
            'get_price': dataset['payout'],
            'os': dataset['os'],
            'os_version': dataset['os_version'],
            'creatives': dataset['creative'],
            'payout_type': dataset['payout_type'],
            'icon_url': dataset['icon_url'],
            'preview_url': preview_url,
            'track_url': dataset['trackinglink'],
            'click': 0,
            'installed': 0.0,
            'income': 0.0,
            'access_price': 0.0,
            'put_price': 0.0,
            'updatetime': datetime.now()
        }
        return self.insert(table, data)

    def create_device_info(self, ad_id, dataset):
        table = 'device'
        data = {
            'ad_id': ad_id,
            'imei': dataset['imei'],
            'mac': dataset['mac'],
            'andid': dataset['andid'],
            'idfa': dataset['idfa'],
            'udid': dataset['udid'],
        }
        return self.insert(table, data)

    def get_device_info(self, ad_id):
        table = 'device'
        fields = ['imei', 'mac', 'andid', 'idfa', 'udid']
        condition_data = {
            'ad_id': ad_id
        }
        return self.select(table, fields, condition_data)

    def count_all_advertise_income_by_id(self, ader_id):
        sql = 'SELECT FORMAT(SUM(income),2) total FROM advertise WHERE ader_id=%s'
        return self._conn_read.query(sql, ader_id)[0]

    def count_all_advertise_income(self):
        sql = 'SELECT FORMAT(SUM(income),2) total FROM advertise'
        return self._conn_read.query(sql)[0]

class AdvertiserModel(BaseDB):

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

        return self.select(table, fields, condition_data)

    def get_pull_status(self, api_name):
        table = 'advertiser'
        fields = ['is_pulled']
        condition_data = {
            'api_name': api_name
        }
        return self.select(table, fields, condition_data)

    def set_pull_status(self, api_name, is_pulled):
        table = 'advertiser'
        data = {
            'is_pulled': is_pulled
        }
        condition_data = {
            'api_name': api_name
        }
        return self.update(table, data, condition_data)

    def get_advertiser(self):
        table = 'advertiser'
        fields = ['id', 'name', 'api_name', 'is_pulled']
        return self.select(table, fields)
