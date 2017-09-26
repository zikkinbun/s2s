# _*_ coding:utf-8_*_
from tornado import gen

from processor.base_processor import BaseProcessor
from utils.constants_utils import BaseConstant
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException

import urls
from datetime import datetime

@urls.processor(BaseConstant.SET_TOKEN)
class XSRFTokenHandler(BaseProcessor):
    '''
        设置TOKEN
    '''

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

        self.token = handler.xsrf_token
        # define member variables here

    @gen.coroutine
    def process(self):
        '''
        process protocol
        '''
        default_expires = 24
        # print type(self.params)
        tag = self.params.get('tag')
        # print tag
        if self._verify_params(tag):
            row = self.adminmodel.set_secret_sign(tag, self.token, default_expires)
            return_data = {
                'token': self.token
            }
            return return_data
        else:
            raise BaseException(BaseError.ERROR_COMMON_ACCESS_DENIED)

    def _verify_params(self, tag):
        if tag == 'IrichSystem':
            return True
        elif tag == 'IrichChnSystem':
            return True
        else:
            return False
