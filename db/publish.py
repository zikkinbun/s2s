# _*_ coding:utf-8_*_

import redis
from mysql import connection

pool=redis.Redis(host='127.0.0.1',port=6379,db=0)
r = redis.StrictRedis(connection_pool=pool)

def test():
    while True:
        input = raw_input("publish:")
        if input == 'over':
            print '停止发布'
            break
        r.publish('spub', input)

def dotest():
    while True:
        query = 'select app_click_id,offer_id from track_click where vilid="%d" ORDER BY updatetime LIMIT 1' % int(1)
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            r.publish('vilidClick', data)
        else:
            break
