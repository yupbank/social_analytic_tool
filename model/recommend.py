#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
recommend.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-12-01
'''
from __future__ import division
import _env
from user import User
from blog import Post

def post_by_user_id(user_id):
    return Post.where(user_id=user_id).col_list(col='id')

def recommend_top(user_id, recommend_list, top=5):
    user_post = post_by_user_id(user_id)
    _ = []
    for rate, post_id in recommend_list:
        if post_id not in user_post:
            _.append([rate, post_id])
    return _[:top]

def bind_post(top_list):
    ids = [i[1] for i in top_list]
    rate = [i[0] for i in top_list]
    posts = Post.get_list(id=ids)
    posts = zip(posts, rate)
    return posts

def recommend_tail(user_id, recommend_list, rate=0.8, top=5):
    user_post = post_by_user_id(user_id)
    _ = []
    total = len(recommend_list)
    user_rate = 0
    for num, (rate, post_id) in enumerate(recommend_list):
        if post_id in user_post:
            user_rate = user_rate + total - num
    print user_rate
    user_rate = user_rate/((total-1)*total/2)
    print user_rate, '!!user_date', total
    if user_rate < rate:
        user_rate = rate
    print int(total*user_rate)
    for rate, post_id in recommend_list[:int(total*rate)]:
        if post_id not in user_post:
            _.append([rate, post_id])
    return _[::-1][:top]

if __name__ == "__main__":
    pass
