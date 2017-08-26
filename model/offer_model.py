# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime
import re

class OfferModel(BaseDB):

    def get_offer_by_app(self, app_id, sign, perPage, indexPage):

        if int(indexPage) == 1:
            sql = 'SELECT offer_id,tittle,pkgname,category,icon_url,preview_url,click_url,os,os_version,region,payout,payout_currency,payout_type,payout_type FROM offer WHERE app_id=%s limit %d,%d' % (app_id, int(indexPage), int(perPage))
            return self._conn_read.query(sql)
        else:
            index = (int(indexPage) - 1)*perPage
            sql = 'SELECT offer_id,tittle,pkgname,category,icon_url,preview_url,click_url,os,os_version,region,payout,payout_currency,payout_type,payout_type FROM offer WHERE app_id=%s limit %d,%d' % (app_id, int(index), int(perPage))
            return self._conn_read.query(sql)

    def check_duplicate_offer(self, app_id, ad_id):
        table = 'offer'
        fields = ['offer_id']
        condition_data = {
            'app_id': app_id,
            'advertise_id': ad_id
        }

        return self.select(table, fields, condition_data)

    def get_offer_by_id(self, offer_id):
        table = 'offer'
        fields = ['payout', 'click_url', 'advertise_id']
        condition_data = {
            'offer_id': offer_id
        }

        return self.select(table, fields, condition_data)[0]

    def get_all_offer(self, perPage, indexPage):

        if int(indexPage) == 1:
            sql = 'select offer_id,tittle,pkgname,category,icon_url,preview_url,click_url,os,os_version,region,payout,payout_currency,payout_type,payout_type from offer limit %d,%d' % (int(indexPage), int(perPage))
            return self._conn_read.query(sql)
        else:
            index = (int(indexPage) - 1)*perPage
            sql = 'select offer_id,tittle,pkgname,category,icon_url,preview_url,click_url,os,os_version,region,payout,payout_currency,payout_type,payout_type from offer limit %d,%d' % (int(index), int(perPage))
            return self._conn_read.query(sql)

    def trans_offer(self, offer_id, app_id, click_url, divide, dataset):
        table = 'offer'
        # print dataset
        preview_url = unicode(dataset['preview_url']).replace('%', '').replace(' ', '')
        tittle = unicode(dataset['ad_name']).replace('%', '').replace('+', ' ').replace('"', '')
        payout = float(dataset['get_price']) * float(divide)
        # print payout
        data = {
            'offer_id': offer_id,
            'app_id': app_id,
            'tittle': tittle,
            'advertise_id': dataset['ad_id'],
            'pkgname': dataset['pkg_name'],
            'icon_url': dataset['icon_url'],
            'preview_url': preview_url,
            'category': dataset['category'],
            'os': dataset['os'],
            'os_version': dataset['os_version'],
            'payout': payout,
            'payout_type': dataset['payout_type'],
            'click_url': click_url,
            'region': dataset['region'],
            'creatives': dataset['creatives'],
            'description': dataset['description'],
            'createdate': datetime.now()
        }
        # print data
        return self.insert(table, data)
