# _*_ coding:utf-8_*_
import pymysql.cursors

local_config = {
          'host':'127.0.0.1',
          'port':3306,
          'user':'db_admin',
          'password':'db_admin2015',
          'db':'s2s',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }

dev_config = {
          'host':'127.0.0.1',
          'port':3316,
          'user':'db_admin',
          'password':'db_admin2015',
          'db':'s2s',
          'charset':'utf8mb4',
          'cursorclass':pymysql.cursors.DictCursor,
          }
# Connect to the database
connection = pymysql.connect(**dev_config)
