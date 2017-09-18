# _*_ coding:utf-8_*_

class BaseConstant(object):
    # 关闭server的时候，最长等待的时间
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5

    #协议号
    CMD_LOGIN = 1
    # 应用列表
    CMD_GET_APP_LIST = 2
