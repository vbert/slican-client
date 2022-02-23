# -*- coding:utf-8 -*-
"""
Project: slican-client
File: /test.py
File Created: 2022-02-23, 10:52:23
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-02-23, 20:27:53
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 - 2022 by vbert
"""
import os
import sys
import time
import socket
import logging

from app_config import AppConfig
from slican.queue import Queue
from slican.commands import Commands
from rocekpl_api_client.messages import Messages


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
    messages = Messages(config)
    commands = Commands(None)
    
    log_format = '%(asctime)s %(levelname)-8s %(name)s - [%(filename)s:%(lineno)d] %(message)s'
    logging.basicConfig(format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    
    coding = 'IBM852'
    separator = '\r\n'
    # message_incoming = b'aECHO 101_ 2\r\naECHO 101_ 2\r\naECHO 101_ 6\r\naECHO 101_ 4\r\naECHO 101_ 9\r\n'
    # message_incoming = b'aOK\r\naOK\r\n'
    # message_incoming = b'aSMSA G001 C 28\r\n'
    # message_incoming = b'aREL 101_ 1\r\n'
    message_incoming = b'aRING 101_ 502740930 5001 530644331 _ _\r\n'

    logging.info(f'PROCCESS: {message_incoming}')

    queue.process_incoming_message(message_incoming, messages, commands, config)


if __name__ == '__main__':
    main()
