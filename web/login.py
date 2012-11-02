#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
login.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''

import _env
from base import BaseHandler

class Login(BaseHandler):
    def get(self):
        return self.render('login.html')
