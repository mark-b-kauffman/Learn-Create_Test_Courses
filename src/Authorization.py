# Credit to jgregoriJavier Gregori who published Bb_rest_helper under the Blackboard Open Source License 
# https://github.com/jgregori/Bb_rest_helper
# LICENSE: https://github.com/jgregori/Bb_rest_helper/blob/master/LICENSE.md shown below.
# We've taken the Auth_Helper() class and created this Authorization class with a few modifications,
# primarly removing the logging. We use this to cache our access token and then refresh it when it expires 
# should that be needed.
"""
Copyright (C) 2020, Blackboard Inc. All rights reserved. Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

-- Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

-- Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

-- Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import datetime
import json
import logging
import os
import sys
import time
import requests
from requests import HTTPError

class Authorization():

    # Initializes the auth helper by taking the target system url,
    # PI key and secret as arguments.
    def __init__(self, url: str, key: str, secret: str):
        self.url = url
        self.key = key
        self.secret = secret
        self.learn_token = None

    # Method that returns True when the token expires. Used by the learn_auth() method.
    def token_is_expired(self, expiration_datetime):
        self.expiration_datetime = expiration_datetime
        self.time_left = (self.expiration_datetime -
                          datetime.datetime.now()).total_seconds()
        if self.time_left < 1:
            time.sleep(1)
            return True
        else:
            return False

    # Returns the authentication token for Blackboard Learn.
    def learn_auth(self):
        self.endpoint = "/learn/api/public/v1/oauth2/token"
        self.params = {"grant_type": "client_credentials"}
        self.headers = {
            'Content-Type': "application/x-www-form-urlencoded"}

        try:
            if self.learn_token == None:

                r = requests.request(
                    "POST",
                    self.url +
                    self.endpoint,
                    headers=self.headers,
                    params=self.params,
                    auth=(
                        self.key,
                        self.secret))
                r.raise_for_status()
                self.data = json.loads(r.text)
                self.learn_token = self.data["access_token"]
                self.expires = self.data["expires_in"]
                m, s = divmod(self.expires, 60)
                self.now = datetime.datetime.now()
                self.expires_at = self.now + \
                    datetime.timedelta(seconds=s, minutes=m)
                print(f"Learn Authentication successful")
                print("Token expires at: " + str(self.expires_at))
                return self.learn_token

            elif self.token_is_expired(self.expires_at):
                print(f'Token expired, refreshing token.')
                r = requests.request(
                    "POST",
                    self.url +
                    self.endpoint,
                    headers=self.headers,
                    params=self.params,
                    auth=(
                        self.key,
                        self.secret))
                r.raise_for_status()
                self.data = json.loads(r.text)
                self.learn_token = self.data["access_token"]
                self.expires = self.data["expires_in"]
                m, s = divmod(self.expires, 60)
                self.now = datetime.datetime.now()
                self.expires_at = self.now + \
                    datetime.timedelta(seconds=s, minutes=m)
                print("Learn Authentication successful")
                print("Token expires at: " + str(self.expires_at))
                return self.learn_token
            else:
                return self.learn_token

        except requests.exceptions.HTTPError as e:
            data = json.loads(r.text)
            print(data["error_description"])


