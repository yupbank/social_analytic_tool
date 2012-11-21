#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
post.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-21
'''
import _env
from base import LoginHandler, BaseHandler
from model import Post as P, User

class Post(BaseHandler):
    def get(self, id):
        p = P.get(id)
        if p:
            user = User.get(p.user_id)
            return self.render('post.html', post=p, user=user)
