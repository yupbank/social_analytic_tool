#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
index.py
Author: yupbank
Email:  yupbank@gmail.com

Created on
2012-11-02
'''
import _env
import tornado.web
import tornado.httpclient as httpclient
from tornado.auth import OAuth2Mixin
from base import BaseHandler
from model import UserAuth, User, gid
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
import binascii, uuid
import urllib
import json
import time
from model.blog import user_auth_new_blog 
from model.group import add_group

RESPONSE = 'code'

SCOPE = ['https://www.googleapis.com/auth/blogger','https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'] 
STATE = binascii.b2a_hex(uuid.uuid4().bytes)
ACCESS_TYPE = 'offline'

def tee(func):
    def _(*args, **kwargs):
        print args, kwargs
        print func
        s = func(*args, **kwargs)
        print s
        return s
    return _

class IndexHandler(BaseHandler):
    def get(self):
        return self.render('index.html')

class GoogleLoginHandler(BaseHandler):
    GOOGLE_AUTHORIZE_API = 'https://accounts.google.com/o/oauth2/auth?%s'
    GOOGLE_TOKEN = 'https://accounts.google.com/o/oauth2/token'
    As_http_client = httpclient.AsyncHTTPClient()
    def prepare(self):
        if self.current_user:
            return self.redirect('/')

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('code', None):
            self.get_authenticated_user(self.call_back)
            return
        self.get_auhenticate_code()
    
    def get_authenticated_user(self, call_back):
        code = self.get_argument('code')
        params = {
                'code': code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
                }
        self.As_http_client.fetch(self.GOOGLE_TOKEN, self.call_back, body=urllib.urlencode(params), method="POST")
    
    def call_back(self, response):
        auth = response.body
        auth = json.loads(auth)
        access_token = auth.get('access_token')
        info_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=%s'%access_token
        self.As_http_client.fetch(info_url, self.prase_user(auth))
        return

    def prase_user(self, auth):
        def _(response):
            user_info = response.body
            user_info = json.loads(user_info)
            google_id = user_info['id']
            ua = UserAuth.get_or_create(id=google_id)
            expire_time = auth.get('expires_in')+time.time()
            expire_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expire_time))
            ua.expire_time =expire_time 
            ua.access_token = auth.get('access_token')
            ua.token_type = auth.get('token_type')
            ua.id_token = auth.get('id_token')
            ua.refresh_token = auth.get('refresh_token')
            ua.save()
            u = User.get_or_create(id=google_id)
            if not u.email:
                u.emial = user_info.get('email')
                u.picture = user_info['picture']
                u.gender = user_info['gender']
                u.birthday = user_info.get('birthday')
                u.name = user_info['name']
                u.save()
            self.set_secure_cookie('S', google_id)
            try:
                user_auth_new_blog(ua)
            except Exception, e:
                print e, 'bad things happen for user:%s'%ua.id
            return self.redirect('/user/%s'%google_id)
        return _




    def get_auhenticate_code(self):
        params = {
                    'response_type': 'code',
                    'client_id': CLIENT_ID,
                    'redirect_uri': REDIRECT_URI,
                    'state': STATE,
                    'access_type': ACCESS_TYPE,
                    'approval_prompt': 'force',
                }
        params = urllib.urlencode(params)
        scope = '+'.join(map(urllib.quote, SCOPE))
        params = '%s&scope=%s'%(params, scope)
        return self.redirect(self.GOOGLE_AUTHORIZE_API%params)

