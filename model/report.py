#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
report.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-12
'''
from group import user_id_by_group_id
from blog import get_author_id_by_user_id, Blog, Comment, get_user_id_by_author_id, get_user_id_by_blog_id, get_author_id_by_blog_id
from user import User
from collections import defaultdict

CACHE = {}

def get_user(user_id):
    if CACHE.get(user_id):
        user = CACHE.get(user_id)
    else:
        user = User.get(user_id)
        CACHE[user_id] = user
    return user

def reports_by_group_id(group_id):
    edges = []
    nodes = []
    index = {}
    _in = defaultdict(int)
    _out = defaultdict(int)
    ids =  user_id_by_group_id(group_id)
    for n,i in enumerate(ids):
        index[i] = n
    for user_id in ids:
        user = get_user(user_id)
        if Blog.get(user_id=user_id):
            blog_id = Blog.get(user_id=user_id).id
            author_id = get_author_id_by_user_id(user_id)
            comments = Comment.where(author_id=author_id)
            counts = count_in (comments, user_id, _in, _out)
            for i, j in counts.iteritems():
                target = get_user(i)
                edge = {'source': index[user_id],
                        'target': index[i],
                        'value': j,
                        }
                edges.append(edge)

    nodes = [
            {   'name': get_user(i).name,
                'in': _in[i],
                'out': _out[i],
                'weight': _in[i]+_out[i],
                'index': n,
                'id':i,
                 }
            for n,i in enumerate(ids)
            ] 
    return {'nodes': nodes, 'links': edges}

def count_in(comments, user_id, _in, _out):
    res = {}
    for comment in comments:
        _a = get_user_id_by_blog_id(comment.blog_id)
        _t = None
        if comment.reply_to:
            _comment = Comment.get(comment.reply_to)
            _t = get_user_id_by_author_id(_comment.author_id)
        _t = _t or _a
        if _t and _t <> user_id:
            _out[user_id] += 1
            _in[_t] += 1
            if _t in res:
                res[_t] += 1
            else:
                res[_t] = 1
    return res

if __name__ == '__main__':
    print reports_by_group_id('100021')
