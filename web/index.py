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
        self.As_http_client.fetch(self.GOOGLE_TOKEN, call_back, body=urllib.urlencode(params), method="POST")
    
    def call_back(self, response):
        res = response.body
        res = json.loads(res)
        access_token = res.get('access_token')
        url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json&access_token=%s'%access_token
        res = httpclient.HTTPClient().fetch(url)
        res = res.body
        res = json.loads(res)
        print res
        google_id = res['id']
        token_type = res.get('token_type')
        id_token = res.get('id_token')
        expires_time = time.time()+res.get('expires_in')
        ua = UserAuth.get_or_create(id_token=id_token)
        ua.expires_time = expires_time
        ua.token_type = token_type
        ua.refresh_token = res.get('refresh_token')
        ua.access_token = access_token
        if not ua.id:
            _id = gid()
            ua.id = _id
            u = User()
            u.id = ua.id
            u.email = res['email']
            u.google_id = google_id
            u.picture = res['picture']
            u.gender = res['gender']
            u.birthday = res.get('birthday')
            u.name = res['name']
            u.save()
        self.set_secure_cookie('S', str(ua.id))
        ua.save()
        return self.redirect('/user/%s'%ua.id)




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

