# _*_ coding:utf-8_*_
from tornado import gen

from processor.base_processor import BaseProcessor
from utils.constants_utils import BaseConstant
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException

import os
import urls
import random
import string
import base64
import sign_api

@urls.processor(BaseConstant.CHN_GET_OFFER)
class OfferHandler(BaseProcessor):

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

    @gen.coroutine
    def process(self):

        global  chn_id

        app_id = self.params.get('app_id')
        sign = self.params.get('accesskey')
        page = self.params.get('page')
        page_size = self.params.get('page_size')

        if self._verify_sign(app_id, sign) and self._verify_app_status(app_id):
            data = self.offermodel.get_offer_by_app(app_id, sign, page_size, page)
            retdata = {
                'offers': data
            }
            return_data = retdata
            return return_data
        else:
            raise BaseException(BaseError.ERROR_COMMON_UNKNOWN)

    def _verify_sign(self, app_id, sign):

        '''
            验证签名
        '''
        verify_sign = None
        data = self.appmodel.verify_app_sign(app_id, sign)
        sign_url = data[0]['callback_url'] + '&sign=%s' % sign
        chn_id = data[0]['chn_id']
        verify_sign = sign_api.verifySinature(sign_url, data[0]['callback_token'])
        if verify_sign:
            return verify_sign
        else:
            return False

    def _verify_app_status(self, app_id):
        '''
            # 验证下游的 APP 状态是否可用
        '''
        verify_app = None
        data = self.chnmodel.verify_app_status(chn_id, app_id)[0]
        if not data:
            raise BaseException(BaseError.ERROR_APP_NOT_EXIST)
        elif int(data['app_status']) == 0 and int(data['app_status']) is None:
            raise BaseException(BaseError.ERROR_APP_VERIFY_NOT_PASS)
        elif data['chn_status'] == 0 or data['chn_status'] is None:
            raise BaseException(BaseError.ERROR_CHN_VERIFY_NOT_PASS)
        elif int(data['app_status']) == 1 and int(data['chn_status']) == 1:
            verify_app = True
            return verify_app
        else:
            raise BaseException(BaseError.ERROR_COMMON_DATABASE_EXCEPTION)

@urls.processor(BaseConstant.LIST_OFFER_ALL)
class ListAllOffer(BaseProcessor):

    def __init__(self, handler):
        '''
        Constructor
        '''
        BaseProcessor.__init__(self, handler)

    @gen.coroutine
    def process(self):
        data = self.offermodel.get_all_offer(self.params['page_size'], self.params['page'])
        if data:
            retdata = {
                'offers': data
            }
            return_data = retdata
            return return_data
        else:
            raise BaseException(BaseError.ERROR_COMMON_DATABASE_EXCEPTION)
