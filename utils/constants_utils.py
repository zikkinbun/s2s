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

    # 下游相关协议
    CHN_LOGIN = 17
    GET_CHN_INCOME = 18

    # OFFER相关协议
    CHN_GET_OFFER = 19
    LIST_OFFER_ALL = 20

    # AM操作相关协议
    AM_SGINUP = 21
    AM_CHN_OPER = 22
    AM_APP_OPER = 23
    AM_LOGIN = 24
    AM_CHN_SIGNUP = 25
    AM_LIST_CHN = 26
    AM_LIST = 27
    AM_COUNT_ADER_INCOME = 28
    AM_CREATE_OFFER = 29

    # 点击操作相关操作
    CLICK_URL_BACK = 30

    # 安装数相关操作
    GET_APP_INSTALL = 31
    GET_APP_RECV_INSTALL = 32
    GET_APP_CLICK = 33
    GET_APP_VALID_CLICK = 34
    GET_CURRENT_APP_CLICK_INSTALL_INCOME = 35
