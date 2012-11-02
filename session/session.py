#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env

import struct
import time
import uuid, OpenSSL
import redis
from settings import CACHE_SERVERS
import settings
from base64 import urlsafe_b64encode, urlsafe_b64decode
from os import urandom
from struct import pack, unpack
import binascii


DEFAULT_ALPHABET = 'ZUBJA01FlhNWKmbX2DrzEpysoL7OvMcQPjV4Rn9t3gdT5xakwI6qufYGCHSei8'

def num2string(num):
    numbers = []

    while num:
        num, remain = divmod(num, len(DEFAULT_ALPHABET))
        numbers.insert(0, DEFAULT_ALPHABET[remain])

    return ''.join(numbers)

def ip_to_int(ip):
    st = ip.split('.')
    return (int(st[0]) << 24) + (int(st[1]) << 16) + (int(st[2]) << 8) + (int(st[3]))

def int_to_ip(number):
    s = []
    while number:
        s.append(str(number & 255))
        number >>= 8
    return '.'.join(reversed(s))

def encode_number(x):
    return struct.pack('>I', x)

def decode_number(x):
    return struct.unpack('>I', x)[0]

def generate_user_id():
    return num2string(int(uuid.UUID(bytes = OpenSSL.rand.bytes(16)).get_hex(), 16))

class RedisSessionStore(object):

    def __init__(self, redis_connection,):
        self.redis = redis_connection

    def generate_id(self, ):
        return num2string(int(uuid.UUID(bytes = OpenSSL.rand.bytes(16)).get_hex(), 16))

    @staticmethod
    def decode_data(value):
        return decode_number(value[:4]), decode_number(value[4:8]), value[8:]

    @staticmethod
    def encode_data(access_time, expiration, data):
        return encode_number(access_time) + encode_number(expiration) + data

    def get_full(self, sid, name):
        value = self.redis.hget(sid, name)
        if value:
            (access_time, expiration, data) = self.decode_data(value)
            now = int(time.time())
            if now - access_time > expiration:
                self.redis.hdel(sid, name)
                return None, None, None
            else:
                self.redis.hset(sid, name, self.encode_data(now, expiration, data))
                return access_time, expiration, data
        return None, None, None

    def get(self, sid, name):
        access_time, expiration, data = self.get_full(sid, name)
        return data

    def set(self, sid, name, data, expiration=None):
        if not expiration:
            expiration = settings.SESSION_DEFAULT_EXPIRE
        self.redis.hset(sid, name, self.encode_data(int(time.time()), expiration, data))

    def keys(self, sid):
        return (key for key in self.redis.hkeys(sid) if not key.startswith('_.'))

    def delete(self, sid, name):
        self.redis.hdel(sid, name)
        if not self.len(sid):
            self.redis.delete(sid)

    def len(self, sid):
        return len(list(self.keys(sid)))

    def has_key(self, sid, name):
        return self.redis.hexists(sid, name)

    def exists(self, sid):
        return self.redis.exists(sid)

    def clear(self, sid):
        self.redis.delete(sid)

    def expire(self, sid, expiration):
        self.redis.expire(sid, expiration)

class Marker(object):
    def __init__(self, ip=None, mark_time=None):
        self.time = mark_time if mark_time else int(time.time())
        self.ip = ip if ip else '0.0.0.0'

    @classmethod
    def load(cls, data):
        time = decode_number(data[:4])
        ip = int_to_ip(decode_number(data[4:8]))
        return cls(ip, time)

    def encode(self):
        return encode_number(self.time) + encode_number(ip_to_int(self.ip))

    def __str__(self):
        return 'ip:%s time:%s' % (self.ip, self.time)


