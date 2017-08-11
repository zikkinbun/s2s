# _*_ coding:utf-8_*_

from base_model import BaseDB
from datetime import datetime

class AdminModel(BaseDB):

    def set_secret_sign(self, secret):
        table = 'admin'
