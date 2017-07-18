# _*_ coding:utf-8_*_
import json

def OfferSerializer(offers):
    _offers = []
    for offer in offers:
        _offer = {
            'offer_id': offer[0],
            'tittle': offer[1],
            'app_id': offer[2],
            'advertise_id': offer[3],
            'pkgname': offer[4],
            'category': offer[5],
            'icon_url': offer[6],
            'preview_url': offer[7],
            'click_url': offer[8],
            'os': offer[9],
            'os_version': offer[10],
            'payout': offer[11],
            'payout_currency': offer[12],
            'payout_type': offer[13],
            'creatives': offer[14],
        }
        _offers.append(json.dumps(_offer))
    return _offers
