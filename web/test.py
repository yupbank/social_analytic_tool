#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
test.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-05
'''
import _env
import tornado.web
import tornado.gen
import tornado.httpclient as httpclient
from base import BaseHandler
import time
from model import Group, GroupInfo

class Test(BaseHandler):
    def get(self):
        self.finish("""
        {"nodes": [{"index": "112100305315359676269", "out": 2, "name": "peng yu", "weight": 3, "in": 1}, {"index": "105572065560802366642", "out": 1, "name": "\u6709\u8da3\u8c46\u74e3", "weight": 3, "in": 2}], "edges": [{"target_name": "\u6709\u8da3\u8c46\u74e3", "source": "112100305315359676269", "counts": 2, "source_name": "peng yu", "target": "105572065560802366642"}, {"target_name": "peng yu", "source": "105572065560802366642", "counts": 1, "source_name": "\u6709\u8da3\u8c46\u74e3", "target": "112100305315359676269"}]};
        """.strip())
        #p = yield tornado.gen.Task(self.take_long)
        #print p
        #self.finish('watiteing')
        

    def take_long(self, callback):
        time.sleep(10)
        print '1-10'
        return callback('yes')
