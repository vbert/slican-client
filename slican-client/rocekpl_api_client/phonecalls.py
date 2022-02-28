# -*- coding:utf-8 -*-
"""
Project: rocekpl_api_client
File: /phonecalls.py
File Created: 2022-02-28, 13:04:13
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-02-28, 13:07:41
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 - 2022 by vbert
"""
from .api_client import ApiClient


class PhoneCalls(ApiClient):

    def __init__(self, config) -> None:
        super().__init__(config)


    def list(self) -> str:
        self.endpoint = 'apiPhoneCalls'
        self.params = {}
        self.payload = {}
        return super().get()


    def get(self, id: int) -> str:
        self.endpoint = 'apiPhoneCalls'
        self.params = {'id': id}
        self.payload = {}
        return super().get()


    def create(self, payload: dict) -> str:
        self.endpoint = 'apiPhoneCalls/create'
        self.params = {}
        self.payload = payload
        return super().create()


    def update(self, id: int, payload: dict) -> str:
        self.endpoint = 'apiPhoneCalls/update'
        self.params = {'id': id}
        self.payload = payload
        return super().update()


    def delete(self, id: int) -> str:
        self.endpoint = 'apiPhoneCalls/delete'
        self.params = {'id': id}
        self.payload = {}
        return super().delete()
