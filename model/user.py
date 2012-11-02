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
from time import time
#from session import Session, get_cache, RedisSessionStore, id_binary_decode, id_binary_encode
from os import urandom

#cache = get_cache()
#store = RedisSessionStore(cache)
#_session = Session.get_session(redis_store=store)

class User(Model):
    pass

class UserAuth(Model):
    pass

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
    #print user_session(100002)
    s = _session[100002]
    print s, '!!!'
    print user_id_by_session('ooYBAAasVNLNn38R2AvOF0')
