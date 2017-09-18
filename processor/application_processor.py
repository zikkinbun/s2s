# _*_ coding:utf-8_*_
from tornado import gen

from utils.constants_utils import BaseConstant
from processor.base_processor import BaseProcessor
import urls

@urls.processor(BaseConstant.CMD_GET_APP_LIST)
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
