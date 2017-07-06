# _*_ coding:utf-8_*_
import json

def OfferSerializer(data, page, page_size):
    body = {
        'c': 0,
        'offer': [
            {
                'id': data[0],
                'name': data[1],
                'payout': data[5],
                'point': data[6],
                'cap': data[7],
                'preview_url': data[16],
                'countries': data[9],
                'store_label': data[21],
                'os': data[10],
                'task': data[4],
                'traffic': data[11],
                'os_version': data[12],
                'carrier': data[13],
                'nettype': data[15],
                'creatives': [
                    {
                        'mime': data[25],
                        'width': data[26],
                        'height': data[27],
                        'url': data[28]
                    }
                ],
                'size': data[22],
                'device': data[14],
                'mandatory_device': {
                    'imei': data[29],
                    'mac': data[30],
                    'idfa': data[31],
                    'ip': data[32],
                    'udid': data[33]
                },
                'icon_url': data[17],
                'adtxt': data[3],
                'package': data[2],
                'category': data[19],
                'tracknglink': data[8],
            },
        ],
        'total': 1,
        'page': page,
        'page_size': page_size,
        'n': 1
    }
    return json.dumps(body)
