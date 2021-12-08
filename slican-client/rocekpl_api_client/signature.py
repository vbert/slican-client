# -*- coding:utf-8 -*-
"""
Project: rocekpl_api_client
File: /signature.py
File Created: 2021-11-15, 14:04:28
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-06, 13:48:31
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import hashlib
import urllib.parse
from typing import Any


class Signature(object):

    def __init__(self) -> None:
        pass


    def create(self, timestamp: int, secret: str, params: Any) -> str:
        separator = '&'
        temp = []
        temp.append(secret)
        if params is not None:
            if isinstance(params, dict):
                temp.append(urllib.parse.urlencode(params))
                # for key, value in sorted(params.items()):
                #     temp.append(f'{key}={value}')
            else:
                temp.append(params)
        temp.append(timestamp)
        hash = hashlib.sha512(bytes(separator.join([str(elem) for elem in temp]), 'utf-8'))
        return hash.hexdigest()
