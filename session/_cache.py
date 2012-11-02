# coding: utf-8
import redis
import settings

_REDIS_SERVERS = {}
def get_cache(name='social'):
    global _REDIS_SERVERS
    cache = _REDIS_SERVERS.get(name)
    if not cache:
        server_setting = settings.CACHE_SERVERS.get(name)
        if not server_setting:
            raise ValueError(u'未知服务器设置 %s' % name)
        server_setting = server_setting.split(':')
        server_setting[-1] = int(server_setting[-1])
        cache = redis.StrictRedis(*(server_setting))
        _REDIS_SERVERS[name] = cache
    return cache
