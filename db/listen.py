# _*_ coding:utf-8_*_

import redis

pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=1)
r = redis.StrictRedis(connection_pool=pool)
p = r.pubsub()
p.subscribe('excelFile')
for item in p.listen():
    print item
    if item['type'] == 'message':
        data =item['data']
        r.set('s', 32)
        print data
        if item['data'] == 'over':
            break;
p.unsubscribe('spub')
print '取消订阅'
