#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import _env
import os
from collections import defaultdict
from math import log, sqrt
from os.path import join
#from tofromfile import tofile, fromfile
from nltk import word_tokenize
from model.blog import Post, Comment, get_comment_by_user_id
from model.user import User
import copy
import numpy as np

class Idf(object):
    def __init__(self):
        self._idf = defaultdict(int)
        self._count = 0
        self.tf = []
        self.__idf = None

    def append(self, id, txt):
        count = 0
        tf = defaultdict(int)
        for i in word_tokenize(str(txt.lower())):
            tf[i] += 1
            count += 1
        for t in tf:
            tf[t] = tf[t]/count
            self._idf[t] += 1
        self._count += 1
        self.tf.append([id, tf])
    

    def idf(self):
        res = {}
        for i in self._idf:
            res[i] = log(self._count/self._idf[i], 2)
        return res

    def similar(self, i, j):
        if not self.tf:
            raise 
        idf = self.idf()
        res = 0
        ti = 0 
        tj = 0
        _tfi = [ y for x,y in self.tf if x == i][0]
        _tfj = [ y for x,y in self.tf if x == j][0]
        _k = copy.deepcopy(_tfi)
        _m = copy.deepcopy(_tfj)
        for _ in _k:
            _k[_] = _tfi[_]*idf[_]
        for _ in _m:
            _m[_] = _tfj[_]*idf[_]
        return self.cos(_k, _m)
    
    def cos(self, i, j):
        s = set()
        for _ in i:
            s.add(_)
        for _ in j:
            s.add(_)
        _i = 0
        _j = 0
        res = 0
        for k in s:
            if k in i:
                _i += i[k]**2
            if k in j:
                _j += j[k]**2
            if k in i and k in j:
                res += i[k]*j[k]
        return res/sqrt(_i*_j)

idf = Idf()

def get_similar_post_comment():
    for post in Post.where():
        idf.append(post.id, post.content)
    post_ids = Post.where().col_list(col='id')
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


    comments = Comment.where().order_by('updated').col_list(col='id,content')
    com_length = len(comments)
    comment_rela = np.zeros(com_length*length, np.float)
    comment_rela = comment_rela.reshape(com_length, length)
    for num, (i, j) in enumerate(comments):
        idf.append(i, j.encode('U8'))
        for x, p in enumerate(post_ids):
            comment_rela[num][x] = idf.similar(i, p)
    return post_ids, similar, [i[0] for i in comments], comment_rela


        
if __name__ == '__main__':
    posts, post_relation, comments, comment_relation = get_similar_post_comment()
    print posts, post_relation

    print comments, comment_relation
    for user in User.where():
        print user.name.encode('U8')
        cs = get_comment_by_user_id(user.id)
        _ = np.zeros(len(posts), np.float)
        for c in cs:
            c_index = comments.index(c.id)
            _ += comment_relation[c_index]
        _ = np.dot(_, post_relation)
        print _
        
    



