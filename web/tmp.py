#!/usr/bin/env python
# -*- coding: utf-8 -*-
from djangomako.shortcuts import render_to_response, render_to_string
from django.shortcuts import redirect
import requests
import binascii, uuid
import urllib
import json
#from models import UserAuth
import time

RESPONSE = 'code'
GOOGLE_AUTHORIZE_API = 'https://accounts.google.com/o/oauth2/auth?%s'
GOOGLE_TOKEN = 'https://accounts.google.com/o/oauth2/token'
CLIENT_ID = '727469625538.apps.googleusercontent.com'
CLIENT_SECRET = 'DT97zk6SlgDSwjODibHmO5nK'
REDIRECT_URI = 'http://social-blogger.tk/google_login'

SCOPE = ['https://www.googleapis.com/auth/blogger','https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'] 
STATE = binascii.b2a_hex(uuid.uuid4().bytes)
ACCESS_TYPE = 'offline'


def login_required(func):
    def _(request, *args, **kwargs):
        cookie = request.COOKIES.get('s', None)
        if not cookie:
            return redirect('/')
        else:
            return func(request, *args, **kwargs)
    return _

def index_view(request):
    return render_to_response('index.html', {'user':request.user})


def google_login(request):
    code = request.GET.get('code')
    if not code:
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
        return redirect(GOOGLE_AUTHORIZE_API%params)
    else:
        params = {
                'code': code,
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': REDIRECT_URI,
                'grant_type': 'authorization_code',
                }
        t = requests.post(GOOGLE_TOKEN, params)
        res = json.loads(t.content)
        access_token = res.get('access_token')
        token_type = res.get('token_type')
        id_token = res.get('id_token')
        expires_time = time.time()+res.get('expires_in')
        user_info = requests.get('https://www.googleapis.com/auth/userinfo.email?access_token=%s'%access_token)
        user_info = json.loads(user_info.content)
        user_id = user_info.get('id')
        #ua = UserAuth.objects.filter(user_id=user_id)
        #if ua:
        #    ua = ua[0]
        #else:
        #    ua = UserAuth(user_id=user_id)
        #    ua.user_mail = user_info.get('email')
        #    ua.access_token = access_token
        #    ua.token_type = token_type
        #    ua.id_token = id_token
        #    ua.expires_time = expires_time
        #    ua.save()
        #ui = UserInfo.objects.filter(user_id=user_id)
        #if ui:
        #    ui = ui[0]
        #else:
        #    ui = UserInfo(user_id=user_id)
        #    ui.user_name = user_indo.get('name')
        #    ui.user_birth = user.get('birthday').replace('-', '')
        #    ui.user_gender = user.get('gender')
        #    ui.user_link = user.get('link')
        #    ui.user_picture = user.get('picture')
        #    ui.save()

        response = render_to_response('success.html', {'code': 'welcome here %s'%user_link, 't': user_name})
        response.set_cookie("S", user_id)
        return response
