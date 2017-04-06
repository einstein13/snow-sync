from time import sleep
from os import path, pardir

from .file_system import FileSystem

class ServerCommands(FileSystem):

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
        folder_path = self.get_project_path()
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