# _*_ coding:utf-8_*_
from handler.advertise_handler import Advertises, Advertiser, AdvertiseStatus
from handler.offer_handler import AdvertiseTransOffer, OfferHandler
from handler.rule_handler import RuleHandler, selectRule, specailRule
from threading import Thread

import tasks



if __name__ == '__main__':
    # test = getOffer.delay()
    # tasks.getOffer()
    adxmi = Advertises()
    # adxmi.verifyPullstatus()
    adxmi.getAdxmiOffer('294daae457e8e335', 100)
    # t = Thread(target=adxmi.getAdxmiOffer, args=('294daae457e8e335', 100))
    # t.start()
    # test = AdvertiseStatus()
    # msg = test.getDeviceInfo('2125151')
    # print msg


# offer = AdvertiseTransOffer('EUIXgvfdSFShEk6TchD7Ug==','01372486')
# data = offer.getAdvertise()
# tran = offer.tranOffer()

# callback = OfferCallback()
# callback.getValidClick()
