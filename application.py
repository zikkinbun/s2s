# _*_ coding:utf-8_*_
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado_crontab
from tornado.options import define, options

import os
import sys
import time
import redis
import torndb
import logging
import signal
import importlib
import ConfigParser

import urls
import setting

from datetime import datetime
from logging import config as logging_config

from utils.logs_utils import Tracker
from db import db_setting

define("port", default=8000, help="run on the given port", type=int)
_http_server_app = None

def initlog(port):

    def __fileConfig(config, disable_existing_loggers=True):
        """
        Read the logging configuration from a ConfigParser-format file.
        This can be called several times from an application, allowing an end user
        the ability to select from various pre-canned configurations (if the
        developer provides a mechanism to present the choices and load the chosen
        configuration).
        """

        formatters = logging_config._create_formatters(config)

        # critical section
        logging._acquireLock()
        try:
            logging._handlers.clear()
            del logging._handlerList[:]
            # Handlers add themselves to logging._handlers
            handlers = logging_config._install_handlers(config, formatters)
            logging_config._install_loggers(config, handlers, disable_existing_loggers)
        finally:
            logging._releaseLock()

    # 配置文件
    fname = sys.path[0]+'/logging.cfg'
    cp = ConfigParser.ConfigParser(None)
    if hasattr(fname, 'readline'):
        cp.readfp(fname)
    else:
        cp.read(fname)

    # 更改handler_sys和handler_track两个的args中的文件名, 把port拼接上
    for item in ['handler_sys', 'handler_track', 'handler_internalTrack']:
        args = list(eval(cp.get(item, 'args').strip()))
        log_dir = os.path.join(setting.LOG_DIR, os.path.dirname(args[0]))
        args[0] = os.path.join(setting.LOG_DIR, '%s_%s'% (args[0], port))
        cp.set(item, 'args', str(tuple(args)))
        # 初始化日志目录
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        __fileConfig(cp)

def shutdown_handler(sig, frame):
        logging.warning('Caught signal: %s', sig)
        tornado.ioloop.IOLoop.instance().add_callback(close_httpserver)

def close_httpserver():
        deadline = time.time() + constants.BaseConstant.MAX_WAIT_SECONDS_BEFORE_SHUTDOWN
        def stop_loop():

            now = time.time()
            io_loop = tornado.ioloop.IOLoop.instance()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                io_loop.stop()
                #关闭数据库连接
                for (k,v) in _http_server_app.db_conns.items():
                    if v:
                        if isinstance(v,redis.StrictRedis):
                            pass
                        else:
                            v.close()
                logging.info('Shutdown')
        stop_loop()
        logging.info(".....close_httpserver():ready")

class Application(tornado.web.Application):

    def __init__(self):
        start_time = time.time()

        settings = {
            "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            "xsrf_cookies": False,
            "login_url": "/v1/chn/login"
        }
        tornado.web.Application.__init__(self, handlers=urls.handlers, debug=True, **settings)

        self.tracker = Tracker('track')
        self.internal_tracker = Tracker('internalTrack')
        self.sys_logger = Tracker('root')

        self.db_conns = self._init_db()
        self._load_processor()

        end_time = time.time()
        logging.info('...server started, %sms used...'% ((end_time - start_time) * 1000))

    def _load_processor(self):
        '''
        加载processor, 将cmd_id和processor的关系映射在urls.processor_mapping中
        '''

        def __find_processor(args, dirname, files):
            for filename in files:
                filepath = os.path.join(dirname, filename)
                if filepath.endswith('.py'):
                    args[0].add(filepath[len(args[1]) + 1: -len('.py')].replace('/', '.').replace('\\', '.'))

#         base_dir = os.path.dirname(__file__)
        base_dir = os.getcwd()
        processors = set()
        os.path.walk(base_dir + '/processor', __find_processor, (processors, base_dir))
        for item in processors:
            importlib.import_module(item)

    def _init_db(self):
        """
            初始化数据库
        """
        db_conns = {}
        db_conns['read'] = torndb.Connection(db_setting.DEV['s2s']['read']['host'], db_setting.DEV['s2s']['read']['database'], db_setting.DEV['s2s']['read']['user'], db_setting.DEV['s2s']['read']['password'])
        db_conns['write'] = torndb.Connection(db_setting.DEV['s2s']['write']['host'], db_setting.DEV['s2s']['write']['database'], db_setting.DEV['s2s']['write']['user'], db_setting.DEV['s2s']['write']['password'])
        return db_conns

    def log_request(self, handler):
        """Writes a completed HTTP request to the logs.
        By default writes to the python root logger.  To change
        this behavior either subclass Application and override this method,
        or pass a function in the application settings dictionary as
        ``log_function``.
        """

        access_log = handler.tracker

        if "log_function" in self.settings:
            self.settings["log_function"](handler)
            return
        if handler.get_status() < 400:
            log_method = access_log.info
        elif handler.get_status() < 500:
            log_method = access_log.warn
        else:
            log_method = access_log.error
        request_time = 1000.0 * handler.request.request_time()
        log_method("HTTPResult:%d %s %.2fms"% (handler.get_status(), handler._request_summary(), request_time))


def main():
    global _http_server_app
    input_params = tornado.options.parse_command_line()

    port = options.port
    initlog(port)

    # signal.signal(signal.SIGINT, shutdown_handler)
    # signal.signal(signal.SIGTERM, shutdown_handler)

    _http_server_app = Application()
    http_server = tornado.httpserver.HTTPServer(_http_server_app)
    http_server.listen(port)

    # union_admix = Admix()
    # _func = functools.partial(union_admix.getAdxmiOffer('294daae457e8e335', 100), *["crontab"])
    # tornado_crontab.CronTabCallback(_func, "*/30 * * * *").start()
    # start it up
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
