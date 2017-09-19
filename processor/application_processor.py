# _*_ coding:utf-8_*_
from tornado import gen

from utils.constants_utils import BaseConstant
from processor.base_processor import BaseProcessor
import os
import urls
import random
import string
import base64

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

    def _verify_params(self):
        '''
        重写父类方法, 作参数校验
        '''
        pass

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

    def _verify_params(self):
        '''
        重写父类方法, 作参数校验
        '''
        pass
