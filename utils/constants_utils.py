# _*_ coding:utf-8_*_

class BaseConstant(object):
    # 关闭server的时候，最长等待的时间
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5

    # 协议号
    CMD_LOGIN = 1

    # 应用相关协议
    LIST_APP_ALL = 2
    LIST_APP_BY_CHNID = 3
    CREATE_APP = 4
    GET_APP_DETAIL = 5
    GET_APP_TOKENURL = 6
    UPDATE_APP_CALLBACKURL = 7
    SET_APP_CALLBACKURL = 8
    SET_DP = 9
    GET_APP_INCOME = 10

    # 广告相关协议
    GET_AD_BY_ID = 11
    GET_AD_BY_GETPRICE = 12
    GET_AD_ALL = 13
    CREATE_ADER = 14
    GET_ADER = 15
    GET_ADER_INCOME = 16
