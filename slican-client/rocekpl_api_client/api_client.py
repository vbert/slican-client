# -*- coding:utf-8 -*-
"""
Project: rocekpl-api-client
File: /api_client.py
File Created: 2021-11-15, 12:13:27
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-09, 23:21:25
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import re
import time
import json
import requests

from .signature import Signature


class ApiClient(object):

    def __init__(self, config) -> None:
        self.config = config
        self.timestamp = int(time.time())
        self.method = 'GET'
        self.endpoint = ''
        self.params = {}
        self.payload = {}
        self.headers = {}


    def get_signature(self) -> str:
        signature = Signature()
        secret = self.config.api_key
        if self.method == 'GET' and len(self.params) > 0:
            params = self.params
        elif type(self.payload) == dict and len(self.payload) > 0:
            params = self.payload
        else:
            params = ''
        return signature.create(self.timestamp, secret, params)


    def get_headers(self) -> dict:
        return {
            'Timestamp': str(self.timestamp),
            'Signature': self.get_signature()
        }


    def get_url(self) -> str:
        url = [self.config.base_url, self.endpoint]
        if len(self.params) > 0:
            for val in self.params.values():
                url.append(val)
        return '/'.join([str(elem) for elem in url])


    def response_re(self, text: str) -> str:
        pattern = '\{(.*}?)\}'
        finded = re.findall(pattern, text)
        res = finded[0]
        return "{%s}" % res


    def get(self) -> str:
        self.method = 'GET'
        response = requests.get(
            self.get_url(),
            headers=self.get_headers()
        )
        return json.loads(self.response_re(response.text))


    def create(self) -> str:
        self.method = 'POST'
        response = requests.post(
            self.get_url(),
            headers=self.get_headers(),
            data=self.payload
        )
        return json.loads(self.response_re(response.text))


    def update(self) -> str:
        self.method = 'PUT'
        response = requests.put(
            self.get_url(),
            headers=self.get_headers(),
            data=self.payload
        )
        return json.loads(self.response_re(response.text))


    def delete(self) -> str:
        self.method = 'DELETE'
        response = requests.delete(
            self.get_url(),
            headers=self.get_headers()
        )
        return json.loads(self.response_re(response.text))
