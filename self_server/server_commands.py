from time import sleep
from os import path, pardir

from commons.find import list_dict_find
from .file_system import FileSystem

class ServerCommands(FileSystem):

    settings = {}

    # settings
    def read_settings(self, command):
        from settings.servers import servers
        if len(servers) == 0:
            self.push_output("No settings included!")
            return

        command_parts = command.split(" ")
        command_parts.append(None)
        message_ok = "Settings loaded sucessfully"
        # message_wrong = "Unable to load settings"

        found_settings = list_dict_find(servers, command_parts[1])
        self.settings = found_settings[1]
        self.push_output(message_ok + " (%s, %s)" % (found_settings[0], found_settings[1]['name']))
        return

    def show_settings(self, command):
        from settings.servers import servers
        elements = [['No', 'name', 'url']]
        for itr in range(len(servers)):
            server = servers[itr]
            elements.append([str(itr), server['name'], server['base_url']])

        self.push_output("List of known servers:")
        self.push_output(elements, typ="table")
        return

    def add_settings(self, command):
        from settings.servers import servers
        name = self.get_user_input('Type settings name:')
        self.push_output(name, typ="pretty_text")
        return

    # pull from the server
    def pull_all_files(self, command):
        if self.settings == {}:
            self.push_output("No settings defined! (hint: read_settings)")
            return
        folder_path = self.get_project_path()
        print(folder_path)
        print("* * *")
        self.get_settings_folder()
        return

    # push to the server
    def push_all_files(self, command):
        pass

    # exiting program
    def exit_all(self):
        self.push_output("Exiting program", typ="pretty_text")
        sleep(0.05)
        self.general_data['running'] = False
        return

    def push_unknown_command(self, command):
        self.push_output("Unknown command: " + command)
        return