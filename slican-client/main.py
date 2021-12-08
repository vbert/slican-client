# -*- coding:utf-8 -*-
"""
Project: slican-client
File: /slican_client.py
File Created: 2021-11-15, 11:36:32
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-08, 9:05:30
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os
import sys
import time
import logging
import socket
from typing import Mapping

from app_config import AppConfig
from slican.queue import Queue
from slican.commands import Commands
from rocekpl_api_client.messages import Messages
from rocekpl_api_client.messages_queue import MessagesQueue

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
    messages_queue = MessagesQueue(config)

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

    addr = (config.slican_host, int(config.slican_port))
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    connected = True
    logging.info('Connection to the server')

    commands = Commands(client)
    commands.run(commands.LOGI, pin=config.pin_sim_card)
    logging.info(commands.LOGI)

    # List of IDs of sent messages
    messages_sent = []
    while True:
        try:
            # Queue handling of SMS messages to be sent 
            is_queue = queue.check_queue()
            if(is_queue):
                messages_list = messages_queue.list()
                if messages_list['success'] == True:
                    for item in messages_list['data']:
                        msg_id = int(item['message_id'])
                        message_get = messages.get(msg_id)
                        if message_get['success'] == True:
                            message = message_get['data']
                            messages_sent.append(message['id'])
                            commands.run(commands.SMSS, recipient=message['recipient'], body=message['body'])
                            logging.info(commands.SMSS.format(k={'recipient': message['recipient'], 'body': message['body']}))
                        messages_queue_delete = messages_queue.delete(msg_id)
                        if messages_queue_delete['success'] == False:
                            logging.error(messages_queue_delete)

            # Handling incoming messages from Slican PBX
            message_incoming = client.recv(1024)
            if message_incoming != commands.EMPTY_FRAME:
                logging.info(message_incoming)
                incoming = commands.incoming_message(message_incoming)

                if incoming['cmd'] == 'aSMSA':
                    msg_id = messages_sent.pop(0)
                    msg_update = messages.update(
                        msg_id,
                        {
                            'order_id': incoming['order_id'],
                            'status': incoming['status']
                        }
                    )
                    if msg_update['success'] == False:
                        logging.error(msg_update)

                if incoming['cmd'] == 'aSMSR':
                    msg_byrecipient = messages.byrecipient(
                        incoming['recipient'],
                        incoming['order_id'],
                        {
                            'report_id': incoming['report_id'],
                            'status': incoming['status']
                        }
                    )
                    if msg_byrecipient['success'] == False:
                        logging.error(msg_byrecipient)
                    else:
                        commands.run(commands.SOK, report_id=incoming['report_id'])

                if incoming['cmd'] == 'aSMSG':
                    msg_create = messages.create({
                        'direction': '1',
                        'sender': incoming['sender'],
                        'recipient': config.sender_phone_number,
                        'body': incoming['body'],
                        'created_by': config.system_user_id,
                        'created_at': ' '.join(incoming['date_time'].split('_')),
                        'status': incoming['status'],
                        'report_id': incoming['report_id']
                    })
                    if msg_create['success'] == False:
                        logging.error(msg_create)
                    else:
                        commands.run(commands.SOK, report_id=incoming['report_id'])

            time.sleep(1)

        except socket.error:
            connected = False
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.error('Connected lost ... reconnecting')
            while not connected:
                try:
                    client.connect(addr)
                    connected = True
                    logging.info('Re-connection successful')
                except socket.error:
                    time.sleep(2)

    logging.info(commands.run(commands.LOGO))
    client.close()
    logging.info('Disconnecting from the server ')


if __name__ == '__main__':
    main()
