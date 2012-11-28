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
from model.blog import update_blogs, update_posts, update_commets

def main():
    print 'sync blogs!!'
    update_blogs()
    #print 'sync posts!!'
    #update_posts()
    #print 'sync comments!!'
    #update_commets()



if __name__ == '__main__':
    main()
