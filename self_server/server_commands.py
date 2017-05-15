from base64 import b64encode
from time import sleep
from os import path, pardir

from commons.find import list_dict_find, list_dict_find_by_name
from commons.prints import pretty_json_print, dict_to_list, generate_standard_data_file_content,\
        fix_newline_signs, generate_hash
from .file_system import FileSystem
from .connection import Connection
from .datatypes import ContentDatabase, CommandRecognizer

class ServerCommands(FileSystem, Connection):

    settings = {}
    settings_files = []
    exit_current = 'exit_current_command'
    no_settings_defined = "No settings defined! (hint: read_settings)"
    command_aborted = "Command aborted"
    standard_confirm = ['yes', 'y', 'true', 't', 'tak']
    standard_reject = ['false', 'f', 'no', 'n', 'nie']
    standard_yes_no = standard_confirm + standard_reject
    file_status_names = {
        'no_change': "No changes",
        'changed': "Record changed",
        'error': "ERROR"
        }

    # settings
    def read_settings(self, command):
        from settings.servers import servers
        if len(servers) == 0:
            self.push_output("No settings included!")
            return

        CR = CommandRecognizer()
        command_arguments = CR.return_command_arguments(command)

        message_ok = "Settings loaded sucessfully"
        # message_wrong = "Unable to load settings"

        found_settings = list_dict_find(servers, command_arguments[1])
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
        CR = CommandRecognizer()
        command_arguments = CR.return_command_arguments(command)

        # name
        name = None
        if command_arguments[1] != '':
            name = command_arguments[1]
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

    def show_files_list(self):
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

    def show_files(self, commandd):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        self.exit_silence = True
        self.show_files_list()
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
        record_type = self.standard_paths["files_custom"]
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

            # Ask about all scripts
            self.push_output("Define fields that will be saved as files (Esc = next step)")
            while True:

                field_name = self.get_user_input("Field name:", typ="enable_escaping")
                if field_name is None:
                    break

                file_name = self.get_user_input("File name (for %s):" % field_name, typ="enable_escaping")
                if file_name is None:
                    break

                scripts_list.append([field_name, file_name])

            # Ask about all fileds
            fields_list.append("Basic")
            self.push_output("Define all custom fields that will be stored in a single data file (Esc = end process)")
            while True:
                comment = self.get_user_input("Field description (comment):", typ="enable_escaping")
                if comment is None:
                    break

                field_name = self.get_user_input("Field name:", typ="enable_escaping")
                if field_name is None:
                    break

                fields_list.append([comment, "", field_name])

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
            'hashed_data': saved_hashes,
            'head_folder_name': record_type,
            'internal_folder_name': record_name
        }
        self.add_files_settings(record_settings)

        self.exit_ok = True
        return

    def delete_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        CR = CommandRecognizer()
        command_arguments = CR.return_command_arguments(command)

        # file number
        number = None
        if command_arguments[1] != '':
            number = command_arguments[1]
        if number is None:
            self.show_files_list()
            number = self.get_user_input("Write file number to delete:")
        if number is None:
            self.abort_current_command(self.exit_current)
            return
        try:
            number = int(number)
        except:
            self.push_output("\"%s\" is not a valid integer" % number, typ="inset")
            return

        result = self.delete_files_settings(number)
        if result is False:
            self.push_output("Number out of range", typ="inset")
            return

        self.push_output("File removed from database", typ="inset")
        self.exit_ok = True
        return

    def truncate_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        self.show_files_list()
        string = "Confirm deleting all data about files (yes/no):"
        confirmation = self.get_user_input(string,
                invalid_message="Give yes/no answer:", options=self.standard_yes_no,
                typ="commmon_switch")

        if confirmation in self.standard_confirm:
            number = self.truncate_files_settings()
            string = "Deleted %s record" % number
            if number != 0:
                string += "s"
            self.push_output(string, typ="inset")
        self.exit_ok = True
        return

    # list files that changed
    def list_files_changes(self):
        result = []
        # returned result (list elemnets):
            # written status
            # content
        # last element:
            # found changes number
            # found errors number
        changes_number = 0
        errors_number = 0
        all_files = self.get_settings_files_list()
        for record in all_files:
            files_content = self.get_files_content(record)
            # error
            if files_content is None:
                result.append([self.file_status_names['error'], record])
                errors_number += 1
                continue
            # if changed anything
            changed = False
            for file_data in record['hashed_data']:
                if not file_data[-1]:
                    changed = True
                    break
            self.push_output(str(changed), typ="inset")
            if changed:
                result.append([self.file_status_names['changed'], files_content])
                changes_number += 1
            else:
                result.append([self.file_status_names['no_change'], files_content])
        result.append([changes_number, errors_number])
        return result

    # pull from the server
    def pull_one_file(self, file_data):
        pass

    def pull_all_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        # find status of current files
        changed_files = self.list_files_changes()
        changes_and_errors = changed_files.pop(-1)
        continue_process = True

        # if some changes detected
        if changes_and_errors[0] > 0:
            string = "There were some changes detected. Pulling can erase them."
            self.push_output(string)
            string = "Do you want to proceed [YES/no]?"
            continue_process = self.get_user_input(string, default="yes",
                    invalid_message="Give yes/no answer:", options=self.standard_yes_no,
                    typ="commmon_switch")
            if continue_process is None:
                self.abort_current_command(self.exit_current)
                return
            continue_process = continue_process in self.standard_confirm

        # if not continuing
        if not continue_process:
            self.exit_ok = True
            return

        # pull all files
        files_list = self.get_settings_files_list()
        self.push_output(str(files_list), "pretty_text")
        # for file_data in self.settings

        # exit command
        self.exit_ok = True
        return

    # push to the server
    def push_all_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return
        return

    # status of files (which are and which aren't modified)
    def show_files_status(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return
        # find status
        changed_files = self.list_files_changes()
        changes_and_errors = changed_files.pop(-1)

        # display info about files
        string = ""
        if changes_and_errors[1] > 0:
            string = "" + str(changes_and_errors[1]) + "error"
            if changes_and_errors[1] > 1:
                string += "s"
            string += " occured while reading files from the disk"
            self.push_output(string, typ="inset")
        if changes_and_errors[0] == 0:
            string = "No changes detected"
        else:
            string = "There are "
            string += str(changes_and_errors[0])
            string += " change"
            if changes_and_errors[0] > 1:
                string += "s"
            string += " detected"
        self.push_output(string, typ="inset")

        # what to display? (any lists?)
        show_changed = False
        show_all = False
        if changes_and_errors[0] + changes_and_errors[1] > 0:
            string = "Do you want to display changed/error files list [YES/no]?"
            show_changed = self.get_user_input(string, default="yes",
                    invalid_message="Give yes/no answer:", options=self.standard_yes_no,
                    typ="commmon_switch")
            if show_changed is None:
                self.abort_current_command(self.exit_current)
                return
            show_changed = show_changed in self.standard_confirm
        if show_changed is False:
            string = "Do you want to display all files status [YES/no]?"
            show_all = self.get_user_input(string, default="yes",
                    invalid_message="Give yes/no answer:", options=self.standard_yes_no,
                    typ="commmon_switch")
            if show_all is None:
                self.abort_current_command(self.exit_current)
                return
            show_all = show_all in self.standard_confirm

        # displaying chosen lists
        if show_changed:
            names_to_find = []
            names_to_find.append(self.file_status_names['changed'])
            names_to_find.append(self.file_status_names['error'])
            result_data = [["No.", "status", "type", "name", "table"]]
            itr = 0
            for record in changed_files:
                if record[0] in names_to_find:
                    itr += 1
                    result_data.append(
                            [str(itr), record[0], record[1]['type'],
                            record[1]['name'], record[1]['table']]
                            )
            self.push_output(result_data, typ="table")
        if show_all:
            names_to_find = []
            names_to_find.append(self.file_status_names['no_change'])
            names_to_find.append(self.file_status_names['changed'])
            names_to_find.append(self.file_status_names['error'])
            result_data = [["No.", "status", "type", "name", "table"]]
            itr = 0
            for record in changed_files:
                if record[0] in names_to_find:
                    itr += 1
                    result_data.append(
                            [str(itr), record[0], record[1]['type'],
                            record[1]['name'], record[1]['table']]
                            )
            self.push_output(result_data, typ="table")

        self.exit_ok = True
        return

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
        if confirmation is None:
            self.abort_current_command(self.exit_current)
            return
        if confirmation in self.standard_reject:
            self.push_output("Aborted", typ="inset")
            return
        self.exit_all("exit")
        return

    def exit_current_command(self, command):
        self.exit_ok = True
        # self.exit_silence = True
        # it shouldn't be run - command should be erased before executing
        self.push_output("Warning: exit_current_command command")
        return

    def push_unknown_command(self, command):
        self.push_output("Unknown command: " + command)
        self.exit_silence = True
        return