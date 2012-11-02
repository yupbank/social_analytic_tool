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

def main():
    for s in  User.where():
        s.delete()
    for s in  UserAuth.where():
        s.delete()

if __name__ == '__main__':
    main()
