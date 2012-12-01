#!/usr/bin/env python
# -*- coding: utf-8 -*-

from marshal import dumps, loads
from json import dumps as json_dumps, loads as json_loads
from gzip import GzipFile

def tofile(f , obj):
    out = GzipFile(f, 'wb')
    out.write( json_dumps(obj) )
    out.close()

def fromfile(f):
    infile = GzipFile(f)
    result = json_loads(infile.read())
    infile.close()
    return result



if __name__ == '__main__':
    tofile('z', {2:2})
    print fromfile("z")
