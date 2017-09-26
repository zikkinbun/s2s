# _*_ coding:utf-8_*_
from tornado import gen

from utils.constants_utils import BaseConstant
from utils.errors import BaseError
from processor.base_processor import BaseProcessor
from handler.cookietoken_handler import EncryptPassword
import os
import urls
import random
import string
import base64

@urls.processor(BaseConstant.CHN_LOGIN)
class ChannelerLogin(BaseProcessor):
    '''
        下游系统登录
    '''

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

        # define member variables here

    @gen.coroutine
    def process(self):
        '''
        process protocol
        '''

        data = self.chnmodel.get_login_chner(self.params['username'], self.params['passwd'])
        if not EncryptPassword(data[0]['passwd']).auth_password(self.params['passwd']):
            raise BaseException(BaseError.ERROR_PASSWORD_ERROR)
        else:
            if int(data[0]['status']) == 1 or int(data[0]['status']) == 0:

                retdata = {
                    'chn_id': data[0]['chn_id'],
                }
                row = self.chnmodel.set_login_time(self.params['username'])
                # if row:
                #     self.set_current_user(data[0]['chn_id'])
                return_data = retdata
                return return_data

@urls.processor(BaseConstant.GET_CHN_INCOME)
class countChnAppIncome(BaseProcessor):
    '''
        统计下游收入
    '''

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

        # define member variables here

    @gen.coroutine
    def process(self):
        '''
        process protocol
        '''
        chn_id = self.params['chn_id']
        if chn_id == 'all':
            chn_list = self.chnmodel.list_chnid()
            chn_income = 0
            msg = []
            for chn in chn_list:
                chnid = chn['chn_id']
                app_list = self.appmodel.list_appid_by_chnid(chnid)
                if app_list is not None:
                    app_datas = []
                    for app in app_list:
                        app_id = app['app_id']
                        app_data = self.appmodel.get_app_income_install_click_by_appid(app_id)[0]
                        chn_income += app_data['income']
                        app_datas.append(app_data)
                    data = {
                        'chn_id': chnid,
                        'detail': app_datas,
                        'total_income': chn_income
                        }
                    msg.append(data)
                else:
                    data = {
                        'chn_id': chnid,
                        'detail': None,
                        'total': None
                    }
                    msg.append(data)
            return_data = msg
            return return_data
        else:
            app_list = self.appmodel.list_appid_by_chnid(chn_id)
            chn_income = 0
            msg = []
            for app in app_list:
                app_data = self.appmodel.get_app_income_install_click_by_appid(app['app_id'])[0]
                app_income = app_data['income']
                chn_income += app_income
                msg.append(app_data)
            data = {
                'detail': msg,
                'total_income': chn_income
            }
            return_data = data
            return return_data
