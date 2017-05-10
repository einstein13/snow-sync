from threading import Thread
from time import sleep

from commons.find import remove_from_list
from commons.threads import ThreadCommons
from .server_commands import ServerCommands
from .datatypes import CommandRecognizer

class Server(ThreadCommons, ServerCommands):

    exit_message_error = "Command exited with error"
    exit_message_ok = "Command exited correctly"
    exit_ok = False
    exit_silence = False

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
        self.exit_silence = True
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
    def get_user_input(self, question, invalid_message=None, default=None, options=[], typ=None):
        self.push_output(question)

        data_to_input = {'command': question}
        if invalid_message is not None:
            data_to_input['invalid_message'] = invalid_message
        if len(options) > 0:
            data_to_input['options'] = options
        if default is not None:
            data_to_input['default_value'] = default

        if typ is not None:
            if typ == 'password':
                data_to_input['character_replacement'] = '*'
            elif typ == 'commmon_switch':
                data_to_input['case_sensitive'] = False
            elif typ == 'case_sensitive':
                data_to_input['case_sensitive'] = False
            elif typ == 'enable_escaping':
                data_to_input['exit_current_on_escape'] = False

        answer = self.get_input_data(data_to_input)

        return answer

    def initiate_exit_message(self):
        self.exit_silence = False
        self.exit_ok = False
        return

    def print_exit_message(self):
        if self.exit_silence:
            return
        if self.exit_ok is True:
            self.push_output(self.exit_message_ok, typ="inset")
            return
        self.push_output(self.exit_message_error, typ="inset")
        return

    # handling with server input queue
    def remove_first_input(self):
        if len(self.general_data['server_queue']) > 0:
            self.general_data['server_queue'].pop(0)
        return

    def abort_current_command(self, name_to_remove):
        removed = remove_from_list(self.general_data['server_queue'], name_to_remove)
        self.push_output("Command aborted", typ="inset")
        self.exit_silence = True
        return

    # interpreting commands
    def run_command(self, command):
        self.initiate_exit_message()
        splitted = command.split(" ")

        CR = CommandRecognizer()
        command_to_execute = CR.return_command(command)
        exec(command_to_execute)

        self.print_exit_message()
        return

    def run_thread(self):
        while self.general_data['running']:
            if len(self.general_data['server_queue']) > 0:
                command = self.general_data['server_queue'].pop(0)
                self.run_command(command)
            sleep(0.03)
        return

    def run(self):
        self.initialize_servers_json()
        self.initialize_projects_home()
        self.show_starting_screen()
        return super(Server, self).run()