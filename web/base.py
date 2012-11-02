#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
base.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-02
'''

import _env
import tornado.web
from mako.template import Template
from mako.lookup import TemplateLookup
from os.path import join
from os.path import dirname,abspath
from model import User
from util import lower_name

PREFIX  = dirname(dirname(abspath(__file__)))
MAKOLOOKUP = dict(
            directories=join(PREFIX,'templates'),
            disable_unicode=True,
            encoding_errors="ignore",
            default_filters=['str', 'h'],
            #input_encoding='utf-8',
            output_encoding=''
            )
MYLOOKUP = TemplateLookup(**MAKOLOOKUP)

def tee(func):
    def _(*args, **kwargs):
        print args, kwargs, '!!!'
        print func, '---'
        s = func(*args, **kwargs)
        print s, '+++'
        return s
    return _


def login_required(func):
    def _(self, *args, **kwargs):
        if not self.current_user:
            return self.redirect('/login')
        return func(self, *args, **kwargs)
    return _


class BaseHandler(tornado.web.RequestHandler):
    def render(self, template_name=None, **kwds):
        if template_name is None:
            if not hasattr(self, 'template'):
                self.template = '%s/%s.htm' % (
                    self.__module__.replace('.', '/'),
                    lower_name(self.__class__.__name__)
                )
            template_name = self.template
        current_user = self.current_user
        kwds['current_user'] = current_user
        kwds['request'] = self.request
        kwds['this'] = self
        #kwds.update(RENDER_KWDS)
        mytemplate = MYLOOKUP.get_template(template_name)
        content = mytemplate.render(**kwds)
        if not self._finished:
            self.finish(content) 

    def get_current_user(self):
        key = 'S'
        user_id = self.get_secure_cookie(key)
        if user_id:
            user = User.get(user_id)
            return user
