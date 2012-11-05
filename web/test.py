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
    @tornado.gen.engine
    @tornado.web.asynchronous
    def get(self):
        id = self.current_user.id
        s = Group.where(user_id=id)
        info = GroupInfo.get_list(s.col_list(col='id'))
        print info
        self.finish('ok')
        #p = yield tornado.gen.Task(self.take_long)
        #print p
        #self.finish('watiteing')
        

    def take_long(self, callback):
        time.sleep(10)
        print '1-10'
        return callback('yes')
