# -*- coding:utf-8 -*-
"""
Project: slican-client
File: /slican_client.py
File Created: 2021-11-15, 11:36:32
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-06, 0:44:37
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os
import sys
import json
import time
from typing import Mapping

from app_config import AppConfig
from rocekpl_api_client.api_client import ApiClient
from rocekpl_api_client.messages_queue import MessagesQueue
from rocekpl_api_client.messages import Messages
from slican.queue import Queue

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    sys.stderr.write(
        'It looks like the dotenv module is not installed. '
        'To fix this, run: pip install python-dotenv')
    sys.exit(1)

def main():
    config = AppConfig()

    queue = Queue(config)
    if(queue.check_queue()):
        msg_queue = MessagesQueue(config)
        msgqs = [
            # msg_queue.delete(121),
            msg_queue.get(125),
            # msg_queue.list(),
            # msg_queue.create({'message_id': 126}),
            # msg_queue.update(126, {'message_id': 121})
        ]
        for msgq in msgqs:
            print(msgq)

        message = Messages(config)
        msgs = [
            # message.delete(4),
            message.get(9),
            # message.list(),
            # message.create({'id': 4, 'sender': '530644331', 'recipient': '502740930', 'body': 'Kolejna wiadomosc testowa.', 'created_by': 1}),
            # message.update(4, {'sender': '530644331', 'recipient': '502740930', 'body': f'Wiadomosc testowa {time.time()}', 'created_by': 1})
        ]
        for msg in msgs:
            print(msg)


if __name__ == '__main__':
    main()
