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
from base import BaseHandler, login_required, LoginHandler
from model import Group, Blog, User, Post
from model.blog import get_comment_by_user_id, get_user_id_by_author_id
from collections import defaultdict
import json
from misc.tofromfile import fromfile
import os


class UserHandler(BaseHandler):
    #@login_required
    def get(self, user_id):
        recommend = []
        try:
            t = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            t = fromfile('%s/misc/recommend'%t)
            recommend = t.get(user_id)
            if recommend:
                _ = []
                for i in recommend:
                    p = Post.get(i[1])
                    _.append(p)
                recommend = _
                
        except Exception, e:
            print e
        
        my_group = Group.where(user_id=user_id)
        Group.bind_info(my_group)
        my_blog = Blog.where(user_id=user_id)
        comments = get_comment_by_user_id(user_id)
        data = self.build_data(comments)
        user = User.get(user_id)
        return self.render('user.html', user=user, my_groups=my_group, my_blogs=my_blog, data=data, recommend=recommend)
    
    def build_data(self, comments, all=True):
        author = defaultdict(list)
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

class UserList(LoginHandler):
    def get(self):
        if self.current_user.id == '112100305315359676269':
            users = User.where()
            return self.render('user_list.html', users=users)
        else:
            self.redirect('/user/%s'%self.current_user.id)

if __name__ == "__main__":
    print os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '!!!'
