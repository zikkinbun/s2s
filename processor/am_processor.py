# _*_ coding:utf-8_*_
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from processor.base_processor import BaseProcessor
from utils.constants_utils import BaseConstant
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException
from handler.cookietoken_handler import EncryptPassword

import os
import urls
import random
import string
import base64

@urls.processor(BaseConstant.AM_SGINUP)
class AMSginup(BaseProcessor):

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

    @gen.coroutine
    def process(self):

        _passwd = EncryptPassword(self.params['passwd'])._hash_password(self.params['passwd'])
        row = self.ammodel.signup_am(self.params['am_name'], _passwd)

        return_data = row
        return return_data

@urls.processor(BaseConstant.AM_CHN_OPER)
class AMCHNOPER(BaseProcessor):

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

    @gen.coroutine
    def process(self):

        row = self.chnmodel.set_channeler_status(int(self.params['status']), self.params['chn_id'])
        return_data = row
        return return_data

@urls.processor(BaseConstant.AM_APP_OPER)
class AMAPPOPER(BaseProcessor):

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

    @gen.coroutine
    def process(self):
        app_id = self.params['app_id']
        chn_id = self.params['chn_id']
        status = self.params['status']

        data = appmodel.get_application_detail(app_id, chn_id)
        if data:
            if data[0]['status'] == 0 or data[0]['status'] == '0' or data[0]['status'] == 1 or data[0]['status'] == '1':
                row = self.appmodel.set_applicaiton_status(status, app_id)
                return_data = row
                return return_data
        else:
            raise BaseException(BaseError.ERROR_COMMON_DATABASE_EXCEPTION)

@urls.processor(BaseConstant.AM_LOGIN)
class AMLogin(BaseProcessor):
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

        data = self.ammodel.login_am(self.params['username'], self.params['passwd'])
        if not EncryptPassword(data[0]['passwd']).auth_password(self.params['passwd']):
            raise BaseException(BaseError.ERROR_PASSWORD_ERROR)
        else:
            if int(data[0]['status']) == 1:

                retdata = {
                    'am_id': data[0]['id'],
                    'is_logined': 1,
                }
                row = self.ammodel.set_login_time(self.params['username'])
                if row:
                    self.set_current_user(data[0]['id'])
                return_data = retdata
                return return_data
            else:
                retdata = {
                    'is_logined': 0,
                }
                return_data = retdata
                return return_data

@urls.processor(BaseConstant.AM_CHN_SIGNUP)
class AMChannelSignup(BaseProcessor):
    '''
        创建下游账号
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
        status = 1 # verifing
        chn_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        _passwd = EncryptPassword(self.params['passwd'])._hash_password(self.params['passwd'])
        data = self.chnmodel.signup_chaneler(self.params['username'], _passwd, self.params['email'], self.params['status'], self.params['chn_id'], self.params['am_id'])
        retdata = {
            'chn_id': chn_id
        }
        return_data = retdata
        return return_data

@urls.processor(BaseConstant.AM_LIST_CHN)
class AMListChannel(BaseProcessor):
    '''
        展示下游账号
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
        am_id = self.params(['am_id'])
        data = self.chnmodel.list_channeler(int(am_id))
        return_data = data
        return return_data

@urls.processor(BaseConstant.AM_LIST)
class AMList(BaseProcessor):
    '''
        展示AM信息
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
        data = self.ammodel.get_am()
        return_data = data
        return return_data

@urls.processor(BaseConstant.AM_COUNT_ADER_INCOME)
class AMCountAdIncome(BaseProcessor):
    '''
        统计从上游获得的收入
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
        ader_id = self.params(['ader_id'])
        data = self.ammodel.count_all_advertise_income_by_id(ader_id)
        return_data = data
        return return_data

@urls.processor(BaseConstant.AM_COUNT_ADER_INCOME)
class AMCreateOfferByUnion(BaseProcessor):

    executor = ThreadPoolExecutor(5)

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
        ader_id = self.params(['ader_id'])
        app_id = self.params(['app_id'])

        checkout_data = self.appmodel.get_application_tranform(app_id)
        if not checkout_data[0]['divide']:
            raise BaseException(BaseError.ERROR_DP_NOT_SETTING)
        else:
            transform_advertise = yield self.tranOffer(ader_id, app_id, checkout_data[0]['divide'])

    @gen.coroutine
    @run_on_executor
    def tranOffer(self, ader_id, app_id, divide):

        datas = self.advermodel.get_advertise_by_aderid(ader_id)
        for data in datas:
            # print data
            check = self.offermodel.check_duplicate_offer(app_id, data['ad_id'])
            if check:
                continue
            else:
                offer_id = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                pid = random.randint(0,10)
                _url = CreateClickUrl(app_id, offer_id, pid)
                click_url = _url.createUrl()
                row = self.offermodel.trans_offer(offer_id, app_id, click_url, divide, data)
