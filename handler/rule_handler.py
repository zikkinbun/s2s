# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection

from datetime import datetime
from pymysql import err
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

        try:
            query = 'insert into rule (name,type,value,comment) values ("%s","%s","%s","%s")' % (rule_name,rule_type,rule_value,rule_comment)
            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()
            if row:
                msg = {
                    'code': 1000,
                    'ruleName': rule_name,
                    'ruleStatus': '规则创建成功'
                }
                self.write(msg)
        except err.ProgrammingError as e:
            print e
        finally:
            connection.close()

class SelectRule(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        rule_id = self.get_argument('rule_id', None)

        try:
            query = 'select name,type,value,comment from rule where id="%d"' % int(rule_id)
            cursor = connection.cursor()
            cursor.execute(query)
            datas = cursor.fetchone()
            if datas:
                response = {
                    'code': 1000,
                    'ruleName': data['name'],
                    'ruleValue': data['value'],
                    'ruleComment': data['comment']
                    }
                self.write(response)
        except err.ProgrammingError as e:
            print e
        # finally:
        #     connection.close()


class SpecailRule(object):

    def getRule(self, rule_id):
        try:
            query = 'select value from rule where id="%d"' % int(rule_id)
            cursor = connection.cursor()
            cursor.execute(query)
            value = cursor.fetchone()
            if value:
                return value['value']
        except err.ProgrammingError as e:
            print e
        # finally:
        #     connection.close()
