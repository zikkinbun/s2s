import json
from errors import BaseError
from common_utils import ComplexEncoder

class ResponseBuilder(object):
    '''
    响应
    '''

    @staticmethod
    def build_error(handler, e):
        '''
        返回错误

        Args:
            handler: torndb.web.RequestHandler object
            e: An instance of UFOException
        Returns:
            A json string
        '''
        print e
        # print handler
        res = {}
        res['retcode'] = e.code
        res['retmsg'] = e.message
        # res['timestamp'] = handler.timestamp
        # res['retcmdid'] = handler.cmdid
        res.update(e.ext)

        return res

    @staticmethod
    def build_success(handler, data=None):
        '''
        返回成功

        Args:
            handler: torndb.web.RequestHandler object
            data: data returned by processor
        Returns:
            A json string
        '''
        # print data
        # print handler
        res = {}
        res['retcode'] = BaseError.SUCCESS
        res['retmsg'] = BaseError.get_message(res['retcode'])
        # res['timestamp'] = handler.timestamp
        # res['retcmdid'] = handler.cmdid
        res['retdata'] = data if data is not None else {}

        return res
