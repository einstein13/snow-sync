#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import time

general_data = {
    'running': True,
    'server_queue': [],
    'pull': False,
    'watcher': { # settings for watcher
        'running': False,
        'last_pull': time(),
        'timediff_minimal': 60,
        'timediff_multiplier': 3,
        'timediff_pull': 20,
        'last_push': time(),
        'sleep_time': 0.5
        }
    }

eol = "\r\n"