#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
_env.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-02
'''
from os.path import abspath, dirname, normpath
import sys

#find the python path
PREFIX = normpath(dirname(dirname(abspath(__file__))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path
