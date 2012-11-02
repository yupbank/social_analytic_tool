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

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape="xhtml_escape",
        )
        tornado.web.Application.__init__(self, handlers, **settings)

