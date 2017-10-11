# _*_ coding:utf-8_*_

from handler.base_handler import BaseHandler
from callback.advertise_callback import AdvertiseCallback

from handler.channel_handler import ChannelerLogin, countChnAppIncome
from handler.am_handler import AMSginup, AMChannelOper, AMAppOper, AMLogin, AMChannelSignup, \
    AMListChannel, AMCreateOfferByUnion, AMCountAdIncome, AMIncome
from handler.offer_handler import OfferHandler
from handler.click_handler import ClickUrlHandler
from handler.install_click_handler import getAppInstall, getAppRecvInstall, getAppClick, getAppValidClick
from handler.advertise_handler import Advertiser, getAdvertiseById, getAdvertiseAll, \
    getAdvertiseByGetPrice, getAdvertiserALL, getAdverIncome, UpdateAdverStatus
from handler.cookietoken_handler import XSRFTokenHandler
from handler.applicaiton_handler import CreateApplication, ListApplication, SetCallbackUrl, getApplicationDetail, \
    ListAllApp, getAppTokenUrl, UpdateAppCallbackUrl, SetDeductionPartition, getAppIncome
from handler.pagenotfound_handler import PageNotFoundHandler

# handler路由
handlers = [
    (r"/v1/chn/login", ChannelerLogin),
    (r"/v1/app/create", CreateApplication),
    (r"/v1/app/active", AMAppOper),
    (r"/v1/app/list", ListApplication),
    (r"/v1/app/listAll", ListAllApp),
    (r"/v1/app/setting", SetCallbackUrl),
    (r"/v1/app/detail", getApplicationDetail),
    (r"/v1/app/getTokenUrl", getAppTokenUrl),
    (r"/v1/app/updateUrl", UpdateAppCallbackUrl),
    (r"/v1/app/SetDP", SetDeductionPartition),
    (r"/v1/am/signup", AMSginup),
    (r"/v1/am/createchn", AMChannelSignup),
    (r"/v1/am/listchn", AMListChannel),
    (r"/v1/am/login", AMLogin),
    (r"/v1/am/setstatus", AMChannelOper),
    (r"/v1/am/createAder", Advertiser),
    (r"/v1/am/createOfferByUnion", AMCreateOfferByUnion),
    (r"/v1/am/updateAderStatus", UpdateAdverStatus),
    (r"/v1/ad/getAdById", getAdvertiseById),
    (r"/v1/ad/getAdAll", getAdvertiseAll),
    (r"/v1/ad/getAdByPrice", getAdvertiseByGetPrice),
    (r"/v1/ad/getAder", getAdvertiserALL),
    (r"/v1/count/getAppInstall", getAppInstall),
    (r"/v1/count/getAppRecvInstall", getAppRecvInstall),
    (r"/v1/count/getAppClick", getAppClick),
    (r"/v1/count/getAppValidClick", getAppValidClick),
    (r"/v1/count/getAppIncome", getAppIncome),
    # (r"/v1/count/getAdIncome", AMCountAdIncome),
    (r"/v1/count/getAMIncome", AMIncome),
    (r"/v1/count/getChnAppIncome", countChnAppIncome),
    (r"/v1/count/getAderIncome", getAdverIncome),
    (r"/v1/offline", OfferHandler),
    (r"/v1/click", AdvertiseCallback),
    (r"/v1/track", ClickUrlHandler),
    (r"/v1/token", XSRFTokenHandler),
    (r".*", PageNotFoundHandler)
]

# 协议号和processor的映射
processor_mapping = {}

def processor(cmdid, is_internal=False):
    '''
    装饰器, 用于装饰processor中的主类
            作用是建立协议号和主类的映射
    '''
    def _module_dec(cls):
        processor_mapping[cmdid] = cls, is_internal
        # print cls
        # print is_internal
        return cls
    # print _module_dec
    return _module_dec
