# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from model.application_model import ApplicationModel
from base_handler import BaseHandler
import sign_api

from pymysql import err
from datetime import datetime
from urlparse import urlparse
import os
import re
import json
import random
import string
import base64

class CreateApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_name = json.loads(self.request.body)['app_name']
        if app_name is None:
            raise tornado.web.MissingArgumentError('app_name')
        pkg_name = json.loads(self.request.body)['pkg_name']
        if pkg_name is None:
            raise tornado.web.MissingArgumentError('pkg_name')
        category = json.loads(self.request.body)['category']
        if category is None:
            raise tornado.web.MissingArgumentError('category')
        platform = json.loads(self.request.body)['platform']
        if platform is None:
            raise tornado.web.MissingArgumentError('platform')
        url = json.loads(self.request.body)['url']
        if url is None:
            raise tornado.web.MissingArgumentError('url')
        description = json.loads(self.request.body)['description']
        if description is None:
            raise tornado.web.MissingArgumentError('description')

        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        app_id = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        app_secret = base64.b64encode(os.urandom(16))

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.create_applicaiton(app_id, app_secret, app_name, pkg_name, category, platform, url, description, chn_id)
            msg = {
                'retcode': 0,
                'retdata': {
                    'AppID': app_id,
                    'AppSecret': app_secret
                },
                'retmsg': 'APP is created,please contract your account manager to active your APP',
            }
            self.write(msg)

        except err.ProgrammingError as e:
            msg = {
                'retcode': 6002,
                'retmsg': 'APP created failure'
            }
            self.write(msg)

class ListApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.list_application(chn_id)
            response = {
                'retcode': 0,
                'retdata': data,
                'retmsg': 'success'
            }
            self.write(response)
        except err.ProgrammingError as e:
            print e


class UpdateApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_name = json.loads(self.request.body)['app_name']
        if app_name is None:
            raise tornado.web.MissingArgumentError('app_name')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            query = 'update application set '
        except err.ProgrammingError as e:
            print e

class ApplicationDetail(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.get_application_detail(app_id, chn_id)
            if data:
                message = {
                    'retcode': 0,
                    'retdata': data,
                    'retmsg': 'success'
                }
                self.write(message)
            else:
                self.write_error(500)
        except err.ProgrammingError as e:
            print e

class DetailSetting(BaseHandler):

    """
        callback_url = http://your_host/your_script?click_id={user_id}&sub_source_id={chn}&ip={ip}
    """

    @tornado.gen.coroutine
    def post(self):
        sign = None
        chn_id = json.loads(self.request.body)['chn_id']
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        callback_url = json.loads(self.request.body)['callback_url']
        if callback_url is None:
            raise tornado.web.MissingArgumentError('callback_url')
        callback_token = base64.b64encode(os.urandom(24)) # 包括 app_secret和用户 token

        url = sign_api.sign_url(callback_url, callback_token)
        # print url
        url_parse = urlparse(url)
        query = url_parse.query
        query_array = query.split('&')
        for group in query_array:
            k, v = group.split('=')
            if k == 'sign':
                sign = v

        try:
            db_conns = self.application.db_conns
            appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
            data = appmodel.set_application_detail(callback_url, callback_token, sign, app_id, chn_id)
            # print data
            message = {
                'retcode': 0,
                'retdata': {
                    'AppSign': sign
                },
                'retmsg': 'success'
            }
            self.write(message)
        except err.ProgrammingError as e:
            print e
