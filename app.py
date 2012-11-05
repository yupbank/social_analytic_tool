#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
app.py
Author: yupbank                                                                   
Email:  yupbank@gmail.com

Created on                                                                        
2012-11-02 
"""

import tornado.web
import os.path
import uuid
from web import IndexHandler, GoogleLoginHandler, Login, UserHandler, Contact, About, Logout,\
                GroupHandler, NewGroupHandler, GroupList,\
                AddGroupHandler
from web.test import Test

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/test", Test),
            (r"/google_login", GoogleLoginHandler),
            (r"/login", Login),
            (r"/user/(\d+)", UserHandler),
            (r"/contact", Contact),
            (r"/about", About),
            (r"/logout", Logout),
            (r"/group/(\d+)", GroupHandler),
            (r"/group/(\d+)/add", AddGroupHandler),
            (r"/group/new/", NewGroupHandler),
            (r"/groups/", GroupList),
            (r"/groups-(\d+)/", GroupList),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape="xhtml_escape",
            debug = True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

