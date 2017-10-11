# _*_ coding:utf-8_*_
import time

from model.admin_model import AdminModel
from model.advertise_model import AdvertiseModel, AdvertiserModel
from model.am_model import AccountManagerModel
from model.application_model import ApplicationModel
from model.channeler_model import ChannelModel
from model.click_model import ClickModel
from model.install_click_model import InstallClickModel
from model.offer_model import OfferModel

class BaseProcessor(object):
    '''
    classdocs
    '''
    def __init__(self, handler):
        '''
        Constructor
        '''
        self.handler = handler
        self.application = handler.application
        self.params = handler.params
        self.cmdid = handler.cmdid
        # self.userid = handler.userid
        # self.userkey = handler.userkey
        # self.timestamp = handler.timestamp
        # self.token = handler.xrsf_token

        # 当前时间戳(秒)
        self.NTIME = int(time.time())

        # logger
        self.tracker = handler.tracker
        self.sys_logger = handler.sys_logger

        # databases
        db_conns = self.application.db_conns

        self.adminmodel = AdminModel(db_conns['read'], db_conns['write'])
        self.advermodel = AdvertiseModel(db_conns['read'], db_conns['write'])
        self.adermodel = AdvertiserModel(db_conns['read'], db_conns['write'])
        self.ammodel = AccountManagerModel(db_conns['read'], db_conns['write'])
        self.appmodel = ApplicationModel(db_conns['read'], db_conns['write'])
        self.chnmodel = ChannelModel(db_conns['read'], db_conns['write'])
        self.clickmodel = ClickModel(db_conns['read'], db_conns['write'])
        self.installclickmodel = InstallClickModel(db_conns['read'], db_conns['write'])
        self.offermodel = OfferModel(db_conns['read'], db_conns['write'])
