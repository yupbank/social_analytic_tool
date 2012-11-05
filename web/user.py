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
from model import Group

class UserHandler(BaseHandler):
    @login_required
    def get(self, user_id):
        my_group = Group.where(user_id=self.current_user.id)
        Group.bind_info(my_group)
        return self.render('user.html', my_groups=my_group)

