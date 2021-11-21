# -*- coding:utf-8 -*-
"""
Project: rocekpl_api_client
File: /messages_queue.py
File Created: 2021-11-15, 16:18:16
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-11-19, 12:39:48
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
from .api_client import ApiClient


class MessagesQueue(ApiClient):

    def __init__(self) -> None:
        super().__init__()


    def list(self) -> str:
        self.endpoint = 'messagesQueue'
        self.params = {}
        self.payload = {}
        return super().get()


    def get(self, id: int) -> str:
        self.endpoint = 'messagesQueue'
        self.params = {'id': id}
        self.payload = {}
        return super().get()


    def create(self, payload: dict) -> str:
        self.endpoint = 'messagesQueue/create'
        self.params = {}
        self.payload = payload
        return super().create()


    def update(self, id: int, payload: dict) -> str:
        self.endpoint = 'messagesQueue/update'
        self.params = {'id': id}
        self.payload = payload
        return super().update()


    def delete(self, id: int) -> str:
        self.endpoint = 'messagesQueue/delete'
        self.params = {'id': id}
        self.payload = {}
        return super().delete()
