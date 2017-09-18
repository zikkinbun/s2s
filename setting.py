# _*_ coding:utf-8_*_

import codecs
import socket
import os
from db import db_setting
import sys

# 避免 utf-8mb4的错误
# from tornado.options import options
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
#设置sys的默认编码是utf-8
reload(sys)
sys.setdefaultencoding('utf-8')  # @UndefinedVariable

# 生产环境IP
PRODUCT_HOSTS =['127.0.0.1', '172.31.5.107']
# 测试环境IP
DEV_HOSTS = ['127.0.0.1', '192.168.1.52', '192.168.8.101', 'benson-MacBookPro']

# 本机IP
# LOCAL_HOST = socket.gethostbyname(socket.gethostname())
LOCAL_HOST = '192.168.1.52'
# print  LOCAL_HOST

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
# print LOG_DIR


# 根据不同环境而不同的配置
# Product environment
if LOCAL_HOST in  PRODUCT_HOSTS:

    # 日志目录
    # LOG_DIR = './logs'
    # 数据库配置
    DATABASE = db_setting.RELEASE

else:
    # 非正式环境
    if LOCAL_HOST in DEV_HOSTS:
        # 测试环境
        # LOG_DIR = './logs'
        REDIS = '127.0.0.1:6379'
        DATABASE = db_setting.DEV
    else:
        print 'current host is not in dev hosts or release hosts'
