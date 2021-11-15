# -*- coding:utf-8 -*-
"""
Project: rocekpl-api-client
File: /api_client.py
File Created: 2021-11-15, 12:13:27
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-11-15, 13:08:56
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import time
import requests

from .api_config import ApiConfig


class ApiClient:

    def __init__(self) -> None:
        self.config = ApiConfig()


    def get_base_url(self):
        return self.config.base_url
