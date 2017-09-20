# _*_ coding:utf-8_*_
from tornado import gen

from utils.constants_utils import BaseConstant
from processor.base_processor import BaseProcessor
import os
import urls
import random
import string
import base64

@urls.processor(BaseConstant.GET_AD_BY_ID)
class getAdvertiseById(BaseProcessor):
    '''
        根据广告商获取广告
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

        data = self.advermodel.get_advertise_by_AderId(self.params['ader_id'], int(self.params['page_size']), int(self.params['index']))
        total = self.advermodel.get_total_count_list(self.params['ader_id'])
        retdata = {
            'total': total['COUNT(*)'],
            'advertise': data,
            'index': index
        }
        return_data = retdata
        return return_data

@urls.processor(BaseConstant.GET_AD_BY_GETPRICE)
class getAdvertiseByGetPrice(BaseProcessor):
    '''
        获取广告
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

        data = self.advermodel.get_advertise_by_get_price(self.params['key'], self.params['value'])
        retdata = {
            'advertise': data,
        }
        return_data = retdata
        return return_data

@urls.processor(BaseConstant.GET_AD_ALL)
class getAdvertiseAll(BaseProcessor):
    '''
        获取所有广告
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

        data = self.advermodel.get_advertise_all(int(self.params['page_size']), int(self.params['index']))
        total = self.advermodel.get_total_count_all()
        retdata = {
            'total': total['COUNT(*)'],
            'advertise': data,
            'index': index
        }
        return_data = retdata
        return return_data

@urls.processor(BaseConstant.CREATE_ADER)
class getAdvertiseAll(BaseProcessor):
    '''
        创建广告主
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
        row = None
        duplicate = self.advermodel.check_duplicate_advertiser(self.params['api_name'])
        if duplicate:
            raise BaseException(BaseError.ERROR_ADER_ALREADY_EXIST)
        else:
            row = self.advermodel.set_advertiser(self.params['api_name'], self.params['name'], self.params['resp_callback_url'], self.params['resp_callback_token'], self.params['is_pulled'])

        return_data = row
        return return_data

@urls.processor(BaseConstant.GET_ADER)
class getAdvertiserALL(BaseProcessor):
    '''
        获取所有广告主
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

        data = self.advermodel.get_advertiser()

        retdata = {
            'union': data
        }

        return_data = retdata
        return return_data

@urls.processor(BaseConstant.GET_ADER_INCOME)
class getAdverIncome(BaseProcessor):
    '''
        获取所有广告主
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
        ader_id = self.params['ader_id']
        if ader_id == 'all':
            ader_data = []
            ader_list = self.adermodel.get_advertiser()
            for ader in ader_list:
                aderid = ader['id']
                advertise = self.admodel.count_all_advertise_income_by_id(aderid)[0]
                ader_data.append(advertise)
            return_data = retdata
            return return_data
        else:
            advertise = admodel.count_all_advertise_income_by_id(ader_id)[0]
            return_data = advertise
            return return_data
