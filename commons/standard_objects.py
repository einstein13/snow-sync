from time import time

general_data = {
    'running': True,
    'server_queue': [],
    'watcher': { # settings for watcher
        'running': False,
        'last_pull': time(),
        'timediff_pull': 60,
        'last_push': time(),
        'sleep_time': 1.5
        }
    }