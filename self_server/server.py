from threading import Thread
from time import sleep

from commons.threads import ThreadCommons

class ServerCommands(object):

    def exit_all(self):
        self.general_data['running'] = False
        return

    def push_unknown_command(self, command):
        message = {}
        message['message'] = 'Unknown command: '+command
        message['type'] = 'text'
        self.output_queue.append(message)
        return

class Server(ThreadCommons, ServerCommands):

    def __init__(self, inp, out, gen_dat):
        super(Server, self).__init__(inp, out, gen_dat)
        return

    def run_command(self,command):
        if command == 'exit_all':
            self.exit_all()
        else:
            self.push_unknown_command(command)
        return

    def run_thread(self):
        from random import randint
        while self.general_data['running']:
            if len(self.general_data['server_queue']) > 0:
                command = self.general_data['server_queue'].pop(0)
                self.run_command(command)
            sleep(0.03)
        return