# -*- coding:utf-8 -*-
"""
Project: rocekpl_api_client
File: /messages.py
File Created: 2021-11-22, 15:55:44
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-08, 8:22:27
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
from .api_client import ApiClient


class Messages(ApiClient):
    STATUS_QUEUED = 'queued'
    STATUS_SENT = 'sent'
    STATUS_DELIVERED = 'delivered'
    STATUS_ERROR = 'error'
    STATUS_RECIVED = 'received'

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
        self.params = {}
        self.payload = payload
        return super().create()


    def update(self, id: int, payload: dict) -> str:
        self.endpoint = 'apiMessages/update'
        self.params = {'id': id}
        self.payload = payload
        return super().update()


    def byrecipient(self, recipient: str, order_id: int, payload: dict) -> str:
        self.endpoint = 'apiMessages/byrecipient'
        self.params = {'recipient': recipient, 'order_id': order_id}
        self.payload = payload
        return super().update()


    def delete(self, id: int) -> str:
        self.endpoint = 'apiMessages/delete'
        self.params = {'id': id}
        self.payload = {}
        return super().delete()
