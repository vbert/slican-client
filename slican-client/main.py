# -*- coding:utf-8 -*-
"""
Project: slican-client
File: /slican_client.py
File Created: 2021-11-15, 11:36:32
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-09-27, 19:59:04
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
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
from rocekpl_api_client.messages_queue import MessagesQueue
from rocekpl_api_client.phonecalls import PhoneCalls

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    sys.stderr.write(
        'It looks like the dotenv module is not installed. '
        'To fix this, run: pip install python-dotenv')
    sys.exit(1)


def socket_connect(config, info='Connection to the server'):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (config.slican_host, int(config.slican_port))
    client.connect(addr)
    connected = True
    commands = Commands(client)
    logging.info(info)
    return client, commands, connected


def socket_disconnect(client):
    client.close()
    logging.info('Disconnecting from the server ')
    connected = False
    return connected


def main():
    config = AppConfig()
    queue = Queue(config)
    messages = Messages(config)
    messages_queue = MessagesQueue(config)
    phonecalls = PhoneCalls(config)

    # level=logging.{DEBUG INFO WARNING ERROR CRITICAL}
    log_format = '%(asctime)s %(levelname)-8s %(name)s - [%(filename)s:%(lineno)d] %(message)s'
    # Log in to the file
    logging.basicConfig(filename=os.path.join(config.log_dir, 'main.log'),
                        filemode='a',
                        format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)
    # Log in to the scren
    # logging.basicConfig(format=log_format,
    #                     datefmt='%Y-%m-%d %H:%M:%S',
    #                     level=logging.DEBUG)

    client, commands, connected = socket_connect(config)
    commands.run(commands.LOGI, pin=config.pin_sim_card)
    commands.run(commands.LOGA, access_key=config.access_key)

    while True:
        try:
            # Check if there is anything to send
            is_message_queue = queue.check_message_queue()
            # and if queue is not empty
            if is_message_queue:
                # process mailing list
                if queue.process_mailing_list(messages_queue, messages, commands):
                    queue.reset_timestamp()

            # Check if there is phone number to dial
            is_phonedial_queue = queue.check_phonedial_queue()
            if is_phonedial_queue != 'BRAK':
                if queue.process_dial_number(is_phonedial_queue, commands):
                    queue.reset_dial_queue()

            # Handling incoming messages from Slican PBX
            message_incoming = client.recv(1024)
            if message_incoming != commands.EMPTY_FRAME:
                queue.process_incoming_message(message_incoming, messages, phonecalls, commands, config)

            time.sleep(0.1)

        except socket.error:
            commands.run(commands.LOGO)
            connected = socket_disconnect(client)
            while not connected:
                try:
                    client, commands, connected = socket_connect(config, 'Connected lost ... reconnecting')
                    commands.run(commands.LOGI, pin=config.pin_sim_card)
                    logging.info('Re-connection successful')
                except socket.error:
                    connected = socket_disconnect(client)
                    time.sleep(2)

    connected = socket_disconnect(client)


if __name__ == '__main__':
    main()
