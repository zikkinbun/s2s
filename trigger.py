# _*_ coding:utf-8_*_
from advertise_handler import Advertises
from offer_handler import AdvertiseTransOffer, OfferHandler
from threading import Thread

# from tasks import getOffer
import tasks

if __name__ == '__main__':
    # test = getOffer.delay()
    tasks.getOffer()
    # adxmi = Advertises()
    # adxmi.verifyPullstatus()
    # adxmi.getAdxmiOffer('294daae457e8e335', 100, 1)
    # t = Thread(target=adxmi.getAdxmiOffer, args=('294daae457e8e335', 100, 1,))
    # t.start()

# offer = AdvertiseTransOffer('EUIXgvfdSFShEk6TchD7Ug==','01372486')
# data = offer.getAdvertise()
# tran = offer.tranOffer()

# callback = OfferCallback()
# callback.getValidClick()
