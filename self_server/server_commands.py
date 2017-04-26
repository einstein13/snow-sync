from base64 import b64encode
from time import sleep
from os import path, pardir

from commons.find import list_dict_find, list_dict_find_by_name
from commons.prints import pretty_json_print, dict_to_list, generate_standard_data_file_content, fix_newline_signs
from .file_system import FileSystem
from .connection import Connection

class ServerCommands(FileSystem, Connection):

    settings = {}
    settings_files = []
    exit_current = 'exit_current_command'
    no_settings_defined = "No settings defined! (hint: read_settings)"

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
        return

    def show_settings(self, command):
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
        confirm = ['yes', 'y', 'true', 't']
        reject = ['false', 'f', 'no', 'n']
        available_options = confirm + reject
        confirmation = self.get_user_input(string, options=available_options, typ="commmon_switch")

        # reject deletion
        if confirmation in reject:
            return

        # remove settings folder
        self.remove_settings_folder(found_settings[1]['name'])

        # delete from settings file
        servers.pop(found_settings[0])
        string_data = pretty_json_print(servers)
        self.override_servers_settings_file(string_data)

        self.push_output("Settings removed successfully", typ="inset")
        return

    def show_files(self, commandd):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

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

    def add_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        # type
        business_rule = ["business rule", "business_rule", "businessrule", "br", "business"]
        script_include = ["script include", "script_include", "scriptinclude", "si", "include"]
        ui_policy = ["ui policy", "ui_policy", "uipolicy", "user interface policy", "user_interface_policy", "ui p", "uip", "ui_p", "policy"]
        ui_action = ["ui action", "ui_action", "uiaction", "user interface action", "user_interface_action", "ui a", "uia", "ui_a", "action"]
        data_policy = ["data policy", "data_policy", "datapolicy", "dp", "data"]
        client_script = ["client script", "client_script", "clientscript", "cs", "client"]
        custom = ["custom", "custom file", "custom_file", "customfile", "user defined", "user_defined", "userdefined"]

        all_options = business_rule + script_include + ui_policy + ui_action + data_policy + client_script + custom

        string = "[Business Rule/ Data Policy/ Script Include/ UI Policy/ UI Action/ Client Script /Custom]"
        self.push_output(string)
        string = "Choose record type:"
        found_type = self.get_user_input(string, options=all_options, typ="commmon_switch")
        if found_type is None:
            return

        # table
        table = None

        if found_type in custom:
            table = self.get_user_input("Table name of the record:", typ="case_sensitive")
            if table is None:
                return
        elif found_type in business_rule:
            table = "sys_script"
        elif found_type in script_include:
            table = "sys_script_include"
        elif found_type in ui_policy:
            table = "catalog_ui_policy"
        elif found_type in ui_action:
            table = "sys_ui_action"
        elif found_type in data_policy:
            table = "sys_data_policy2"
        elif found_type in client_script:
            table = "sys_script_client"

        # sys_id
        sys_id = self.get_user_input("Record sys_id:")
        if sys_id is None:
            return

        record_data = self.connect_api(table, sys_id=sys_id)
        if record_data is None:
            self.push_output("Error occured while reading remote files", typ="inset")
            return
        result_data = record_data['result']

        scripts_list = []
            # list of fields
                # [field, file_name]
        fields_list = []
            # list of fields
                # string - base group
                # [name_of_field, additional_comment, field_data]
        record_name = None
        record_type = None

        # commonly used values
        boolean = "[true/false]"

        if found_type in custom:
            self.push_output("List of all downloaded elements:")
            elements = [["name", "value"]]
            elements = dict_to_list(result_data, elements)
            self.push_output(elements, typ="table")

            record_type = "custom"
            # TO DO !!!
            # scripts?
            # what to save?
            # comments?

        elif found_type in business_rule:
            record_type = self.standard_paths['files_business_rule']
            record_name = result_data['name']
            scripts_list = [
                ["script", "script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Application", "(read only!)", "sys_scope.value"],
                    ["Table", "", "collection"],
                    ["Active", boolean, "active"],
                    ["Advanced", boolean, "advanced"],
                    "When to run",
                    ["When", "[before/ after/ async/ display]", "when"],
                    ["Order", "(integer)", "order"],
                    ["Insert", boolean, "action_insert"],
                    ["Update", boolean, "action_update"],
                    ["Delete", boolean, "action_delete"],
                    ["Query", boolean, "action_query"],
                    # FILTER CONDITIONS
                    # ROLE CONDITIONS
                    "Actions",
                    ["Set field values", "(use ServiceNow template language)", "template"],
                    ["Add message", boolean, "add_message"],
                    ["Abort action", boolean, "abort_action"],
                    "Advanced",
                    ["Condition", "", "condition"]
                ]

        if record_name is None:
            return
        
        # create storage folder
        self.create_record_folder(record_type, record_name)

        # create scripts files
        if len(scripts_list) > 0:
            for row in scripts_list:
                string_data = fix_newline_signs(result_data[row[0]])
                data = [record_type, record_name, row[1], string_data]
                self.override_record_file(data)

        # create data file
        if len(fields_list) > 0:
            file_content = generate_standard_data_file_content(result_data, fields_list)
            data = [record_type, record_name, self.standard_paths['file_standard_file'], file_content]
            self.override_record_file(data)

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
    def exit_all(self):
        self.push_output("Exiting program", typ="pretty_text")
        sleep(0.05)
        self.general_data['running'] = False
        return

    def push_unknown_command(self, command):
        self.push_output("Unknown command: " + command)
        return