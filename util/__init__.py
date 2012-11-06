#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__init__.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''

import _env
import config
import tornado.httpclient
import json
import time
import urllib

def lower_name(class_name):
    """
    >>>lower_name("UserCount")
    'user_count'

    >>>lower_name("user_count")
    'user_count'
    """
    result = []
    for c in class_name:
        i = ord(c)
        if 65 <= i <= 90:
            if result:
                if not 48 <= ord(result[-1]) <= 57:
                    result.append('_')
            i += 32
            c = chr(i)
        result.append(c)
    return ''.join(result)

def get_json(url, **kwargs):
    res = syncdownload(url, **kwargs)
    try:
        res = json.loads(res.body)
    except Exception,e:
        raise e
    return res

def auth_key_json(url, **kwargs):
    link = '%s?key=%s'%(url,config.BROWSE_KEY)
    if kwargs:
        link = '%s&%s'%(link, urllib.urlencode(kwargs))
    print link
    return get_json(link)

def authrize_json(url, access_token, token_type, **kwargs):
    headers = {'Authorization':'%s %s'%(token_type, access_token)}
    return get_json(url, headers=headers, **kwargs)

def syncdownload(url, request_timeout=config.TIME_OUT, **kwargs):
    http_client = tornado.httpclient.HTTPClient()
    return http_client.fetch(url, request_timeout=request_timeout, **kwargs)

def time_plus(seconds):
    t = time.time()+seconds
    return t

def conver_to_stamp(my_time, format_str='%Y-%m-%D %H:%M:%S'):
    t = time.stptime(format_str, my_time)
    return t

def cover_stamp_to_time(my_stamp, format_str='%Y-%m-%D %H:%M:%S'):
    t = time.strtime(format_str, my_stamp)
    return t
