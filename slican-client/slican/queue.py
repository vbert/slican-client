# -*- coding:utf-8 -*-
"""
Project: slican
File: /queue.py
File Created: 2021-12-05, 23:00:01
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-06, 0:43:53
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import os

class Queue:

    def __init__(self, config) -> None:
        self.config = config


    def __file_path(self) -> str:
        return os.path.join(self.config.data_dir, self.config.messages_queue_file)


    def __read_timestamp(self) -> int:
        timestamp = 0
        full_path = self.__file_path()
        try:
            file = open(full_path, 'r+')
            timestamp = file.read()
            if int(timestamp) > 0:
                file.seek(0)
                file.truncate()
                file.write('0')
            file.close()
        except IOError:
            print(f'Cannot open file ({full_path})')
        return int(timestamp)


    def check_queue(self) -> bool:
        if self.__read_timestamp() > 0:
            return True
        else:
            return False
