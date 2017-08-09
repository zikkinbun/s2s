# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime
import re

class OfferModel(BaseDB):

    def get_offer_by_app(self, app_id, sign):
        table = 'offer'
        fields = ['offer_id', 'tittle', 'pkgname', 'category', 'icon_url', 'preview_url', 'click_url', 'os', 'os_version', 'region', 'payout', 'payout_currency', 'payout_type', 'creatives']

        condition_data = {
            'app_id': app_id
        }

        return self.select(table, fields, condition_data)

    def check_duplicate_offer(self, app_id, ad_id):
        table = 'offer'
        fields = ['offer_id']
        condition_data = {
            'app_id': app_id,
            'advertise_id': ad_id
        }

        return self.select(table, fields, condition_data)

    def get_all_offer(self):
        table = 'offer'
        fields = ['offer_id', 'tittle', 'pkgname', 'category', 'icon_url', 'preview_url', 'click_url', 'os', 'os_version', 'region', 'payout', 'payout_currency', 'payout_type', 'creatives']

        return self.select(table, fields)

    def trans_offer_by_rule(self, offer_id, app_id, click_url, dataset):
        table = 'offer'

        data = {
            'offer_id': offer_id,
            'app_id': app_id,
            'tittle': dataset['ad_name'],
            'advertise_id': dataset['ad_id'],
            'pkgname': dataset['pkg_name'],
            'icon_url': dataset['icon_url'],
            'preview_url': dataset['preview_url'],
            'category': dataset['category'],
            'os': dataset['os'],
            'os_version': dataset['os_version'],
            'payout': dataset['get_price'],
            'payout_type': dataset['payout_type'],
            'click_url': click_url,
            'region': dataset['region'],
            'creatives': dataset['creatives'],
            'description': dataset['description'],
            'createdate': datetime.utcnow()
        }
        print data
        return self.insert(table, data)
