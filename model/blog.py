#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
blog.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-05
'''
import _env
from _db import Model
import requests
from config import BROWSE_KEY
from user import User, UserAuth
BLOGGER_API = 'https://www.googleapis.com/blogger/v3/users/%s/blogs'
POSTS_API = 'https://www.googleapis.com/blogger/v3/blogs/%s/posts'
COMMENT_API = 'https://www.googleapis.com/blogger/v3/blogs/%s/posts/%s/comments'

class Blog(Model):
    pass

class Author(Model):
    pass

class Comment(Model):
    pass

class Post(Model):
    pass

def get_blog_info(google_id, token_type, access_token):
    blogger_api = BLOGGER_API%google_id
    s = requests.get(blogger_api, headers={'Authorization':'%s %s'%(token_type, access_token)})
    print s.content

def get_posts(blogger_id):
    post_api = POSTS_API%blogger_id
    s = requests.get('%s?key=%s'%(post_api, BROWSE_KEY))
    print s.content

def get_comment(blogger_id, post_id):
    comment_api = COMMENT_API%(blogger_id, post_id)
    s = requests.get('%s?key=%s'%(comment_api, BROWSE_KEY))
    print s.content

if __name__ == "__main__":
    for i in UserAuth.where():
        get_blog_info(i.id, i.token_type, i.access_token)

