# _*_ coding:utf-8_*_
from tornado import gen

from utils.constants_utils import BaseConstant
from processor.base_processor import BaseProcessor
import os
import urls
import random
import string
import base64
import sign_api
from urlparse import urlparse

@urls.processor(BaseConstant.LIST_APP_ALL)
class GetAppList(BaseProcessor):
    '''
    获取GetAppInfo
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

        data = self.appmodel.list_application_all()

        return_data = data
        return return_data

    def _verify_params(self):
        '''
        重写父类方法, 作参数校验
        '''
        pass

@urls.processor(BaseConstant.LIST_APP_BY_CHNID)
class ListApplication(BaseProcessor):
    '''
        根据chn_id获取AppInfo
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

        data = self.appmodel.list_application_by_chnid(self.params['chn_id'])
        # print data

        return_data = data
        return return_data

@urls.processor(BaseConstant.CREATE_APP)
class CreateApplication(BaseProcessor):
    '''
        创建APP
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
        app_id = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        app_secret = base64.b64encode(os.urandom(16))
        data = self.appmodel.create_applicaiton(app_id, app_secret, self.params['app_name'], self.params['pkg_name'], self.params['category'], self.params['platform'], self.params['url'], self.params['description'], self.params['chn_id'])
        # print data

        return_data = data
        return return_data

@urls.processor(BaseConstant.GET_APP_DETAIL)
class getApplicationDetail(BaseProcessor):
    '''
        查看APP详情
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
        data = self.appmodel.get_application_detail(self.params['app_id'], self.params['chn_id'])[0]
        # print data

        return_data = data
        return return_data

@urls.processor(BaseConstant.GET_APP_TOKENURL)
class getAppTokenUrl(BaseProcessor):
    '''
        查看APP详情
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
        data = self.appmodel.get_application_token_url(self.params['app_id'], self.params['chn_id'])
        # print data
        retdata = {
            'callback_token': data[0]['callback_token'],
            'callback_url': data[0]['callback_url']
        }
        return_data = retdata
        return return_data

@urls.processor(BaseConstant.UPDATE_APP_CALLBACKURL)
class UpdateAppCallbackUrl(BaseProcessor):
    '''
        查看APP详情
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
        sign = None
        data = self.appmodel.get_application_token_url(self.params['app_id'], self.params['chn_id'])
        # print data
        callback_token = data[0]['callback_token']

        url = sign_api.sign_url(callback_url, callback_token)
        url_parse = urlparse(url)
        query = url_parse.query
        query_array = query.split('&')
        for group in query_array:
            k, v = group.split('=')
            if k == 'sign':
                sign = v

        row = self.appmodel.set_application_detail(self.params['callback_url'], callback_token, sign, self.params['app_id'], self.params['chn_id'])
        return_data = 0
        return return_data

@urls.processor(BaseConstant.SET_APP_CALLBACKURL)
class SetCallbackUrl(BaseProcessor):
    '''
        查看APP详情
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
        sign = None
        # print data
        callback_token = base64.b64encode(os.urandom(24)) # 包括 app_secret和用户 token

        url = sign_api.sign_url(self.params['callback_url'], callback_token)
        url_parse = urlparse(url)
        query = url_parse.query
        query_array = query.split('&')
        for group in query_array:
            k, v = group.split('=')
            if k == 'sign':
                sign = v

        row = self.appmodel.set_application_detail(self.params['callback_url'], callback_token, sign, self.params['app_id'], self.params['chn_id'])
        return_data = 0
        return return_data

@urls.processor(BaseConstant.SET_DP)
class SetDeductionPartition(BaseProcessor):
    '''
        查看APP详情
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
        row = self.appmodel.set_applicaiton_tranform(self.params['app_id'], self.params['deduction'], self.params['divide'])
        # print data

        return_data = row
        return return_data

@urls.processor(BaseConstant.GET_APP_INCOME)
class getAppIncome(BaseProcessor):
    '''
        查看APP详情
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
        data = self.appmodel.get_application_income(self.params['app_id'])[0]
        # print data

        return_data = data
        return return_data
