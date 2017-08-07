# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from db.mysql import connection
from base import BaseHandler

from pymysql import err
from datetime import datetime
import os
import re
import json
import random
import string

class CreateApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_name = self.get_argument('app_name', None)
        if app_name is None:
            raise tornado.web.MissingArgumentError('app_name')
        pkg_name = self.get_argument('pkg_name', None)
        if pkg_name is None:
            raise tornado.web.MissingArgumentError('pkg_name')
        category = self.get_argument('category', None)
        if category is None:
            raise tornado.web.MissingArgumentError('category')
        platform = self.get_argument('os', None)
        if platform is None:
            raise tornado.web.MissingArgumentError('platform')
        url = self.get_argument('url', [])
        if url is None:
            raise tornado.web.MissingArgumentError('url')
        description = self.get_argument('description', None)
        if description is None:
            raise tornado.web.MissingArgumentError('description')

        chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            chn_id = self.get_secure_cookie('user_id', None)
            if chn_id is None:
                raise tornado.web.MissingArgumentError('chn_id')
        else:
            raise tornado.web.MissingArgumentError('chn_id')

        app_id = base64.b64encode(os.urandom(16))
        app_secret = base64.b64encode(os.urandom(16))

        try:
            query = 'insert into application (app_id,app_name,app_secret,pkg_name,platform,category,\
                url,is_stored,description,channeler_id,createdate) values ("%s","%s","%s","%s","%s","%s",\
                "%s","%s","%s","%s","%s")' % (app_id,app_name,app_secret,pkg_name,platform,category,url,is_stored,\
                description,chn_id,datetime.utcnow())

            cursor = connection.cursor()
            row = cursor.execute(query)
            connection.commit()

            if row:
                msg = {
                    'code': 0,
                    'msg': 'APP is created,please contract your account manager to active your APP',
                    'App_id': app_id,
                    'App_secret': app_secret
                    }
                self.write(msg)
            else:
                msg = {
                    'msgcode': 6002,
                    'msgdata': 'APP created failure'
                }
                self.write(msg)
        except err.ProgrammingError as e:
            print e
        finally:
            connection.close()

class ListApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            chn_id = self.get_secure_cookie('user_id', None)
            if chn_id is None:
                raise tornado.web.MissingArgumentError('chn_id')
        else:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            app_list = []
            query = 'select app_name,status,platform from application where channeler_id="%s"' % chn_id
            cursor = connection.cursor()
            cursor.execute(query)
            datas = iter(cursor.fetchall())
            for data in datas:
                message = {
                    'app_name': data['app_name'],
                    'platform': data['platform'],
                    'status': data['status']
                }
                app_list.append(message)
            response = {
                'code': 0,
                'data': app_list,
                'msg': 'success'
            }
            self.write(response)
        except err.ProgrammingError as e:
            print e


class UpdateApplication(BaseHandler):

    @tornado.gen.coroutine
    def post(self):
        app_name = self.get_argument('app_name', None)
        if app_name is None:
            raise tornado.web.MissingArgumentError('app_name')
        chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            raise tornado.web.MissingArgumentError('chn_id')

        try:
            query = 'update application set '
        except err.ProgrammingError as e:
            print e

class DetailSetting(BaseHandler):

    """
        callback_url = http://your_host/your_script?click_id={user_id}&sub_source_id={chn}&ip={ip}
    """

    @tornado.gen.coroutine
    def post(self):
        sign = None
        chn_id = self.get_argument('chn_id', None)
        if chn_id is None:
            chn_id = self.get_secure_cookie('user_id', None)
            if chn_id is None:
                raise tornado.web.MissingArgumentError('chn_id')
        else:
            raise tornado.web.MissingArgumentError('chn_id')

        app_id = self.get_argument('app_id', None)
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')
        callback_url = self.get_argument('callback_url', None)
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

        query = 'update application set callback_url="%s",callback_token="%s",sign="%s" where channeler_id="%s" and app_id="%s"' % (callback_url, callback_token, sign, chn_id, app_id)
        # print query
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            message = {
                'code': 0,
                'msg': 'Your AppSign is %s, please mark down' % sign
            }
            self.write(message)
        except err.ProgrammingError as e:
            print e
