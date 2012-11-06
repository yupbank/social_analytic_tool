#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
rm.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''
import _env
from user import User, UserAuth
from blog import Blog, Comment, Post, Author
from group import Group, GroupInfo

def delete(cls):
    for s in cls.where():
        s.delete()
def main():
    for i in [User, UserAuth, Blog, Comment, Post, GroupInfo, Group, Author]:
        delete(i)


if __name__ == '__main__':
    main()
