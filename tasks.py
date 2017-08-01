# _*_ coding:utf-8_*_
from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab

from advertise_handler import Advertises
from rule_handler import specailRule
from offer_handler import AdvertiseTransOffer

from threading import Thread

app = Celery("tasks", broker='redis://127.0.0.1:6379/1')
app.conf.CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERYBEAT_SCHEDULE = {
        "every_15minutes_run":{
            "task":"tasks.getOffer",
            "schedule":crontab(minute='*/15'),
            },
        },
)

@app.task
def getOffer():
    adxmi = Advertises()
    t = Thread(target=adxmi.getAdxmiOffer, args=('294daae457e8e335', 100, 1,))
    t.start()

def getRule():
    sp_rule = specailRule()
    value = sp_rule.getRule(2)
    print value

def tranOfferbyRule():
    add = AdvertiseTransOffer()
    sql = add.getRuleAdvertise(3)
    query = add.tranRuleOffer('q+aAyoS+p9Gnj0Ll962k0Q==')

def tranOfferbyOne():
    add = AdvertiseTransOffer()
    sql = add.getONEAdvertise('03184972')
    query = add.tranONEOffer('q+aAyoS+p9Gnj0Ll962k0Q==', '03184972')
