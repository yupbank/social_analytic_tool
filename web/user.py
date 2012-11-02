#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
user.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''
import _env
from base import BaseHandler, login_required

class UserHandler(BaseHandler):
    @login_required
    def get(self, user_id):
        return self.render('user.html')

