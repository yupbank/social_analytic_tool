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

def reports_by_group_id(group_id):
    in_edge = []
    cache = {}
    for user_id in user_id_by_group_id(group_id):
        blog_id = Blog.get(user_id=user_id).id
        author_id = get_author_id_by_user_id(user_id)
        comments = Comment.where(author_id=author_id)
        counts = count_in (comments)
        if cache.get(user_id):
            user = cache.get(user_id)
        else:
            user = User.get(user_id)
            cache[user_id] = user
        user = User.get(user_id)
        for i, j in counts.iteritems():
            if user_id <> i:
                if i in cache:
                    target = cache[i]
                else:
                    target = User.get(i)
                    cache[i] = target

                edge = {'source': user_id,
                        'source_name': user.name,
                        'target': i,
                        'target_name': target.name,
                        'counts': j,
                        }
                in_edge.append(edge)
            else:
                print user_id, i
    return in_edge

def count_in(comments):
    res = {}
    for comment in comments:
        _a = get_user_id_by_blog_id(comment.blog_id)
        _t = None
        if comment.reply_to:
            _comment = Comment.get(comment.reply_to)
            _t = get_user_id_by_author_id(_comment.author_id)
        _t = _t or _a
        if _t:
            if _t in res:
                res[_t] += 1
            else:
                res[_t] = 1
    return res

if __name__ == '__main__':
    print reports_by_group_id('100021')
