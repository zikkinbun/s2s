# _*_ coding:utf-8_*_
from tornado import gen

from processor.base_processor import BaseProcessor
from utils.constants_utils import BaseConstant
from utils.errors import BaseError, CommonError
from utils.exception import BaseException, DBException, ParamException

import re
import os
import urls
import json
import base64

@urls.processor(BaseConstant.CLICK_URL_BACK)
class ClickUrlProcessor(BaseProcessor):

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

        is_existed = self.checkUnique(self.params['app_click_id'])
        if is_existed == 2:
            click_id = base64.b64encode(os.urandom(12))
            track_data = self.clickmodel.get_trackurl(self.params['offer_id'])
            click_row = self.clickmodel.create_record(click_id, track_data['ad_id'], self.params['app_id'], self.params['app_click_id'], self.params['offer_id'])
            install_row = self.install_click_model.set_install_click(self.params['offer_id'], track_data['ad_id'], self.params['app_id'])
            update_row = self.install_click_model.update_recv_click(self.params['offer_id'], self.params['app_id'])
            track_link = trackinglink + '&user_id=%s' % click_id

            self.redirect(track_link)
            return True
        else:
            raise BaseException(BaseError.ERROR_COMMON_UNKNOWN)


    def checkUnique(self, app_click_id):
        data = self.clickmodel.check_duplication(app_click_id)
        if data and len(data) > 1:
            # this click is not unique
            return_data = 1
        elif data and len(data) == 1:
            # this click is unique
            return_data = 2
        else:
            # other error
            return_data = 3
