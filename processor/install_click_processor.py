# _*_ coding:utf-8_*_
from tornado import gen

from processor.base_processor import BaseProcessor
from utils.constants_utils import BaseConstant
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException

import urls

@urls.processor(BaseConstant.GET_APP_INSTALL)
class getAppInstall(BaseProcessor):

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
        data = self.installclickmodel.count_post_install(self.params['app_id'])
        retdata = {
            'installed': data['total']
        }
        return retdata

@urls.processor(BaseConstant.GET_APP_RECV_INSTALL)
class getAppRecvInstall(BaseProcessor):

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
        data = self.installclickmodel.count_recv_install(self.params['app_id'])
        retdata = {
            'recv': data['total']
        }
        return retdata

@urls.processor(BaseConstant.GET_APP_CLICK)
class getAppClick(BaseProcessor):

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
        data = self.installclickmodel.count_recv_click(self.params['app_id'])
        retdata = {
            'click': data['total']
        }
        return retdata

@urls.processor(BaseConstant.GET_APP_VALID_CLICK)
class getAppValidClick(BaseProcessor):

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
        data = self.installclickmodel.count_valid_click(self.params['app_id'])
        retdata = {
            'valid': data['total']
        }
        return retdata
