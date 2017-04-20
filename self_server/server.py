from threading import Thread
from time import sleep

from commons.threads import ThreadCommons
from .server_commands import ServerCommands

class Server(ThreadCommons, ServerCommands):

    def __init__(self, inp, out, gen_dat):
        super(Server, self).__init__(inp, out, gen_dat)
        self.settings = {}
        return

    # help parts
    def show_starting_screen(self):
        string = "Welcome to the SNow synch server\nTo show help type \"help\" and push Enter"
        self.push_output(string, typ='pretty_text')
        return

    def show_help(self, command):
        command_parts = command.split(" ")
        help_text = " ".join(command_parts[1:])
        all_known_commands = [
            "BASIC:",
            "  help - shows help",
            "  exit - close down program (at any stage)",
            "SETTINGS:",
            "  show_settings - show table with all known settings",
            "  read_settings - read chosen settings from recorded file",
            "  add_settings - add new settings to recorded file",
            "  delete_settings - delete chosen settings from recorded file",
            "SYNCHRO:",
            "  pull - get all files from the server",
            "  push - update files on the server"
            ]
        if help_text == 'SOMETHING':
            string = "UNKNOWN MESSAGE"
        else:
            string = "H E L P\nPossible commands:\n"
            string += "\n".join(all_known_commands)
        self.push_output(string, typ='pretty_text')
        return

    # user commands
    def get_user_input(self, question, command=None, options=[]):
        self.push_output(question)

        data_to_input = {'command': question}
        if command is not None:
            data_to_input['command'] = command
        if len(options) > 0:
            data_to_input['options'] = options

        answer = self.get_input_data(data_to_input)

        return answer

    # interpreting commands
    def run_command(self, command):
        if command == 'exit':
            self.exit_all()
        elif command.split(" ")[0] == 'read_settings':
            self.read_settings(command)
        elif command == "pull":
            self.pull_all_files(command)
        elif command == "push":
            self.push_all_files(command)
        elif command.split(" ")[0] in ("help", "man"):
            self.show_help(command)
        elif command == "add_settings" or command == "add settings":
            self.add_settings(command)
        elif command == "show_settings" or command == "show settings":
            self.show_settings(command)
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