from threading import Thread
from time import sleep

class ThreadCommons(object):
    """docstring for ThreadCommons"""
    def __init__(self, inp, out, gen_dat):
        super(ThreadCommons, self).__init__()
        self.input_queue = inp # DICT: {'requests': [], 'responses': {}}
        self.output_queue = out # LIST: []
        self.general_data = gen_dat # DICT: {'running': True, 'server_queue': []}
        return

    def run_thread(self):
        while self.general_data['running']:
            print("running thread")
            sleep(1)
        return

    def constant_run(self):
        thread = Thread(target = self.run_thread)
        thread.start()
        while self.general_data['running']:
            if not thread.isAlive():
                self.output_queue.append("Restarting broken thread (%s)!" % thread.name)
                thread = Thread(target = self.run_thread)
                thread.start()
            sleep(3)
        return

    def run(self):
        thread = Thread(target = self.constant_run)
        thread.start()
        return thread
