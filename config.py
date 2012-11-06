#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
config.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-02
'''
import platform

DEBUG = True

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = '3306'
MYSQL_MAIN = 'social_blogger'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'root'

DB_HOST_MAIN = '%s:%s:%s:%s:%s' % (
    MYSQL_HOST, MYSQL_PORT, MYSQL_MAIN, MYSQL_USER, MYSQL_PASSWD
)

DB_MAIN_TABLE = (
        '*',
        'user',
)
DB_CONFIG = {
    'main': {
        'master': DB_HOST_MAIN,
        'tables': DB_MAIN_TABLE,
    },
}

CACHE_SERVERS = {
            'social':'127.0.0.1:6379'
            }
SESSION_DEFAULT_EXPIRE = 60 * 60 * 24 * 365  # Session中某一项的失效时间
SESSION_FIRST_EXPIRE = 60 * 15              # 用户第一次访问，Session本身的失效时间
SESSION_SECOND_EXPIRE = 60 * 60 * 24 * 30   # 用户第二次访问，Session本身的失效时间

if 'laptop' in platform.node():
    CLIENT_ID = '727469625538-e6gb033obi5ac1im530h8cdhel7pok8u.apps.googleusercontent.com'
    CLIENT_SECRET = 'aCHF_iL80l1fCZqxA2JQ2Jt3'
    REDIRECT_URI = 'http://localhost:9999/google_login'
else:
    CLIENT_ID = '727469625538.apps.googleusercontent.com'
    CLIENT_SECRET = 'DT97zk6SlgDSwjODibHmO5nK'
    REDIRECT_URI = 'http://social-blogger.tk/google_login'
BROWSE_KEY = 'AIzaSyCQP1O5vJmsG0p2Z1vjAtzLDgC7WWnhnpo'

TIME_OUT = 1
