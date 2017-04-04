from threading import Thread
from time import sleep
from os import path, pardir

from commons.threads import ThreadCommons

class ServerCommands(object):

    settings = {}

    # reading settings
    def read_settings(self, command):
        from settings.servers import servers
        if len(servers) == 0:
            self.output_queue.append({'type': 'text', 'message': "No settings included!"})
            return

        command_parts = command.split(" ")
        message_ok = "Settings loaded sucessfully"
        message_wrong = "Unable to load settings"
        if len(command_parts) == 1:
            self.settings = servers[0]
            self.output_queue.append({'type': 'text', 'message': message_ok})
            return
        
        number = -1
        try:
            number = int(command_parts[1])
        except:
            pass
        if number > 0:
            try:
                self.settings = servers[number-1]
                self.output_queue.append({'type': 'text', 'message': message_ok})
                return
            except:
                pass

        for dictionary in servers:
            if 'name' in dictionary.keys() and dictionary['name'] == command_parts[1]:
                self.settings = dictionary
                self.output_queue.append({'type': 'text', 'message': message_ok})
                return

        self.output_queue.append({'type': 'text', 'message': message_wrong})
        return

    # pull from the server
    def pull_all_files(self, command):
        if self.settings == {}:
            self.output_queue.append({'type': 'text', 'message': 'No settings defined! (read_settings)'})
            return
        file_path = path.abspath(__file__)
        folder_path = file_path
        for itr in range(3):
            folder_path = path.abspath(path.join(folder_path, pardir))
        print(folder_path)
        return

    # push to the server
    def push_all_files(self, command):
        pass

    # exiting program
    def exit_all(self):
        self.output_queue.append({'type': 'pretty_text', 'message': 'Exiting program'})
        sleep(0.05)
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
        self.settings = {}
        return

    # help parts
    def show_starting_screen(self):
        string = "Welcome to the SNow synch server\nTo show help type \"help\" and push Enter"
        self.output_queue.append({'type': 'pretty_text', 'message': string})
        return

    def show_help(self, command):
        command_parts = command.split(" ")
        help_text = " ".join(command_parts[1:])
        all_known_commands = [
            "help - shows help",
            "exit - close down program",
            "read_settings - read settings from recorded file",
            "pull - get all files from the server",
            "push - update files on the server"
            ]
        if help_text == 'SOMETHING':
            string = "UNKNOWN MESSAGE"
        else:
            string = "H E L P\nPossible commands:\n"
            string += "\n".join(all_known_commands)
        self.output_queue.append({'type': 'pretty_text', 'message': string})
        return

    # interpreting commands
    def run_command(self,command):
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