# _*_ coding:utf-8_*_
import json

def OfferSerializer(offers):
    _offers = []
    for offer in offers:
        _offer = {
            'offer_id': offer['offer_id'],
            'tittle': offer['tittle'],
            'app_id': offer['app_id'],
            'advertise_id': offer['advertise_id'],
            'pkgname': offer['pkgname'],
            'category': offer['category'],
            'icon_url': offer['icon_url'],
            'preview_url': offer['preview_url'],
            'click_url': offer['click_url'],
            'os': offer['os'],
            'os_version': offer['os_version'],
            'region': offer['region'],
            'payout': offer['payout'],
            'payout_currency': offer['payout_currency'],
            'payout_type': offer['payout_type'],
            'creatives': offer['creatives'],
        }
        _offers.append(json.dumps(_offer))
    return _offers
