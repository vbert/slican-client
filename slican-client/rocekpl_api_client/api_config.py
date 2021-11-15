# -*- coding:utf-8 -*-
"""
Project: rocekpl-api-client
File: /api_config.py
File Created: 2021-11-15, 12:32:31
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-11-15, 13:05:26
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os

class ApiConfig:

    def __init__(self) -> None:
        self.data_dir: str = os.getenv('DATA_DIR')
        self.messages_queue_file: str = os.getenv('MESSGAGES_QUEUE_FILE')
        self.api_key: str = os.getenv('API_KEY')
        self.hash_algorithm: str = os.getenv('HASH_ALGORITHM')
        self.base_url: str = os.getenv('BASE_URL')

    def get_all(self):
        return self