class Session(object):
    """为Tornado实现Session功能

    此Session作为Server Side Cookie功能来实现，具有以下特性：
    1. Session较长时间保存，如一个月。
    2. Session可以存放比传统Session更多的数据。

    Session定义：
        create_info: 创建时间及IP等信息
        update_info: 修改时间及IP等信息
        access_info: 最后获取时间及IP等信息

    设置:
    Session['a'] = a

    获取
    Session['a']

    """

    ACCESS_MARKER_KEY = '_.a'
    CREATE_MARKER_KEY = '_.c'
    UPDATE_MARKER_KEY = '_.u'

    def set_marker(self, name):
        marker = Marker(self.access_ip)
        self._store.set(self._session_id, name, marker.encode())

    def mark_create(self):
        self.set_marker(self.CREATE_MARKER_KEY)

    def mark_access(self):
        self.set_marker(self.ACCESS_MARKER_KEY)

    def mark_update(self):
        self.set_marker(self.UPDATE_MARKER_KEY)

    def generate(self):
        self._session_id = self._store.generate_id()
        self.mark_create()
        self.mark_update()
        self.mark_access()
        self.expire(settings.SESSION_FIRST_EXPIRE)

    def expire(self, expiration):
        self._store.expire(self._session_id, expiration)

    def load(self, session_id):
        if self._store.exists(session_id):
            self._session_id = session_id
            self.expire(settings.SESSION_SECOND_EXPIRE)
        else:
            self.generate()

    def __init__(self, session_store, session_id=None, ip=None):
        self._store = session_store
        self.access_ip = ip
        if not session_id:
            self.generate()
        else:
            self.load(session_id)

    def clear(self):
        self.mark_update()
        self._store.clear(self._session_id)

    def set(self, key, value, expire):
        self.mark_update()
        return self._store.set(self._session_id, key, unicode(value).encode('utf-8'), expire)

    @property
    def session_id(self):
        return self._session_id

    @property
    def access(self):
        return Marker.load(self._store.get(self._session_id, self.ACCESS_MARKER_KEY))

    @property
    def update(self):
        return Marker.load(self._store.get(self._session_id, self.UPDATE_MARKER_KEY))

    @property
    def create(self):
        return Marker.load(self._store.get(self._session_id, self.CREATE_MARKER_KEY))

    def get_key_access_time(self, key):
        access_time, expiration, data = self._store.get_full(self._session_id, key)
        return access_time

    def get_key_expire(self, key):
        access_time, expiration, data = self._store.get_full(self._session_id, key)
        return expiration

    def __getitem__(self, key):
        self.mark_access()
        value = self._store.get(self._session_id, key)

        if value:
            return value.decode('utf-8')

        return None

    def __setitem__(self, key, value):
        self.mark_update()
        print key, value.decode('U8', 'replace'), '!!'
        return self._store.set(self._session_id, key, value.decode('utf-8', 'replace').encode('U8'))

    def __delitem__(self, key):
        self.mark_update()
        self._store.delete(self._session_id, key)

    def __len__(self):
        self.mark_access()
        return self._store.len(self._session_id)

    def __contains__(self, key):
        self.mark_access()
        return self._store.has_key(self._session_id, key)

    def keys(self):
        self.mark_access()
        return self._store.keys(self._session_id)

    def __iter__(self):
        self.mark_access()
        for key in self._store.keys(self._session_id):
            yield key


    @classmethod
    def get_session(cls, sid=None, redis_store=RedisSessionStore(redis.StrictRedis('127.0.0.1', 6379))):
        return cls(redis_store, sid)


def user_id_by_base64(string):
    try:
        user_id = urlsafe_b64decode(string+'==')
    except (binascii.Error, TypeError):
        return 0
    else:
        return unpack('I', user_id)[0]

def id_binary_decode(session):
    if not session:
        return
    user_id = session[:6]
    value = session[6:]
    try:
        value = urlsafe_b64decode(value+'=')
    except (binascii.Error, TypeError):
        return None, None

    user_id = user_id_by_base64(user_id)

    return user_id, value

def id_binary_encode(user_id, session):
    user_id_key = pack('I', int(user_id))
    user_id_key = urlsafe_b64encode(user_id_key)[:6]
    ck_key = urlsafe_b64encode(session)
    return '%s%s'%(user_id_key, ck_key)


if __name__ == '__main__':
    print CACHE_SERVERS,'!!!'
    print user_id_by_base64(100222)
    #r = RedisSessionStore(redis.StrictRedis('127.0.0.1', 6379))
    #start = time.time()
    #sids = []
    #for i in xrange(100):
    #    s = Session(r)
    #    s['a'] = 'a'
    #    s['b'] = 123
    #    s['c'] = 356
    #    s['d'] = 'abc'
    #    s['e'] = u'北京'
    #    sids.append(s.session_id)
    #print time.time() - start

    #start = time.time()
    #for sid in sids:
    #    s = Session(r, sid)
    #    m = Session(r, 'sddd')
    #    print m.session_id, '!!!'
    #    a = s['a']
    #    b = s['b']
    #    c = s['c']
    #    d = s['d']
    #    e = s['e']
    #print time.time() - start
