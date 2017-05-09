from base64 import b64encode
from time import sleep
from os import path, pardir

from commons.find import list_dict_find, list_dict_find_by_name
from commons.prints import pretty_json_print, dict_to_list, generate_standard_data_file_content,\
        fix_newline_signs, generate_hash
from .file_system import FileSystem
from .connection import Connection
from .datatypes import ContentDatabase

class ServerCommands(FileSystem, Connection):

    settings = {}
    settings_files = []
    exit_current = 'exit_current_command'
    no_settings_defined = "No settings defined! (hint: read_settings)"
    standard_confirm = ['yes', 'y', 'true', 't', 'tak']
    standard_reject = ['false', 'f', 'no', 'n', 'nie']
    standard_yes_no = standard_confirm + standard_reject

    # settings
    def read_settings(self, command):
        from settings.servers import servers
        if len(servers) == 0:
            self.push_output("No settings included!")
            return

        command_parts = command.split(" ")
        command_parts.append(None)
        if command_parts[0] == 'read':
            command_parts.pop(0)
            command_parts[0] = 'read_settings'

        message_ok = "Settings loaded sucessfully"
        # message_wrong = "Unable to load settings"

        found_settings = list_dict_find(servers, command_parts[1])
        self.settings = found_settings[1]
        self.push_output(message_ok + " (%s, %s)" % (found_settings[0], found_settings[1]['name']), typ="inset")

        result = self.test_connection()
        if result:
            self.push_output("Connection OK", typ="inset")
        else:
            self.push_output("Connection failed", typ="inset")
        self.exit_ok = True
        return

    def show_settings(self, command):
        self.exit_silence = True
        from settings.servers import servers
        elements = [['No', 'name', 'url']]
        for itr in range(len(servers)):
            server = servers[itr]
            elements.append([str(itr), server['name'], server['instance_url']])

        self.push_output("List of known servers:")
        self.push_output(elements, typ="table")
        return

    def add_settings(self, command):
        from settings.servers import servers

        # get needed info
        name = self.get_user_input('Type settings name:')
        if name is None:
            self.abort_current_command(self.exit_current)
            return
        if list_dict_find_by_name(servers, name) is not None:
            self.push_output("Given name (%s) is already used. Please chose another or delete current." % name)
            return

        instance_name = self.get_user_input('Instance name [%s]:' % name, default=name)
        if instance_name is None:
            self.abort_current_command(self.exit_current)
            return

        default_url = 'https://%s.service-now.com/' % instance_name
        instance_url = self.get_user_input('Instance url [%s]:' % default_url, default=default_url)
        if instance_url is None:
            self.abort_current_command(self.exit_current)
            return

        user_name = self.get_user_input('Username for instance [admin]:', default='admin')
        if user_name is None:
            self.abort_current_command(self.exit_current)
            return

        user_password = self.get_user_input('User password for instnce:', typ='password')
        if user_password is None:
            self.abort_current_command(self.exit_current)
            return

        hashed_data = b64encode(bytes(user_name + ":" + user_password, "UTF-8")).decode("UTF-8")

        # add settings to servers list
        completed_data = {
            'name': name,
            'authorization': hashed_data,
            'instance_name': instance_name,
            'instance_url': instance_url
        }
        servers.append(completed_data)
        string_data = pretty_json_print(servers)
        self.override_servers_settings_file(string_data)
        self.push_output("Settings stored", typ="inset")

        # add folder to settings
        self.create_settings_folder(name)
        self.initialize_files_folder(name)

        # test connection
        test_result = self.test_connection(server_data=completed_data)
        if test_result:
            self.push_output("Connection OK", typ="inset")
        else:
            self.push_output("Connection is not working", typ="inset")

        self.exit_ok = True
        return

    def delete_settings(self, command):
        from settings.servers import servers
        splitted = command.split(" ")

        # name
        name = None
        if splitted[0] == "delete_settings" and len(splitted) > 1:
            name = splitted[1]
        elif len(splitted) > 2:
            name = splitted[2]
        else:
            name = self.get_user_input('Type settings name:')

        if name is None:
            self.abort_current_command(self.exit_current)
            return

        # look for correct settings
        found_settings = list_dict_find_by_name(servers, name)
        if found_settings is None:
            self.push_output("Can't find any settings by given name (%s)." % name)
            return

        # confirm deletion
        string = "Confirm deletion of \"" + name + "\" settings (yes/no):"
        confirmation = self.get_user_input(string,
                invalid_message="Give yes/no answer:", options=self.standard_yes_no,
                typ="commmon_switch")

        # reject deletion
        if confirmation in self.standard_reject:
            self.exit_ok = True
            return

        # remove settings folder
        self.remove_settings_folder(found_settings[1]['name'])

        # delete from settings file
        servers.pop(found_settings[0])
        string_data = pretty_json_print(servers)
        self.override_servers_settings_file(string_data)

        # delete from memory (if matches)
        if self.settings and self.settings['name'] == name:
            self.settings = {}

        self.push_output("Settings removed successfully", typ="inset")
        self.exit_ok = True
        return

    def show_files(self, commandd):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        self.exit_silence = True
        files = self.get_settings_files_list()
        records = [["No.", "type", "name", "table", "sys_id"]]
        for itr in range(len(files)):
            row = files[itr]
            records.append([
                    str(itr), row["type"], row["name"],
                    row["table"], row["sys_id"]
                ])
        self.push_output("Synchronized records:")
        self.push_output(records, typ="table")
        return

    def show_result_data_in_table(self, result_data):
        self.push_output("List of all downloaded elements:")
        elements = [["name", "value"]]
        elements = dict_to_list(result_data, elements)
        self.push_output(elements, typ="table")
        return

    def add_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        CD = ContentDatabase()

        all_options = CD.get_all_aliases()
        result_data_shown = False

        # GET NECESSARY DATA FROM THE USER

        strings = [
            "[Business Rule/ Data Policy/ Script Include/ Client Script /",
            "UI Policy / UI Action / UI Page / UI Macro / UI Script / UI Context Menu /",
            "Catalog UI Policy / Catalog Client Script / Custom]",
            ]
        for string in strings:
            self.push_output(string)
        string = "Choose record type:"
        found_type = self.get_user_input(string, options=all_options, typ="commmon_switch")
        if found_type is None:
            return

        record_characteristics = CD.find_data_by_alias(found_type)
        if record_characteristics == {}:
            self.push_output("Error occured while looking for record standard data")
            return

        # table
        table = record_characteristics['table']
        if table == "":
            table = self.get_user_input("Table name of the record:", typ="case_sensitive")
            if table is None:
                return

        # sys_id
        sys_id = self.get_user_input("Record sys_id:")
        if sys_id is None:
            return

        # downloaded data
        self.push_output("Getting record data", typ="inset")
        record_data = self.connect_api(table, sys_id=sys_id)
        if record_data is None:
            self.push_output("Error occured while reading remote files", typ="inset")
            return
        result_data = record_data['result']

        # record name
        record_name = ""
        if record_characteristics["record_name"] == "":
            if not result_data_shown:
                self.show_result_data_in_table(result_data)
                result_data_shown = True
            # Ask about record name
            question = "Name of the record (attribute or user defined in quotation marks):"
            record_name = self.get_user_input(question, typ="case_sensitive")
            if record_name is None:
                return
            # Get data
            quotations = ["\"", "\'"]
            if record_name[0] in quotations and record_name[-1] in quotations:
                record_name = record_name[1:len(record_name)-1]
            else:
                try:
                    record_name = result_data[record_name]
                except:
                    self.push_output("There is no given attribute in the result data", typ="inset")
                    return
        else:
            record_name = result_data[record_characteristics["record_name"]]

        # record type
        record_type = self.standard_paths[record_characteristics["files_custom"]]
        if record_characteristics["standard_path_name"]:
            record_type = self.standard_paths[record_characteristics["standard_path_name"]]

        # list of script files
        scripts_list = record_characteristics['scripts_list']
            # list of fields
                # [field, file_name]

        # list of fileds
        fields_list = record_characteristics['fields_list']
            # list of fields
                # string - base group
                # [name_of_field, additional_comments, "", field_data]

        if scripts_list == [] and fields_list == []:
            if not result_data_shown:
                self.show_result_data_in_table()
                result_data_shown = True
            # Ask about all scripts and other fields

        # NOW SAVE DATA TO THE FILES

        saved_hashes = []
            # list of saved hashes of files (just to check if the files were modified)
                # [field, file, hash]
        
        # create storage folder
        self.create_record_folder(record_type, record_name)

        # create scripts files
        if len(scripts_list) > 0:
            for row in scripts_list:
                string_data = fix_newline_signs(result_data[row[0]])
                data = [record_type, record_name, row[1], string_data]
                self.override_record_file(data)
                # save hash
                hashed = generate_hash(string_data)
                saved_hashes.append([row[0], row[1], hashed])

        # create data file
        if len(fields_list) > 0:
            file_content = generate_standard_data_file_content(result_data, fields_list)
            data = [record_type, record_name, self.standard_paths['file_standard_file'], file_content]
            self.override_record_file(data)
            # save hash
            hashed = generate_hash(file_content)
            saved_hashes.append(['__all_fields__', self.standard_paths['file_standard_file'], hashed])

        # create custom project settings
        record_settings = {
            'type': record_type,
            'name': record_name,
            'table': table,
            'sys_id': sys_id,
            'hashed_data': saved_hashes
        }
        self.add_files_settings(record_settings)

        self.exit_ok = True
        return

    def delete_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return
        return

    def truncate_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return
        return

    # pull from the server
    def pull_all_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
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
    def exit_all(self, command):
        self.exit_silence = True
        self.push_output("Exiting program", typ="pretty_text")
        sleep(0.05)
        self.general_data['running'] = False
        return

    def exit_with_prompt(self, command):
        self.exit_silence = True
        string = "Confirm exiting (yes/no) [yes]:"
        confirmation = self.get_user_input(string,
                invalid_message="Give yes/no answer:", options=self.standard_yes_no,
                typ="commmon_switch", default="yes")
        if confirmation in self.standard_reject or confirmation is None:
            self.push_output("Aborted", typ="inset")
            return
        self.exit_all("exit")
        return

    def exit_current_command(self, command):
        self.exit_ok = True
        self.exit_silence = True
        return

    def push_unknown_command(self, command):
        self.push_output("Unknown command: " + command)
        self.exit_silence = True
        return