# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.pools import POOL
from db.mysql import connection

from datetime import datetime
import base64
import os
import json
import random
import string

class RuleHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        rule_name = self.get_argument('rule_name', None)
        rule_type = self.get_argument('rule_type', None)
        rule_value = self.get_argument('rule_value', None)
        rule_comment = self.get_argument('rule_comment', None)

        query = 'insert into rule (name,type,value,comment) values ("%s","%s","%s","%s")' % (rule_name,rule_type,rule_value,rule_comment)

        cursor = yield POOL.execute(query)
        if cursor:
            msg = {
                'ruleName': rule_name,
                'ruleStatus': '规则创建成功'
            }
            self.write(msg)

class selectRule(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        rule_id = self.get_argument('rule_id', None)

        query = 'select name,type,value,comment from rule where id="%d"' % int(rule_id)
        cursor = yield POOL.execute(query)
        if cursor:
            data = cursor.fetchone()
            response = {
                'ruleName': data[0],
                'ruleValue': data[2],
                'ruleComment': data[3]
                }
            self.write(response)


class specailRule(object):

    def getRule(self, rule_id):
        query = 'select value from rule where id="%d"' % int(rule_id)
        cursor = connection.cursor()
        cursor.execute(query)
        value = cursor.fetchone()
        # connection.close()
        if value:
            return value['value'][2:]
