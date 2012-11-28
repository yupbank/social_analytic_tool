#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
add_group.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-28
'''
import _env
from model.user import User
from model.group import Group, add_group

if __name__ == '__main__':
    except_id = '118270245423604986734'
    for i in  User.where():
        if not i.id == except_id:
            group = Group.where(user_id=i.id)
            if not group:
                add_group(i.id)
