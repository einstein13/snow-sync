from threading import Thread
from time import sleep

from commons.find import remove_from_list
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
            "FILES:",
            "  show_files - show list of files within configuration",
            "  add_files - add new file to the configuration",
            "  delete_files - delete existing file record from the configuration",
            "  truncate_files - delete all records from the configuration",
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
    def get_user_input(self, question, command=None, default=None, options=[], typ=None):
        self.push_output(question)

        data_to_input = {'command': question}
        if command is not None:
            data_to_input['command'] = command
        if len(options) > 0:
            data_to_input['options'] = options
        if default is not None:
            data_to_input['default_value'] = default

        if typ is not None:
            if typ == 'password':
                data_to_input['character_replacement'] = '*'

        answer = self.get_input_data(data_to_input)

        return answer

    # handling with server input queue
    def remove_first_input(self):
        if len(self.general_data['server_queue']) > 0:
            self.general_data['server_queue'].pop(0)
        return

    def abort_current_command(self, name_to_remove):
        removed = remove_from_list(self.general_data['server_queue'], name_to_remove)
        self.push_output("Command aborted", typ="inset")
        return

    # interpreting commands
    def run_command(self, command):
        splitted = command.split(" ")
        if command == 'exit':
            self.exit_all()
        elif splitted[0] == 'read_settings' or\
                (splitted[0] == 'read' and splitted[1] == 'settings'):
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
        elif command == "delete_settings" or command == "delete settings":
            self.delete_settings(command)
        elif command == "add_files" or command == "add files":
            self.add_files(command)
        elif command == "show_files" or command == "show files":
            self.show_files(command)
        elif command == "delete_files" or command == "delete files":
            self.delete_files(command)
        elif command == "truncate_files" or command == "truncate files":
            self.truncate_files(command)
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