# _*_ coding:utf-8_*_
from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab

from handler.advertise_handler import Advertises
from handler.rule_handler import SpecailRule
from handler.offer_handler import AdvertiseTransOffer

from threading import Thread
import re

app = Celery("tasks", broker='redis://127.0.0.1:6379/1')
app.conf.CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE = {
        "every_30minutes_run":{
            "task":"tasks.getOffer",
            "schedule":crontab(minute='*/30'),
            },
        },
)

@app.task
def getOffer():
    adxmi = Advertises()
    t = Thread(target=adxmi.getAdxmiOffer, args=('294daae457e8e335', 100))
    t.start()

def getValidClick():
    pass

def getRule():
    sp_rule = SpecailRule()
    value = sp_rule.getRule(2)
    print value

def tranoffer():
    adt = AdvertiseTransOffer()
    data = adt.getRuleAdvertise(2)
    print data

def sqltest():
    line = '{get_price} >= 1'
    params = re.split(' ', line)
    table = 'advertise'
    fields = ['ad_id', 'ad_name', 'pkg_name', 'region', 'category', 'icon_url', 'preview_url', 'get_price', 'payout_type', 'os', 'os_version', 'creatives', 'description', 'status']

    items = ['SELECT ']
    if not fields:
        items.append('*')
    else:
        for field in fields:
            items.append(field+',')
    sql_str = ''.join(items)
    sql_str = sql_str[0:len(sql_str)-1] + " FROM " + table

    condition_str = ''
    condition_list = [' WHERE get_price']
    condition_list.append(params[1])
    condition_list.append(params[2])
    condition_str = ''.join(condition_list)

    sql = sql_str + condition_str
    print sql

def resub():
    text = 'http://ibrainer.net/cy/100/iPhone7_cy/?referrer ​=1​866'
    text1 = 'Hot & Sweet" Korean Drama(Vodacom)"'

    data = text.replace(' ', '').replace('%', '')
    # data1 = text1.replace('"', '')
    print data

if __name__ == '__main__':
    resub()
