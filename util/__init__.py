#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
__init__.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''
def lower_name(class_name):
    """
    >>>lower_name("UserCount")
    'user_count'

    >>>lower_name("user_count")
    'user_count'
    """
    result = []
    for c in class_name:
        i = ord(c)
        if 65 <= i <= 90:
            if result:
                if not 48 <= ord(result[-1]) <= 57:
                    result.append('_')
            i += 32
            c = chr(i)
        result.append(c)
    return ''.join(result)

