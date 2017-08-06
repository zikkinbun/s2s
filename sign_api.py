# _*_ coding:utf-8_*_
from urlparse import urlparse
from urllib import unquote_plus
from hashlib import md5

def verifySinature(callback_url, callback_token):
    sign = None
    params = {}
    url_parse = urlparse(callback_url)
    query = url_parse.query
    query_array = query.split('&')

    for group in query_array:
        k, v = group.split('=')
        if k == 'sign':
            sign = v
        else:
            params[k] = unquote_plus(v)
    del k, v

    sorted_params = sorted(params.items(), key=lambda d: d[0])

    before_md5 = ''.join(['%s=%s' % (k, v) for k, v in sorted_params])
    before_md5 += callback_token

    m = md5()
    m.update(before_md5)
    return sign == m.hexdigest()

def sign_url(url, app_secret):
    sign = None
    params = dict()
    url_parse = urlparse(url)
    query = url_parse.query
    query_array = query.split('&')
    for group in query_array:
        k, v = group.split('=')
        if k == 'sign':
            sign = v
        else:
            params[k] = unquote_plus(v)

    str = ''
    sorted_params = sorted(params.items(), key = lambda d:d[0])
    for k, v in sorted_params:
        str += '%s=%s' % (k, v)
    str += app_secret

    # print str
    m = md5()
    m.update(str)
    sign = m.hexdigest()

    return '%s&sign=%s' % (url, sign)
