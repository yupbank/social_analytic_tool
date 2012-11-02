#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
info.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''
import _env
from base import BaseHandler

class Contact(BaseHandler):
    def get(self):
        return self.render('contact.html')

class About(BaseHandler):
    def get(self):
        return self.render('about.html')
