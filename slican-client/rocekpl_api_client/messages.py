# -*- coding:utf-8 -*-
"""
Project: rocekpl_api_client
File: /messages.py
File Created: 2021-11-22, 15:55:44
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-05, 23:50:17
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
from .api_client import ApiClient


class Messages(ApiClient):

    def __init__(self, config) -> None:
        super().__init__(config)


    def list(self) -> str:
        self.endpoint = 'apiMessages'
        self.params = {}
        self.payload = {}
        return super().get()


    def get(self, id: int) -> str:
        self.endpoint = 'apiMessages'
        self.params = {'id': id}
        self.payload = {}
        return super().get()


    def create(self, payload: dict) -> str:
        self.endpoint = 'apiMessages/create'
        self.params = {'id': payload['id']}
        self.payload = payload
        return super().create()


    def update(self, id: int, payload: dict) -> str:
        self.endpoint = 'apiMessages/update'
        self.params = {'id': id}
        self.payload = payload
        return super().update()


    def delete(self, id: int) -> str:
        self.endpoint = 'apiMessages/delete'
        self.params = {'id': id}
        self.payload = {}
        return super().delete()
