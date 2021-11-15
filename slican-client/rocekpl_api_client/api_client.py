# -*- coding:utf-8 -*-
"""
Project: rocekpl-api-client
File: /api_client.py
File Created: 2021-11-15, 12:13:27
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-11-15, 21:57:27
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import time
import requests

from .api_config import ApiConfig
from .signature import Signature


class ApiClient:

    def __init__(self) -> None:
        self.config = ApiConfig()
        self.timestamp = int(time.time())
        self.method = 'GET'
        self.endpoint = ''
        self.params = {}
        self.data = {}
        self.headers = {}


    def get_signature(self) -> str:
        signature = Signature()
        secret = self.config.api_key
        if self.method == 'GET' and len(self.params) > 0:
            params = self.params
        elif type(self.data) == dict and len(self.data) > 0:
            params = self.data
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


    def get_all(self) -> str:
        self.method = 'GET'
        self.endpoint = 'messagesQueue'
        self.params = {}
        self.data = {}
        self.headers = self.get_headers()

        heads = self.get_headers()
        response = requests.get(
            self.get_url(),
            headers=heads
        )

        return response.text
