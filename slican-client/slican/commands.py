# -*- coding:utf-8 -*-
"""
Project: slican
File: /commands.py
File Created: 2021-12-06, 13:46:18
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-09-27, 20:59:39
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import socket
from typing import Any

class Commands(object):

    # for sms
    INCOMING = ('aOK', 'aERROR', 'aNA', 'aSMSA', 'aSMSG', 'aSMSR')
    OUTGOING = ('aLOGI', 'aLOGO', 'aSMSS', 'aSOK')
    # for phone
    INCOMING += ('aECHO', 'aRING', 'aREL', 'aSTAT', 'aDRDY', 'aCONN')
    OUTGOING += ('aLOGA', 'aDIAL')


    LOGI = "aLOGI G001 {k[pin]}\r\n"
    LOGA = "aLOGA {k[access_key]}\r\n"
    LOGO = "aLOGO G001\r\n"
    SMSS = "aSMSS G001 {k[recipient]} C1 N 167 {k[body]}\r\n"
    SOK = "aSOK G001 {k[report_id]}\r\n"

    DIAL = "aDIAL 10__ {k[recipient]}"

    EMPTY_FRAME = b't\r\n'

    CHARACTER_ENCODING = 'IBM852'
    SEPARATOR = '\r\n'


    def __init__(self, client: socket) -> None:
        self.client = client


    def prepare(self, command: str, kwargs) -> str:
        return command.format(k=kwargs)


    def run(self, command: str, **kwargs) -> None:
        cmd = self.prepare(command, kwargs)

        print(cmd)

        self.client.sendall(bytes(cmd, self.CHARACTER_ENCODING))


    def incoming_message(self, message: str) -> dict:
        message_parts = message.split(' ', 7)
        if message_parts[0] in self.INCOMING:
            return self.handle_command(message_parts)
        else:
            return {
                'cmd': 'UnknownCommand',
                'unknown_command': message_parts[0],
                'status': 'error',
                'error': 'Nieznana komenda przychodzaca.'
            }


    def handle_command(self, message: dict) -> dict:
        response = {}
        command = message[0]
        if command == 'aSMSA':
            response = self.__command_SMSA(message)
        elif command == 'aSMSR':
            response = self.__command_SMSR(message)
        elif command == 'aSMSG':
            response = self.__command_SMSG(message)
        elif command == 'aNA':
            response = self.__command_NA(message)
        elif command == 'aERROR':
            response = self.__command_ERROR(message)
        elif command == 'aOK':
            response = self.__command_OK(message)
        elif command == 'aRING':
            response = self.__command_RING(message)
        elif command == 'aSTAT':
            response = self.__command_STAT(message)
        elif command == 'aDRDY':
            response = self.__command_DRDY(message)
        elif command == 'aDIAL':
            response = self.__command_DIAL(message)
        else:
            response = {}
        
        response['cmd'] = command
        return response


    def __command_RING(self, message) -> dict:
        return {
            'incoming_phone': message[2]
        }


    def __command_STAT(self, message) -> dict:
        off_hook = message[2]
        if off_hook == 'H':
            return {
                'off_hook': 1
            }
        else:
            return {
                'off_hook': 0
            }


    def __command_DRDY(self, message) -> dict:
        return {
            'dial_ready': message
        }


    def __command_DIAL(self, message) -> dict:
        return {}


    def __command_SMSA(self, message) -> dict:
        type = message[2]
        if type == 'C':
            return {
                'status': 'sent',
                'order_id': message[3]
            }
        else:
            return {
                'status': 'error',
                'error_id': message[3],
                'error': 'SMS został odrzucony przez operatora.'
            }


    def __command_SMSR(self, message) -> dict:
        type = message[2]
        if type == 'D':
            self.run(self.SOK, report_id=message[3])
            return {
                'status': 'delivered',
                'report_id': message[3],
                'order_id': message[4],
                'recipient': message[5]
            }
        else:
            return {
                'status': 'error',
                'report_id': message[3],
                'order_id': message[4],
                'error_id': message[5],
                'error': 'SMS nie został dostarczony do odbiorcy.',
                'recipient': message[6]
            }


    def __command_SMSG(self, message) -> dict:
        return {
            'status': 'received',
            'report_id': message[2],
            'sender': message[3],
            'date_time': message[6],
            'body': message[7]
        }


    def __command_NA(self, message) -> dict:
        if message[1]:
            return {
                'status': 'error',
                'error_id': message[1],
                'error': f'NA: {message[1]}'
            }
        else:
            return {
                'status': 'error',
                'error': 'Nieznany błąd.'
            }


    def __command_ERROR(self, message) -> dict:
        return {
            'status': 'error',
            'error': 'Komunikat lub parametry mają niewłaściwą składnię lub wartość.'
        }

    def __command_OK(self, message) -> dict:
        return {}
