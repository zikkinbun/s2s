# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler
from model.rule_model import RuleModel

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector

from datetime import datetime
import base64
import os
import json
import random
import string

class RuleHandler(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        # rule_name = self.get_argument('rule_name', None)
        rule_name = json.loads(self.request.body)['rule_name']
        if rule_name is None:
            raise tornado.web.MissingArgumentError('rule_name')
        # rule_type = self.get_argument('rule_type', None)
        rule_type = json.loads(self.request.body)['rule_type']
        if rule_type is None:
            raise tornado.web.MissingArgumentError('rule_type')
        # rule_value = self.get_argument('rule_value', None)
        rule_value = json.loads(self.request.body)['rule_value']
        if rule_value is None:
            raise tornado.web.MissingArgumentError('rule_value')
        # rule_comment = self.get_argument('rule_comment', None)
        rule_comment = json.loads(self.request.body)['rule_comment']
        if rule_comment is None:
            raise tornado.web.MissingArgumentError('rule_comment')

        try:
            db_conns = self.application.db_conns
            rulemodel = RuleModel(db_conns['read'], db_conns['write'])
            row = rulemodel.create_rule(rule_name, rule_type, rule_value, rule_comment)
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


class SelectRule(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def post(self):
        # rule_id = self.get_argument('rule_id', None)
        rule_id = json.loads(self.request.body)['rule_id']
        if rule_id is None:
            raise tornado.web.MissingArgumentError('rule_id')
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
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()

    def getRule(self, rule_id):
        try:
            db_conns = self.db_conns
            rulemodel = RuleModel(db_conns['read'], db_conns['write'])
            value = rulemodel.get_rule_by_id(rule_id)
            if value:
                return value['value']
        except Exception as e:
            print e
