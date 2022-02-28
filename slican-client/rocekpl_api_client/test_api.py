# -*- coding:utf-8 -*-
"""
Project: rocekpl_api_client
File: /test_api.py
File Created: 2022-02-28, 10:24:00
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-02-28, 10:47:11
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 - 2022 by vbert
"""
import re
import time
import json
import requests

from signature import Signature


def get_signature(timestamp) -> str:
    signature = Signature()
    api_key = 'X1921QZ!K3L8BS0Y'
    secret = api_key
    params = {
        'id': 1
    }
    return signature.create(timestamp, secret, params)


def main():
    timestamp = int(time.time())
    header = {
        'Timestamp': timestamp,
        'Signature': get_signature(timestamp)
    }
    print(header)


if __name__ == '__main__':
    main()