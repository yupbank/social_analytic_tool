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
import time
import md5
from config import BROWSE_KEY
from user import User, UserAuth
from util import auth_key_json, authrize_json, get_json
BLOGGER_API = 'https://www.googleapis.com/blogger/v2/users/self/blogs'
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

def get_user_id_by_blog_id(blog_id):
    blog = Blog.get(id=blog_id)
    return blog.user_id

def get_author_id_by_blog_id(blog_id):
    return get_author_id_by_user_id(get_user_id_by_blog_id(blog_id))

def get_user_id_by_author_id(author_id):
    authors = Author.where(id = author_id)
    for author in authors:
        if author.user_id:
            return author.user_id

def get_author_id_by_user_id(user_id):
    author = Author.get(user_id=user_id)
    if author:
        return author.id

def new_blog(blog_id, user_id, name, description, updated, published, link, total_post):
    blog = Blog.get(id=blog_id, updated=simplify_google_time(updated))
    if not blog:
        print 'new_blog'
        blog = Blog.get_or_create(id=blog_id)
        blog.user_id = user_id
        blog.name = name
        blog.description = description
        blog.updated = simplify_google_time(updated)
        blog.published = simplify_google_time(published)
        blog.link = link
        blog.total_post = total_post
        blog.save()
    return blog

def new_post(post_id, blog_id, user_id, published, updated, link, title, content, reply_num, author_id):
    post = Post.get(id=post_id, updated=simplify_google_time(updated))
    if not post:
        print 'new_post'
        post = Post(id=post_id)
        post.blog_id = blog_id
        post.user_id = user_id
        post.published = simplify_google_time(published)
        post.updated = simplify_google_time(updated)
        post.link = link
        post.title = title
        post.content = content
        post.reply_num = reply_num
        post.author_id = author_id
        post.save()
    return post

def get_comment_by_user_id(user_id):
    _ = []
    _.extend(get_blog_comment_by_user_id(user_id) or [])
    _.extend(get_reply_comment_by_user_id(user_id) or [])
    return _

def get_blog_comment_by_user_id(user_id):
    blog_ids = Blog.where(user_id=user_id).col_list(col='id')
    if blog_ids:
        comment = Comment.get_list(blog_id=blog_ids).where('reply_to is null')
        return comment

def get_reply_comment_by_user_id(user_id):
    author = Author.get(user_id=user_id)
    if author:
        comment = Comment.where(reply_to=author.id)
        return comment

def new_comment(comment_id, post_id, blog_id, published, updated, content, author_id, reply_to=None):
    comment = Comment.get(id=comment_id, updated=simplify_google_time(updated))
    if not comment:
        print 'new_comment'
        comment = Comment(id=comment_id)
        comment.post_id = post_id
        comment.blog_id = blog_id
        comment.published = simplify_google_time(published)
        comment.updated = simplify_google_time(updated)
        comment.content = content
        comment.author_id = author_id
        comment.reply_to = reply_to
        comment.save()
    return comment

def new_author(author_id, name, link, picture, user_id=None):
    if not user_id:
        author = Author.get(id=author_id)
    else:
        author = Author.get(id=author_id, user_id=user_id)
    if not author:
        print 'new_author'
        author = Author.get_or_create(id=author_id)
        author.user_id = user_id
        author.name = name
        author.link = link
        author.picture = picture
        author.save()
    return author

def get_blogs(google_id, token_type, access_token):
    blogger_api = BLOGGER_API
    return authrize_json(blogger_api, access_token, token_type)

def get_posts(blogger_id, **kwargs):
    print 'call:%s'%blogger_id, '!!!'
    post_api = POSTS_API%blogger_id
    return auth_key_json(post_api, **kwargs)

def get_comments(blogger_id, post_id, **kwargs):
    comment_api = COMMENT_API%(blogger_id, post_id)
    return auth_key_json(comment_api, **kwargs)

def user_auth_new_blog(user_auth):
    access_token = user_auth.get_access_token()
    blog_info = get_blogs(user_auth.id, user_auth.token_type, access_token)
    print blog_info, '!!!'
    for item in blog_info.get('items', []):
        user_id = user_auth.id
        blog_id = item.get('id')
        name = item.get('name')
        description = item.get('description')
        updated = item.get('updated')
        published = item.get('published')
        link = item.get('url')
        total_post = item.get('posts', {}).get('totalItems')
        return new_blog(blog_id, user_id, name, description, updated, published, link, total_post)

def simplify_google_time(google_time):
    _ = google_time

    try:
        time.strptime(_, '%Y-%m-%d %H:%M:%S')
    except Exception,e:
        _.replace('T', ' ')
        _ = _[:-6]
    return _

#def blog_pulic_post_count(blog_id):
#    post_link = POSTS_API%blog_id
#    print post_link
#    posts = get_json(post_link)
#    print posts


def update_posts_by_blog(blog):
    posts_info = get_posts(blog.id)
    posts = posts_info.get('items', [])
    for post in posts:
        post_id = post.get('id')
        published = post.get('published')
        updated = post.get('published')
        link = post.get('url')
        title = post.get('title')
        content = post.get('content')
        reply_num = post.get('replies', {}).get('totalItems')
        author = post.get('author', {})
        author_id = author.get('id')
        author_name = author.get('displayName')
        author_link = author.get('url')
        author_picture = author.get('image',{}).get('url')
        user_id = blog.user_id
        new_post(post_id, blog.id, user_id, published, updated, link, title, content, reply_num, author_id)
        new_author(author_id, author_name, author_link, author_picture, user_id)

def update_comments_by_post(post):
    comments_info = get_comments(post.blog_id, post.id) or {}
    comments = comments_info.get('items', [])
    for comment in comments:
        comment_id = comment.get('id')
        post_id = post.id
        blog_id = post.blog_id
        published = comment.get('published')
        updated = comment.get('updated')
        content = comment.get('content')
        reply_to = comment.get('inReplyTo', {}).get('id')
        author = comment.get('author')
        author_id = author.get('id')
        author_name = author.get('displayName')
        author_link = author.get('url')
        author_picture = author.get('image',{}).get('url')
        new_comment(comment_id, post_id, blog_id, published, updated, content, author_id, reply_to)
        new_author(author_id, author_name, author_link, author_picture)
            


def update_blogs():
    for i in UserAuth.where():
        user_auth_new_blog(i)

def update_posts():
    for blog in Blog.where():
        update_posts_by_blog(blog)

def update_commets():
    for post in Post.where():
        update_comments_by_post(post)

if __name__ == "__main__":
    for i in User.where():
        print get_comment_by_user_id(i.id)
        


