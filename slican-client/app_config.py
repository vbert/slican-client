# -*- coding:utf-8 -*-
"""
Project: rocekpl-api-client
File: /api_config.py
File Created: 2021-11-15, 12:32:31
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-08-02, 11:18:26
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os

class AppConfig(object):
    __instance = None

    def getInstance():
        """ Static access method. """
        if AppConfig.__instance == None:
            AppConfig()
        return AppConfig.__instance


    def __init__(self) -> None:
        """ Virtually private constructor. """
        self.data_dir: str = os.getenv('DATA_DIR')
        self.messages_queue_file: str = os.getenv('MESSGAGES_QUEUE_FILE')
        self.phonedial_queue_file: str = os.getenv('PHONEDIAL_QUEUE_FILE')
        self.api_key: str = os.getenv('API_KEY')
        self.hash_algorithm: str = os.getenv('HASH_ALGORITHM')
        self.base_url: str = os.getenv('BASE_URL')
        self.slican_host: str = os.getenv('SLICAN_HOST')
        self.slican_port: int = os.getenv('SLICAN_PORT')
        self.access_key: int = os.getenv('ACCESS_KEY')
        self.internal_phone_number: int = os.getenv('INTERNAL_PHONE_NUMBER')
        self.pin_sim_card: int = os.getenv('PIN_SIM_CARD')
        self.sender_phone_number: str = os.getenv('SENDER_PHONE_NUMBER')
        self.system_user_id: str = os.getenv('SYSTEM_USER_ID')
        self.log_dir: str = os.getenv('LOG_DIR')
        if AppConfig.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            AppConfig.__instance = self
