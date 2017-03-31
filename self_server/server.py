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

    def show_starting_screen(self):
        string = """
* * * * * * * * * * * * * * * * * * * *
Welcome to the SNow synch server
To show help type "help" and push Enter
* * * * * * * * * * * * * * * * * * * *
"""
        self.output_queue.append(string)
        return

    def show_help(self, command):
        help_parts = command.split(" ")
        help_text = " ".join(help_parts[1:])
        if help_text == 'SOMETHING':
            string = """
UNKNOWN MESSAGE
"""
        else:
            string = """
* * * * * * * * * * * * * * * * * * * *
 H E L P
* * * * * * * * * * * * * * * * * * * *
Possible commands:
help - shows help
exit_all - close down program
* * * * * * * * * * * * * * * * * * * *
"""
        self.output_queue.append(string)

    def run_command(self,command):
        if command == 'exit_all':
            self.exit_all()
        elif command.split(" ")[0] in ("help", "man"):
            self.show_help(command)
        else:
            self.push_unknown_command(command)
        return

    def run_thread(self):
        while self.general_data['running']:
            if len(self.general_data['server_queue']) > 0:
                command = self.general_data['server_queue'].pop(0)
                self.run_command(command)
            sleep(0.03)
        return

    def run(self):
        self.show_starting_screen()
        return super(Server, self).run()