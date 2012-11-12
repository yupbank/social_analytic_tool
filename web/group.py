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
from base import LoginHandler, BaseHandler
from tornado.web import HTTPError
from model import Group, GroupInfo, User, Blog
from model.group import new_info, add_group
from model.cid import CID_CREATE
from model.report import reports_by_group_id
import time
import json

class GroupHandler(BaseHandler):
    def get(self, id):
        gi = GroupInfo.get(id=id)
        if not gi:
            raise HTTPError(404)
        group_name = gi.name
        creater = User.get(gi.create_id)
        description = gi.description
        groups = Group.where(group_id=id)
        user_ids = groups.col_list(col='user_id')
        users = User.get_list(user_ids)
        blogs = Blog.where('user_id in (%s)'%','.join(user_ids))
        return self.render('group.html', gi=gi, creater=creater, groups=groups, users=users, blogs=blogs)

class ReportHandler(BaseHandler):
    def get(self):
        id = self.get_argument('id')
        reports = reports_by_group_id(id)
        data = json.dumps(reports)
        self.finish(data)


class AddGroupHandler(LoginHandler):
    def get(self, id):
        g = Group.get(group_id=id)
        if not g:
            raise HTTPError(404)
        add_group(id, self.current_user.id)
        uri = self.request.path 
        print uri
        return self.redirect('/group/%s'%id)

class NewGroupHandler(LoginHandler):
    def get(self):
        return self.render('new_group.html', error={})
    
    def post(self):
        error = {}
        group_name = self.get_argument('group_name', None)
        group_description = self.get_argument('group_description', None)
        if not group_name:
            error['group_name'] = 'U have to input the name'
        if not group_description:
            error['group_description'] = 'the group must have to be declared'
        if error:
            return self.render('new_group.html', error=error, group_name=group_name, group_description=group_description)
        create_id = self.current_user.id
        gi = new_info(create_id, group_name, group_description)
        g = add_group(gi.id, create_id, CID_CREATE)
        return self.redirect('/group/%s'%g.group_id)

class GroupList(BaseHandler):
    def get(self, limit=0):
        offset = 20
        limit = int(limit)
        groups = GroupInfo.where()
        groups = groups[limit:limit+offset]
        return self.render('groups.html', groups=groups)

