# -*- coding:utf-8 -*-
"""
Project: slican-client
File: /test2.py
File Created: 2022-12-18, 21:50:58
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-12-18, 22:20:50
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 - 2022 by vbert
"""
import time


def main():
    print('Test 2')

    message_list = {
        'data': [
            {
                'message_id': 1,
                'recipient': '123456789'
            },
            {
                'message_id': 2,
                'recipient': '345678901'
            },
            {
                'message_id': 3,
                'recipient': '567890123'
            },
            {
                'message_id': 4,
                'recipient': '123456789'
            },
            {
                'message_id': 5,
                'recipient': '345678901'
            },
            {
                'message_id': 6,
                'recipient': '567890123'
            },
            {
                'message_id': 7,
                'recipient': '123456789'
            },
            {
                'message_id': 8,
                'recipient': '345678901'
            },
            {
                'message_id': 9,
                'recipient': '567890123'
            },
            {
                'message_id': 10,
                'recipient': '123456789'
            },
            {
                'message_id': 11,
                'recipient': '345678901'
            },
            {
                'message_id': 12,
                'recipient': '567890123'
            }
        ]
    }

    timer = 0
    for item in message_list['data']:
        id = item['message_id']
        recipient = item['recipient']
        if timer < 4:
            sleep = 1
        else:
            timer = 0
            sleep = 5
        timer = timer + 1
        print(f'{id}: {recipient}, {timer} - {sleep}')
        time.sleep(sleep)


if __name__ == '__main__':
    main()