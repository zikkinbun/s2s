# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from pools import POOL
from mysql import connection

from datetime import datetime
import base64
import os
import json
import random
import string

class RuleHandler(tornado.web.RequestHandler):

    def __init__(self):
        self.rule = None

    def post(self):
        rule_name = self.get_argument('rule_name', None)
        rule_format = self.get_argument('rule_format', None)
        rule_comment = self.get_argument('rule_comment', None)

        query = 'insert into rule (name,format,comment) values ("%s","%s","%s")' % (rule_name,rule_format,rule_comment)

        cursor = POOL.execute(query)
        if cursor:
            self.write('规则创建成功')
