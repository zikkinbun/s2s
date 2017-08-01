# _*_ coding:utf-8_*_
from tornado_mysql import pools

import json

pools.DEBUG = True
POOL = pools.Pool(
        dict(host='127.0.0.1', port=3306, user='db_admin', passwd='db_admin2015', db='s2s', charset='utf8mb4'),
        max_idle_connections=1,
        max_recycle_sec=3)
