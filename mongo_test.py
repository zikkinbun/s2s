import pymongo
import datetime

conn = pymongo.MongoClient("mongodb://db_admin:db_admin2017@112.74.182.80:27017/S2S")

db = conn['S2S']

db.Applications.insert({
    'app_id': '86154845',
    'app_name': 's2stest',
    'app_secret': 'fafafsfdgsgds',
    'guest_id': '1',
    'os': 'ios',
    'contact_email': 'test@test.com',
    'requests': '100',
    'click': '80',
    'installed': '70',
    'payment': '',
    'am_id': '1',
    'dev_income': '3.0',
    'ad_output': '0.5',
    'countries': 'CHN',
    'unit_price': '1.0',
    'preview_url': 'http://test.test.com',
    'icon_url': 'http://test.tet.com',
    'createdate': datetime.datetime.utcnow(),
    'status': 'passed',
    'operation': 'active'
})

db.Union.insert({
    'union_id': '1',
    'union_key': 'aaaaaaaa',
    'account': 'test',
    'contact': 'bensonma',
    'level': '3',
    'running_sum': '999',
    'before_filter': '333',
    'after_filter': '222',
    'status': 'testing',
    'comment': 'testtgest',
    'createdate': datetime.datetime.utcnow()
})

db.Advertises.insert({
    'ad_id': '1',
    'ad_name': 'asasasas',
    'app_id': '86154845',
    'ad_txt': 'fsafsadasdsad',
    'region': ['CHN', 'JPN', 'HK'],
    'union_id': '1',
    'ader_bid': '10',
    'ader_expenses': '5',
    'dev_income': '2'
})

db.Guests.insert({
    'guest_id': '1',
    'guest_name': 'aaa',
    'contact_type': 'email',
    'email': 'test@gmail.com',
    'identify': 'developer',
    'country': 'CHN',
    'province': 'guangdong',
    'city': 'guangzhou',
    'sign_up_date': datetime.datetime.utcnow(),
    'sign_up_type': 'foreign',
    'status': 'actived',
    'am_id': '1',
    'sign': 'aaaaaaasdsdsdsd',
    'operation': {
        'type': 'aaaa',
        'allow': '1'
    }
})

db.AM.insert({
    'user_id': '1',
    'user_name': 'test',
    'app_id': ['1', '2', '23'],
    'income': '111',
    'output': '88',
    'total': '20'
})

db.catch_package_img.insert({
    'img_id': '1',
    'type': 'jpg',
    'heigh': '100',
    'width': '100',
    'url': 'http://ad.google.com'
})
