# -*- coding:utf-8 -*-
"""
Project: slican
File: /queue.py
File Created: 2021-12-05, 23:00:01
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-02-28, 22:55:36
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os
import logging

class Queue(object):

    # List of IDs of sent messages
    messages_sent = []

    def __init__(self, config) -> None:
        self.config = config
        # self.messages_sent = []


    def __file_path(self) -> str:
        return os.path.join(self.config.data_dir, self.config.messages_queue_file)


    def __read_timestamp(self) -> int:
        timestamp = 0
        full_path = self.__file_path()
        try:
            file = open(full_path, 'r+')
            timestamp = file.read()
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')
        return int(timestamp)


    def check_queue(self) -> bool:
        if self.__read_timestamp() > 0:
            return True
        else:
            return False


    def reset_timestamp(self) -> None:
        full_path = self.__file_path()
        try:
            file = open(full_path, 'r+')
            file.seek(0)
            file.truncate()
            file.write('0')
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')


    def process_mailing_list(self, messages_queue, messages, commands) -> bool:
        message_list = messages_queue.list()
        if message_list['success'] == True:
            for item in message_list['data']:
                msg_id = int(item['message_id'])
                message_get = messages.get(msg_id)
                if message_get['success'] == True:
                    message = message_get['data']
                    self.messages_sent.append(message['id'])
                    commands.run(commands.SMSS, recipient=message['recipient'], body=message['body'])
                    logging.info(commands.SMSS.format(k={'recipient': message['recipient'], 'body': message['body']}))

                    logging.warning(' - '.join(map(str, self.messages_sent)))

                messages_queue_delete = messages_queue.delete(msg_id)
                if messages_queue_delete['success'] == False:
                    logging.error(messages_queue_delete)
            return True
        else:
            return False


    def process_incoming_message(self, message_incoming, messages, phonecalls, commands, config):
        logging.info(message_incoming)
        
        message_list = message_incoming.decode(commands.CHARACTER_ENCODING).split(commands.SEPARATOR)
        for message in message_list:
            if len(message) > 0:
                incoming = commands.incoming_message(message)
                # aNA
                if incoming['cmd'] == 'aNA':
                    msg_id = self.messages_sent.pop(0)
                    msg_update = messages.update(
                        msg_id,
                        {
                            'error_text': incoming['error'],
                            'status': incoming['status']
                        }
                    )
                # aSMSA
                if incoming['cmd'] == 'aSMSA':
                    msg_id = self.messages_sent.pop(0)
                    if incoming['status'] == 'sent':
                        msg_update = messages.update(
                            msg_id,
                            {
                                'order_id': incoming['order_id'],
                                'status': incoming['status']
                            }
                        )
                    else:
                        msg_update = messages.update(
                            msg_id,
                            {
                                'status': incoming['status'],
                                'error_text': f"R{incoming['error_id']} {incoming['error']}"
                            }
                        )
                    logging.warning(' - '.join(map(str, self.messages_sent)))
                    if msg_update['success'] == False:
                        logging.error(msg_update)
                # aSMSR
                if incoming['cmd'] == 'aSMSR':
                    if incoming['status'] == 'delivered':
                        msg_byrecipient = messages.byrecipient(
                            incoming['recipient'],
                            incoming['order_id'],
                            {
                                'report_id': incoming['report_id'],
                                'status': incoming['status']
                            }
                        )
                    else:
                        msg_byrecipient = messages.byrecipient(
                            incoming['recipient'],
                            incoming['order_id'],
                            {
                                'report_id': incoming['report_id'],
                                'status': incoming['status'],
                                'error_text': f"E{incoming['error_id']} {incoming['error']}"
                            }
                        )
                    if msg_byrecipient['success'] == False:
                        logging.error(msg_byrecipient)
                    else:
                        commands.run(commands.SOK, report_id=incoming['report_id'])
                # aSMSG
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
                # aRING
                if incoming['cmd'] == 'aRING':
                    msg_create = phonecalls.create({
                        'status': '0',
                        'direction': '1',
                        'phone_number': incoming['incoming_phone']
                    })
                    if msg_create['success'] == False:
                        logging.error(msg_create)
                # Unknown Command
                if incoming['cmd'] == 'UnknownCommand':
                    logging.info({
                        'incoming': incoming
                    })
