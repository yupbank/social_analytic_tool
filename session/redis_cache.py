__author__ = 'yupbank'
# coding: utf-8
import functools
import operator
import redis
import settings
from session import RedisSessionStore

_redis_servers = {}
for key, value in settings.CACHE_SERVERS.items():
    _redis_servers[key] = redis.StrictRedis(*value)

_redis_store = RedisSessionStore(_redis_servers['social'])

def get_store():
    return _redis_store

class CacheManager(object):
    def __init__(self, server='social'):
        self.cache = _redis_servers[server]

    # key -> value
    def get_by_key(self, key):
        return self.cache.get(key)

    # key* -> [key1, key2, key3]
    def get_keys(self, pattern):
        return self.cache.keys(pattern)

    # key ->list -> list[start:end]
    def get_sort_list(self, key, start, end):
        return self.cache.zrange(key, start, end)

    # [get_by_key(refix + key) for key in keys]
    def get_by_keys(self, prefix, keys):
        properties = self.cache.mget(map(functools.partial(operator.add, prefix), keys))

        return dict(zip(keys, properties))

    def exists(self, key, value):
        return self.cache.zscore(key, value)

    def get_list_by_keys(self, name, prefix, properties, count, start, desc=True):
        """获取新闻列表

        Args:
            key: Key
            start: 开始Offset
            count: 数量
        """


        if desc:
            ids = self.cache.zrevrange(name, start, start + count - 1)
        else:
            ids = self.cache.zrange(name, start, start + count - 1)
        prefix  += ':%s.'
        query_keys = map(functools.partial(operator.add, prefix), properties)
        keys = []
        for id in ids:
            keys.extend(map(lambda key: key % id, query_keys))

        if not ids:
            return []
        l = self.cache.mget(*keys)

        key_count = len(properties)

        objs = []
        for i, _id in enumerate(ids):
            begin = key_count * i
            end = key_count * (i + 1)
            obj = dict(zip(properties, l[begin:end]))
            obj['id'] = _id
            objs.append(obj)

        return objs

    def index(self, name, key):
        return self.cache.zrank(name, key)

    def get_by_rank(self, name, rank):
        if rank < 0:
            return None

        results = self.cache.zrange(name, rank, rank)
        if results:
            return results[0]

        return None

    def set(self, name, value, expire=None):
        if expire:
            self.cache.set(name, value)
            self.cache.expire(name, expire)
        else:
            self.cache.set(name, value)

    def zcount(self, name, min, max):
        return self.cache.zcount(name, min, max)
