# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class RuleModel(BaseDB):

    def get_rule_by_id(self, id):
        table = 'rule'
        fields = ['value']
        condition_data = {
            'id': id
        }

        return self.select(table, fields, condition_data)[0]
