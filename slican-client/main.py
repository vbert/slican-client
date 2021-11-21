# -*- coding:utf-8 -*-
"""
Project: slican-client
File: /slican_client.py
File Created: 2021-11-15, 11:36:32
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-11-19, 12:42:04
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os
import sys
import json

#from rocekpl_api_client.api_client import ApiClient
from rocekpl_api_client.messages_queue import MessagesQueue

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    sys.stderr.write(
        'It looks like the dotenv module is not installed. '
        'To fix this, run: pip install python-dotenv')
    sys.exit(1)

msg_queue = MessagesQueue()

# mq_get = json.loads(msg_queue.create({'message_id': 127}))
# if mq_get['success']:
#     print(mq_get['data'])
# else:
#     print(mq_get['errors'])

print([
    msg_queue.delete(121),
    msg_queue.get(125),
    msg_queue.list(),
    msg_queue.create({'message_id': 126}),
    msg_queue.update(126, {'message_id': 121})
])
