# _*_ coding:utf-8_*_

from utils.db_utils import TornDBReadConnector, TornDBWriteConnector
from model.admin_model import AdminModel

class getToken(object):

    def __init__(self):
        self.db_conns = {}
        self.db_conns['read'] = TornDBReadConnector()
        self.db_conns['write'] = TornDBWriteConnector()
        self.adminmodel = AdminModel(self.db_conns['read'], self.db_conns['write'])

    def get_token(self, token, tag):

        data = self.adminmodel.get_token(token, tag)[0]
        print data
        if data:
            return True
        else:
            return False
