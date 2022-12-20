# -*- coding:utf-8 -*-
"""
Project: slican
File: /queue.py
File Created: 2021-12-05, 23:00:01
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-12-18, 22:20:29
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os
import re
import json
import time
import logging

class Queue(object):

    # List of IDs of sent messages
    messages_sent = []

    # Phone number patern
    phone_number_pattert = '[0-9]{9}'

    # Handset is off hook
    off_hook = 0

    def __init__(self, config) -> None:
        self.config = config
        # self.messages_sent = []


    def __file_path(self, file_name) -> str:
        return os.path.join(self.config.data_dir, file_name)


    def __read_timestamp(self) -> int:
        timestamp = 0
        full_path = self.__file_path(self.config.messages_queue_file)
        try:
            file = open(full_path, 'r+')
            timestamp = file.read()
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')
        return int(timestamp)


    def check_message_queue(self) -> bool:
        if self.__read_timestamp() > 0:
            return True
        else:
            return False


    def check_phonedial_queue(self) -> str:
        full_path = self.__file_path(self.config.phonedial_queue_file)
        try:
            file = open(full_path, 'r+')
            phone_number = json.loads(file.read())
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')

        validate = re.match(self.phone_number_pattert, phone_number)
        if validate:
            return validate.string
        else:
            return 'BRAK'


    def reset_timestamp(self) -> None:
        full_path = self.__file_path(self.config.messages_queue_file)
        try:
            file = open(full_path, 'r+')
            file.seek(0)
            file.truncate()
            file.write('0')
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')


    def reset_dial_queue(self) -> None:
        full_path = self.__file_path(self.config.phonedial_queue_file)
        try:
            file = open(full_path, 'w+')
            file.write(json.dumps(''))
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')


    def process_mailing_list(self, messages_queue, messages, commands) -> bool:
        message_list = messages_queue.list()
        if message_list['success'] == True:
            timer = 0
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
                timer = timer + 1
                if timer < 4:
                    sleep = 5
                else:
                    timer = 0
                    sleep = 10
                time.sleep(sleep)
            return True
        else:
            return False


    def process_dial_number(self, phone_number, commands) -> bool:
        commands.run(commands.DIAL, recipient=phone_number)
        logging.info(commands.DIAL.format(k={'recipient': phone_number}))
        return True


    def process_incoming_message(self, message_incoming, messages, phonecalls, commands, config):
        logging.info(message_incoming)
        
        message_list = message_incoming.decode(commands.CHARACTER_ENCODING).split(commands.SEPARATOR)
        for message in message_list:
            if len(message) > 0:
                incoming = commands.incoming_message(message)
                # aNA
                if incoming['cmd'] == 'aNA':
                    self.off_hook = 0
                    msg_id = self.messages_sent.pop(0)
                    msg_update = messages.update(
                        msg_id,
                        {
                            'error_text': incoming['error'],
                            'status': incoming['status']
                        }
                    )
                # aSTAT
                if incoming['cmd'] == 'aSTAT':
                    self.off_hook = incoming['off_hook']
                # aDRDY
                if incoming['cmd'] == 'aDRDY':
                    if self.off_hook == 1:
                        self.off_hook = 0
                        # Check if there is phone number to dial
                        is_phonedial_queue = self.check_phonedial_queue()
                        logging.info('is_phonedial_queue: {k[recipient]}'.format(k={'recipient': is_phonedial_queue}))

                        if is_phonedial_queue != 'BRAK':
                            if self.process_dial_number(is_phonedial_queue, commands):
                                self.reset_dial_queue()
                # aSMSA
                if incoming['cmd'] == 'aSMSA':
                    self.off_hook = 0
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
                    self.off_hook = 0
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
                    self.off_hook = 0
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
                    self.off_hook = 0
                    msg_create = phonecalls.create({
                        'status': '0',
                        'direction': '1',
                        'phone_number': incoming['incoming_phone']
                    })
                    if msg_create['success'] == False:
                        logging.error(msg_create)
                # Unknown Command
                if incoming['cmd'] == 'UnknownCommand':
                    self.off_hook = 0
                    logging.info({
                        'incoming': incoming
                    })
