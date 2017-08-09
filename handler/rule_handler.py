# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from model.rule_model import RuleModel

from utils.db_utils import TornDBConnector
from db import setting

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
                    'retcode': 0,
                    'retdata': {
                        'ruleName': rule_name,
                    },
                    'retmsg': 'success'
                }
                self.write(msg)
        except Exception as e:
            print e
        finally:
            connection.close()

class SelectRule(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        rule_id = self.get_argument('rule_id', None)

        try:
            db_conns = self.application.db_conns
            rulemodel = RuleModel(db_conns['read'], db_conns['write'])
            data = rulemodel.get_rule_by_id(rule_id)
            if data:
                response = {
                    'retcode': 0,
                    'retdata': {
                        'ruleName': data['name'],
                        'ruleValue': data['value'],
                        'ruleComment': data['comment']
                    },
                    'retmsg': 'success'
                }
                self.write(response)
        except Exception as e:
            print e


class SpecailRule(object):

    def __init___(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBConnector(setting.DEV['s2s']['read']['host'], setting.DEV['s2s']['read']['database'], setting.DEV['s2s']['read']['user'], setting.DEV['s2s']['read']['password'])
        self.db_conns['write'] = TornDBConnector(setting.DEV['s2s']['write']['host'], setting.DEV['s2s']['write']['database'], setting.DEV['s2s']['write']['user'], setting.DEV['s2s']['write']['password'])

    def getRule(self, rule_id):
        try:
            db_conns = self.db_conns
            rulemodel = RuleModel(db_conns['read'], db_conns['write'])
            value = rulemodel.get_rule_by_id(rule_id)
            if value:
                return value['value']
        except Exception as e:
            print e
        # finally:
        #     connection.close()
