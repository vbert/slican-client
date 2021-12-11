# -*- coding:utf-8 -*-
"""
Project: slican
File: /timer.py
File Created: 2021-12-11, 19:47:15
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2021-12-11, 19:51:04
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 by vbert
"""
import datetime

def check_timer(timer, limit=1200):
    '''limit - number of seconds'''
    timer_now = datetime.datetime.now()
    delta = timer_now - timer
    if delta.seconds > limit:
        return (timer_now, True)
    else:
        return (timer_now, False)

# Check timer - protection against loss of authorization
# timer_start = datetime.datetime.now()
# timer_now, reset_timer = check_timer(timer_start)
# if reset_timer:
#     timer_start = timer_now
#     commands.run(commands.LOGO)
#     connected = socket_disconnect(client)
#     client, commands, connected = socket_connect(config)
#     commands.run(commands.LOGI, pin=config.pin_sim_card)
#     time.sleep(5)
