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
from model.blog import get_comment_by_user_id, get_user_id_by_author_id
from collections import defaultdict
import json

class UserHandler(BaseHandler):
    @login_required
    def get(self, user_id):
        my_group = Group.where(user_id=user_id)
        Group.bind_info(my_group)
        my_blog = Blog.where(user_id=user_id)
        comments = get_comment_by_user_id(user_id)
        data = self.build_data(comments)
        return self.render('user.html', my_groups=my_group, my_blogs=my_blog, data=data)
    
    def build_data(self, comments, all=True):
        autor = defaultdict(list)
        for i in comments:
            if i.author_id in author:
                author[i.author_id].append(i.id)
            else:
                author[i.author_id] = [i.id]
        data = []
        for i,j in author.items():
            _ = {}
            _["author_id"] = i
            _["comment_ids"] = j
            _["user_id"] = get_user_id_by_author_id(i)
            _["comment_counts"] = len(j)
            data.append(_)
        print data, '!!!!!!!!!!!!!'
        return json.dumps(data)
