# _*_ coding:utf-8_*_
import sys
import time
import json
import traceback
import datetime
from hashlib import md5, sha1


class ComplexEncoder(json.JSONEncoder):
    '''
    encoder for json dumps
    '''

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, ObjectId):
            return obj.__str__()
        else:
            return json.JSONEncoder.default(self, obj)



def trace_error():
    '''
    trace exception info, output in sys.stdout
    '''

    etype, evalue, tracebackObj = sys.exc_info()[:3]
    print("Type: " , etype)
    print("Value: " , evalue)
    traceback.print_tb(tracebackObj)

# #
# @brief 将datetime转化为str
# @param formate 要转化的str的格式，默认为%Y-%m-%d
def datetime_to_str(datetime, formate='%Y-%m-%d'):
    return datetime.strftime(formate)

# #
# @brief 将datetime转化为时间戳
#
def datetime_to_timetuple(date_time):
    time.mktime(date_time.timetuple())

# #
# @brief 将时间戳转化为str
#
def timetuple_to_str(timetuple, formate='%Y-%m-%d'):
    time.strftime(formate, time.localtime(timetuple))

def request_to_dict(request):
    '''
    将x-www-form-urlencoded形式的参数转化为dict
    '''

    arguments = {}
    map(lambda name: arguments.setdefault(name, request.arguments[name][0] if len(request.arguments[name]) == 1 else request.arguments[name]), request.arguments)

    return arguments

def is_web_request(user_agent):
    '''
    通过user_agent判断是否是web请求
    '''

    platforms = ['iPod', 'iPhone', 'iPad', 'Android']

    for item in platforms:
        if item in user_agent:
            return False

    return True

##
# @brief 将对象实例转化为dict
# @param obj 对象的实例
#
#
def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d


###
#@brief 将dict转化为对象
#@param d dict的对象
#
def dict2object(d):
    #convert dict to object
    if '__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
    else:
        inst = d
    return inst
