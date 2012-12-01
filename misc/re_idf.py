#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
re_idf.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-26
'''
import _env
from model.group import Group
from model.blog import Post, get_author_id_by_user_id, Comment, get_comment_by_user_id
import numpy as np
from idf import idf

def posts_by_users(users):
    for user in users:
        for post in Post.where(user_id=user):
            yield post

def comment_by_users(users):
    for post in posts_by_users(users):
        for comment in Comment.where(post_id=post.id):
            yield comment

def comment_by_group_user(group_id, user_id):
    author_id = get_author_id_by_user_id(user_id)
    users = get_user_by_group(group_id)
    comments = []
    for user in users:
        for post in Post.where(user_id=user):
            for comment in Comment.where(post_id=post.id):
                if comment.author_id == author_id:
                    comments.append(comment)
    return comments

def get_user_by_group(group_id):
    group = Group.get(group_id=group_id)
    return group.users

def get_group_similar_post_comment(group_id):
    users = get_user_by_group(group_id)
    return user_comment_smilar(users)

        

def user_post_similar(users):
    post_ids = []
    for post in posts_by_users(users):
        post_ids.append(post.id)
        idf.append(post.id, post.content.encode('U8'))
    length = len(post_ids)
    similar = np.zeros(length**2, np.float)
    similar = similar.reshape(length, length)
    
    cache = {}
    for numi, i in enumerate(post_ids):
        for numj, j in enumerate(post_ids):
            key = '%s-%s'%(i, j)
            if key not in cache and '%s-%s'%(j, i) not in cache:
                cache[key] = idf.similar(i, j)
            else: 
                key = '%s-%s'%(j, i)
            similar[numi][numj] = cache[key]
    return post_ids, similar

def user_comment_smilar(users):
    authors = []
    for user in users:
        author = get_author_id_by_user_id(user)
        if author:
            authors.append(author)

    comments = []
    post_ids, similar = user_post_similar(users)
    for comment in comment_by_users(users):
        comments.append([comment.id, comment.content.encode('U8')])

    length = len(comments)
    comment_rela = np.zeros(length*len(post_ids), np.float)
    comment_rela = comment_rela.reshape(length, len(post_ids))
    
    for num, (i, j) in enumerate(comments):
        idf.append(i, j)
        for x, p in enumerate(post_ids):
            comment_rela[num][x] = idf.similar(i, p)
    return post_ids, similar, [i[0] for i in comments], comment_rela

def main():
    value = {}
    users = get_user_by_group(100022)
    posts, post_relation, comments, comment_relation = user_comment_smilar(users)
    print len(users), users
    for user in users:
        user_comments = comment_by_group_user(100022, user)
        user_comment = np.zeros(len(posts), np.float)
        user_comment_length = len(user_comments)
        for comment in user_comments:
            comment_index = comments.index(comment.id)
            user_comment += comment_relation[comment_index]
        user_comment = np.dot(user_comment, post_relation)
        if user_comment_length:
            user_comment = user_comment/user_comment_length
        user_comment = zip(user_comment, posts)
        user_comment.sort(key=lambda x:x[0], reverse=True)
        value[user] = user_comment
    
    print 'to_file!!', value
    from tofromfile import tofile
    tofile('recommend', value)

def cut():
    value = {}
    users = get_user_by_group(100022)
    posts, post_relation, comments, comment_relation = user_comment_smilar(users)
    for user in users:
        user_comments = comment_by_group_user(100022, user)
        user_comment = np.zeros(len(posts), np.float)
        user_comment_length = len(user_comments)
        for comment in user_comments:
            comment_index = comments.index(comment.id)
            user_comment += comment_relation[comment_index]
        user_comment = np.dot(user_comment, post_relation)
        if user_comment_length:
            user_comment = user_comment/user_comment_length
        user_comment = zip(user_comment, posts)
        user_comment.sort(key=lambda x:x[0], reverse=True)
        _ = []
        res = []
        for p in posts_by_users([user]):
            _.append(p.id)
        print _
        for i in user_comment:
            print i[0], '!!'
            if i[0] not in _:
                res.append(i)
        print res
        length = int(len(res)*0.2)
        res = res[:length][::-1]
        value[user] = res 
    from tofromfile import tofile
    tofile('re_recommend', value)
    


if __name__ == '__main__':
    main()
