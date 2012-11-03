#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
crawl_blog.py
Author: yupbank                                                                   
Email:  yupbank@gmail.com

Created on                                                                        
2012-11-03 
"""
import _env
from model import User, UserAuth
BLOGGER_INFO = 'https://www.googleapis.com/blogger/v3/users/%s/blogs?access_token=%s'
import requests

def main():
    for user in User.where():
        user_id = user.id
        print user.name.encode('U8')
        ua = UserAuth.get(id=user.id)
        access_token = ua.access_token
        s = requests.get(BLOGGER_INFO%(user_id, access_token))
        print s.content


if __name__ == '__main__':
    main()
