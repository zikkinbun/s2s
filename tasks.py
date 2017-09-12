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

# if __name__ == '__main__':
#     resub()
