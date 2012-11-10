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
from model import Group, Blog

class UserHandler(BaseHandler):
    @login_required
    def get(self, user_id):
        my_group = Group.where(user_id=user_id)
        Group.bind_info(my_group)
        my_blog = Blog.where(user_id=user_id)
        return self.render('user.html', my_groups=my_group, my_blogs=my_blog)

