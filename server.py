#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
server.py
Author: yupbank                                                                   
Email:  yupbank@gmail.com

Created on                                                                        
2012-11-02 
"""

import tornado.ioloop
import tornado.autoreload
import tornado.options
from tornado.options import define, options
from app import Application


define("port", default=9999, help="run on the given port", type=int)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    print "start on port %s..."%options.port
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == '__main__':
    main()
