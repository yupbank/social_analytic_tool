#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
user.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-02
'''
import _env
from _db import Model
import time
#from session import Session, get_cache, RedisSessionStore, id_binary_decode, id_binary_encode
from os import urandom
from config import CLIENT_ID, CLIENT_SECRET
GOOGLE_REFRESH_API = 'https://accounts.google.com/o/oauth2/token'
import requests
import urllib
import json
#cache = get_cache()
#store = RedisSessionStore(cache)
#_session = Session.get_session(redis_store=store)

CACHE_USER = {}

def cache(func):
    def _(self, id):
        if not id in CACHE_USER:
            CACHE_USER[id] = func(self, id)
        return CACHE_USER[id]
    return _

class User(Model):
    pass

class UserAuth(Model):

    def get_access_token(self):
        expire_time = time.mktime(time.strptime(self.expire_time, '%Y-%m-%d %H:%M:%S'))
        if expire_time < time.time():
            print 'refresh access_token!!!'
            data = dict(
                    client_id = CLIENT_ID,
                    client_secret = CLIENT_SECRET,
                    refresh_token = self.refresh_token,
                    grant_type = 'refresh_token'
                    )
            res = requests.post(GOOGLE_REFRESH_API, urllib.urlencode(data),  headers = {
                        'content-type': 'application/x-www-form-urlencoded',})
            res = json.loads(res.content)
            print res, '!!!'
            self.access_token = res.get('access_token')
            expire_time = time.time() + res.get('expires_in')
            self.expire_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time))
            self.save()
        return self.access_token
#def user_session(user_id):
#    s = _session[user_id]
#    print s, '!!!'
#    if not s:
#        s = urandom(12)
#        _session[user_id] = s
#    return id_binary_encode(user_id, s)
#
#def user_session_rm(user_id):
#    u = UserSession.where(id=user_id).update(value=None)
#    mc_user_session.delete(user_id)
#
#def user_id_by_session(session):
#    if not session:
#        return
#    user_id, value = id_binary_decode(session)
#    if not user_id:
#        return
#
#    db = _session[user_id]
#    if value == db.decode('U8'):
#        return user_id

if __name__ == "__main__":
    import md5
    for i in UserAuth.where():
        print i.get_access_token()
