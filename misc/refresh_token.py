#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
refresh_token.py
Author: yupbank                                                                   
Email:  yupbank@gmail.com

Created on                                                                        
2012-11-03 
"""
import _env
import requests
import urllib
from model import UserAuth
from config import CLIENT_ID, CLIENT_SECRET

REFRESH_API = 'https://www.googleapis.com/o/oauth2/token'
GRANT_TYPE = 'refresh_token'

def main():
    for ua in UserAuth.where():
        print ua.id, ua.expire_time
        data = dict(
                client_id = CLIENT_ID,
                client_secret = CLIENT_SECRET,
                refresh_token = ua.refresh_token,
                grant_type = GRANT_TYPE,
                )
        data = urllib.urlencode(data)
        t = requests.post(REFRESH_API, data)
        print t.content



if __name__ == '__main__':
    main()
