# _*_ coding:utf-8_*_
import tornado.web
import tornado.httpclient

from base_handler import BaseHandler

from model.install_click_model import InstallClickModel

class getAppInstall(BaseHandler):

    @tornado.gen.coroutine
    def post(self):

        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        db_conns = self.application.db_conns
        try:
            installmodel = InstallClickModel(db_conns['read'], db_conns['write'])
            data = installmodel.count_post_install(app_id)
            if data:
                message = {
                 'retcode': 0,
                 'retdata': {
                    'installed': data['total']
                 },
                 'retmsg': 'success'
                }
                self.write(message)
        except Exception as e:
            print e

class getAppRecvInstall(BaseHandler):

    @tornado.gen.coroutine
    def post(self):

        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        db_conns = self.application.db_conns
        try:
            installmodel = InstallClickModel(db_conns['read'], db_conns['write'])
            data = installmodel.count_recv_install(app_id)
            if data:
                message = {
                 'retcode': 0,
                 'retdata': {
                    'recv': data['total']
                 },
                 'retmsg': 'success'
                }
                self.write(message)
        except Exception as e:
            print e

class getAppClick(BaseHandler):

    @tornado.gen.coroutine
    def post(self):

        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        db_conns = self.application.db_conns
        try:
            installmodel = InstallClickModel(db_conns['read'], db_conns['write'])
            data = installmodel.count_recv_click(app_id)
            if data:
                message = {
                 'retcode': 0,
                 'retdata': {
                    'click': data['total']
                 },
                 'retmsg': 'success'
                }
                self.write(message)
        except Exception as e:
            print e

class getAppValidClick(BaseHandler):

    @tornado.gen.coroutine
    def post(self):

        # app_id = self.get_argument('app_id', None)
        app_id = json.loads(self.request.body)['app_id']
        if app_id is None:
            raise tornado.web.MissingArgumentError('app_id')

        db_conns = self.application.db_conns
        try:
            installmodel = InstallClickModel(db_conns['read'], db_conns['write'])
            data = installmodel.count_valid_click(app_id)
            if data:
                message = {
                 'retcode': 0,
                 'retdata': {
                    'valid': data['total']
                 },
                 'retmsg': 'success'
                }
                self.write(message)
        except Exception as e:
            print e
