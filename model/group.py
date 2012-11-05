#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
group.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-03
'''
import _env
from _db import Model
import time
from gid import gid
from cid import CID_MEMBER

class Group(Model):
    @classmethod
    def bind_info(cls, groups):
        for i in groups:
            i.group_info = GroupInfo.get(id=i.group_id)

def add_group(id, user_id, state=CID_MEMBER):
    g = Group.get_or_create(group_id=id, user_id=user_id)
    g.sate = state
    g.save()
    return g


class GroupInfo(Model):
    pass
    
def new_info(create_id, name, description):
    id = gid()
    gi = GroupInfo.get_or_create(id=id, create_id=create_id)
    gi.name = name
    gi.description = description
    gi.save()
    return gi
    



if __name__ == '__main__':
    pass
