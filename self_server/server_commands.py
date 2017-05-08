from base64 import b64encode
from time import sleep
from os import path, pardir

from commons.find import list_dict_find, list_dict_find_by_name
from commons.prints import pretty_json_print, dict_to_list, generate_standard_data_file_content,\
        fix_newline_signs, generate_hash
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
        confirm = ['yes', 'y', 'true', 't', 'tak']
        reject = ['false', 'f', 'no', 'n', 'nie']
        available_options = confirm + reject
        confirmation = self.get_user_input(string, invalid_message="Give yes/no answer:", options=available_options, typ="commmon_switch")

        # reject deletion
        if confirmation in reject:
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

    def add_files(self, command):
        if self.settings == {}:
            self.push_output(self.no_settings_defined)
            return

        # known types
            # general
        business_rule = ["business rule", "business_rule", "businessrule", "br", "business"]
        data_policy = ["data policy", "data_policy", "datapolicy", "dp", "data"]
        script_include = ["script include", "script_include", "scriptinclude", "si", "include"]
        client_script = ["client script", "client_script", "clientscript", "cs", "client"]
            # System UI
        ui_policy = ["ui policy", "ui_policy", "uipolicy", "user interface policy",
                "user_interface_policy", "policy", "ui_pol", "ui pol"]
        ui_action = ["ui action", "ui_action", "uiaction", "user interface action",
                "user_interface_action", "action", "ui"]
        ui_page = ["ui page", "ui_page", "uipage", "user interface page", "user_interface_page",
                "page", "ui_pag", "ui pag"]
        ui_macro = ["ui macro", "ui_macro", "uimacro", "user interface macro", "user_interface_macro",
                "macro", "ui_mac", "ui mac"]
        ui_script = ["ui script", "ui_script", "uiscript", "user interface script",
                "user_interface_script", "script", "ui_sc", "ui sc"]
        ui_context_menu = ["ui context menu", "ui_context_menu", "uicontextmenu",
                "user interface context menu", "user_interface_context_menu", "context menu",
                "context_menu", "ui_cm", "ui cm"]
            # Service Catalog
        catalog_ui_policy = ["catalog ui policy", "catalog_ui_policy", "cat ui policy", "cat_ui_policy",
                "catalog user interface policy", "catalog_user_interface_policy", "catalog policy",
                "catalog_policy", "cat_ui_pol", "cat ui pol", "cataloguipolicy"]
        catalog_client_script = ["catalog client script", "catalog_client_script", "catalogclientscript",
                "cat cs", "cat_cs", "cat client", "cat_client", "catalog client", "catalog_client"]
            # Other
        custom = ["custom", "custom file", "custom_file", "customfile", "user defined", "user_defined", "userdefined"]

        all_options = business_rule + data_policy + script_include + client_script
        all_options += ui_policy + ui_action + ui_page + ui_macro + ui_script + ui_context_menu
        all_options += catalog_ui_policy + catalog_client_script + custom

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

        # table
        table = None

        if found_type in custom:
            table = self.get_user_input("Table name of the record:", typ="case_sensitive")
            if table is None:
                return
        elif found_type in business_rule:
            table = "sys_script"
        elif found_type in data_policy:
            table = "sys_data_policy2"
        elif found_type in script_include:
            table = "sys_script_include"
        elif found_type in client_script:
            table = "sys_script_client"
        elif found_type in ui_policy:
            table = "sys_ui_policy"
        elif found_type in ui_action:
            table = "sys_ui_action"
        elif found_type in ui_page:
            table = "sys_ui_page"
        elif found_type in ui_macro:
            table = "sys_ui_macro"
        elif found_type in ui_script:
            table = "sys_ui_script"
        elif found_type in ui_context_menu:
            table = "sys_ui_context_menu"
        elif found_type in catalog_ui_policy:
            table = "catalog_ui_policy"
        elif found_type in catalog_client_script:
            table = "catalog_script_client"

        # sys_id
        sys_id = self.get_user_input("Record sys_id:")
        if sys_id is None:
            return

        # downloaded data
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
        saved_hashes = []
            # list of saved hashes of files (just to check if the files were modified)
                # [field, file, hash]

        # information to save
        record_name = None
        record_type = None

        # commonly used values
        comment_boolean = "[true/false]"
        comment_read_only = "(read only!)"
        comment_integer = "(integer)"

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
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Table", "", "collection"],
                    ["Active", comment_boolean, "", "active"],
                    ["Advanced", comment_boolean, "", "advanced"],
                    "When to run",
                    ["When", "[before/ after/ async/ display]", "", "when"],
                    ["Order", comment_integer, "", "order"],
                    ["Insert", comment_boolean, "", "action_insert"],
                    ["Update", comment_boolean, "", "action_update"],
                    ["Delete", comment_boolean, "", "action_delete"],
                    ["Query", comment_boolean, "", "action_query"],
                    # FILTER CONDITIONS
                    # ROLE CONDITIONS
                    "Actions",
                    ["Set field values", "(use ServiceNow template language)", "", "template"],
                    ["Add message", comment_boolean, "", "add_message"],
                    ["Abort action", comment_boolean, "", "abort_action"],
                    "Advanced",
                    ["Condition", "", "condition"]
                ]
        elif found_type in data_policy:
            record_type = self.standard_paths['files_data_policy']
            record_name = result_data['sys_name']
            scripts_list = [
                    ["description", "description.txt"]
                ]
            fields_list = [
                    "Basic",
                    ["Table", "", "model_table"],
                    ["Inherit", comment_boolean, "", "inherit"],
                    ["Reverse if false", comment_boolean, "", "reverse_if_false"],
                    ["Active", comment_boolean, "", "active"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Apply to import sets", comment_boolean, "", "apply_import_set"],
                    ["Apply to SOAP", comment_boolean, "", "apply_soap"],
                    ["Use as UI Policy on client", comment_boolean, "", "enforce_ui"],
                    ["Short description", "", "short_description"]
                    # CONDITIONS?
                ]
        elif found_type in script_include:
            record_type = self.standard_paths['files_script_include']
            record_name = result_data['name']
            scripts_list = [
                    ["description", "description.txt"],
                    ["script", "script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["API Name", comment_read_only, "", "api_name"],
                    ["Client callable", comment_boolean, "", "client_callable"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Accessible from", "[public / package_private]", "", "access"],
                    ["Active", comment_boolean, "", "active"],
                    ["Protection policy", comment_read_only, "", "sys_policy"]
                ]
        elif found_type in client_script:
            record_type = self.standard_paths['files_client_script']
            record_name = result_data['name']
            scripts_list = [
                    ["description", "description.txt"],
                    ["messages", "messages.txt"],
                    ["script", "script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Table", "", "table"],
                    ["UI Type", "[0-Desktop, 1-Mobile, 10-Both]", "", "ui_type"],
                    ["Type", "[onCellEdit / onChange / onLoad / onSubmit]", "", "type"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Active", comment_boolean, "", "active"],
                    ["Inherited", comment_boolean, "", "applies_extended"],
                    ["Global", comment_boolean, "", "global"]
                ]
        elif found_type in ui_policy:
            record_type = self.standard_paths['files_ui_policy']
            record_name = result_data['short_description']
            scripts_list = [
                    ["script_false", "script_if_false.js"],
                    ["script_true", "script_if_true.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Table", "", "table"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Active", comment_boolean, "", "active"],
                    ["Short description", "", "short_description"],
                    ["Order", comment_integer, "", "order"],
                    "When to Apply",
                    # CONDITIONS
                    ["Global", comment_boolean, "", "global"],
                    ["On load", comment_boolean, "", "on_load"],
                    ["Reverse if false", comment_boolean, "", "reverse_if_false"],
                    ["Ingerit", comment_boolean, "", "inherit"],
                    "Script",
                    ["Run scripts", comment_boolean, "", "run_scripts"]

                ]
        elif found_type in ui_action:
            record_type = self.standard_paths['files_ui_action']
            record_name = result_data['name']
            scripts_list = [
                    ["comments", "comments.txt"],
                    ["script", "script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Table", "", "table"],
                    ["Order", comment_integer, "", "order"],
                    ["Action name", "", "action_name"],
                    ["Active", comment_boolean, "", "active"],
                    ["Show insert", comment_boolean, "", "show_insert"],
                    ["Show update", comment_boolean, "", "show_update"],
                    ["UI11 Compatibile", comment_boolean, "", "ui11_compatible"],
                    ["UI16 Compatibile", comment_boolean, "", "ui16_compatible"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Form button", comment_boolean, "", "form_button"],
                    ["Form context menu", comment_boolean, "", "form_context_menu"],
                    ["Form link", comment_boolean, "", "form_link"],
                    ["List banner button", comment_boolean, "", "list_banner_button"],
                    ["List bottom button", comment_boolean, "", "list_button"],
                    ["List context menu", comment_boolean, "", "list_context_menu"],
                    ["List choice", comment_boolean, "", "list_choice"],
                    ["List link", comment_boolean, "", "list_link"],
                    ["Hint", "", "hint"],
                    ["Onclick", "", "onclick"],
                    ["Condition", "", "condition"],
                    ["Protection policy", comment_read_only, "", "sys_policy"]
                ]
        elif found_type in ui_page:
            record_type = self.standard_paths['files_ui_page']
            record_name = result_data['name']
            scripts_list = [
                    ["html", "html.jelly"],
                    ["client_script", "client_script.js"],
                    ["processing_script", "processing_script.js"],
                    ["description", "description.txt"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Category", "[cms/ general/ homepages/ htmleditor/ kb/ catalog]", "", "category"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Direct", comment_boolean, "", "direct"],
                    ["Prtection policy", comment_read_only, "", "sys_policy"]
                ]
        elif found_type in ui_macro:
            record_type = self.standard_paths['files_ui_macro']
            record_name = result_data['name']
            scripts_list = [
                    ["description", "description.txt"],
                    ["xml", "xml.jelly"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Active", comment_boolean, "", "active"],
                    ["Protection policy", "", "sys_policy"]
                ]
        elif found_type in ui_script:
            record_type = self.standard_paths['files_ui_script']
            record_name = result_data['name']
            scripts_list = [
                    ["description", "description.txt"],
                    ["script", "script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Global", comment_boolean, "", "global"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Active", comment_boolean, "", "active"]
                ]
        elif found_type in ui_context_menu:
            record_type = self.standard_paths['files_ui_context_menu']
            record_name = result_data['name']
            scripts_list = [
                    ["action_script", "action_script.js"],
                    ["on_show_script", "onshow_script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Table", "", "table"],
                    ["Menu", "[list_title/ list_header/ list_row]", "", "menu"],
                    ["Type", "[action/ menu/ line/ label/ dynamic]", "", "type"],
                    ["Name", "", "name"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Parent", "", "parent"],
                    ["Odred", comment_integer, "", "order"],
                    ["Active", comment_boolean, "", "active"],
                    ["Run onShow script", comment_boolean, "", "run_on_show_script"],
                    ["Condition", "", "condition"]
                ]
        elif found_type in catalog_ui_policy:
            record_type = self.standard_paths['files_catalog_ui_policy']
            record_name = result_data['short_description']
            scripts_list = [
                    ["script_false", "script_if_false.js"],
                    ["script_true", "script_if_true.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Applies to", "[item / set]", "applies_to"],
                    ["Catalog item", "", "catalog_item.value"],
                    ["Short description", "", "short_description"],
                    ["Active", comment_boolean, "", "active"],
                    "When to Apply",
                    # CATALOG CONDITIONS
                    ["Applies on Catalog Item view", comment_boolean, "", "applies_catalog"],
                    ["Applies on Catalog Tasks", comment_boolean, "", "applies_sc_task"],
                    ["Applies on Requested Items", comment_boolean, "", "applies_req_item"],
                    ["On load", comment_boolean, "", "on_load"],
                    ["Reverse if false", comment_boolean, "", "reverse_if_false"],
                    "Script",
                    ["Run scripts", comment_boolean, "", "run_scripts"]
                ]
        elif found_type in catalog_client_script:
            record_type = self.standard_paths['files_catalog_client_script']
            record_name = result_data['name']
            scripts_list = [
                    ["script", "script.js"]
                ]
            fields_list = [
                    "Basic",
                    ["Name", "", "name"],
                    ["Applies to", "[item - Catalog Item/ set - Variable Set]", "", "applies_to"],
                    ["Active", comment_boolean, "", "active"],
                    ["UI Type", "[0 - Desktop/ 1 - Mobile/ 10 - Both]", "", "ui_type"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Type", "[onCellEdit/ onChange/ onLoad/ onSubmit]", "", "type"],
                    ["Catalog item", "(sys_id)", "", "cat_item.value"],
                    ["Variable name", "", "cat_variable"],
                    ["Applies on Catalog Item view", comment_boolean, "", "applies_catalog"],
                    ["Applies on Requested Items", comment_boolean, "", "applies_req_item"],
                    ["Applies on Catalog Task", comment_boolean, "", "applies_sc_task"]
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
    def exit_all(self):
        self.exit_silence = True
        self.push_output("Exiting program", typ="pretty_text")
        sleep(0.05)
        self.general_data['running'] = False
        return

    def push_unknown_command(self, command):
        self.push_output("Unknown command: " + command)
        self.exit_silence = True
        return