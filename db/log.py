# _*_ coding:utf-8_*_

import logging

logger=logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh=logging.FileHandler('info.log')
fh.setLevel(logging.INFO)

formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
