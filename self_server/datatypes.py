

class ContentDatabase(object):
    # commonly used values
    comment_boolean = "[true/false]"
    comment_read_only = "(read only!)"
    comment_integer = "(integer)"

    database = [
        # Standard scripts
        {
            "name": "Business Rule",
            "aliases": ["business rule", "business_rule", "businessrule", "br", "business"],
            "table": "sys_script",
            "standard_path_name": "files_business_rule",
            "record_name": "name",
            "scripts_list": [
                    ["script", "script.js"]
                ],
            "fields_list": [
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
        },
        {
            "name": "Data Policy",
            "aliases": ["data policy", "data_policy", "datapolicy", "dp", "data"],
            "table": "sys_data_policy2",
            "standard_path_name": "files_data_policy",
            "record_name": "sys_name",
            "scripts_list": [
                    ["description", "description.txt"]
                ],
            "fields_list": [
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
        },
        {
            "name": "Scrip Include",
            "aliases": ["script include", "script_include", "scriptinclude", "si", "include"],
            "table": "sys_script_include",
            "standard_path_name": "files_script_include",
            "record_name": "name",
            "scripts_list": [
                    ["description", "description.txt"],
                    ["script", "script.js"]
                ],
            "fields_list": [
                    "Basic",
                    ["Name", "", "name"],
                    ["API Name", comment_read_only, "", "api_name"],
                    ["Client callable", comment_boolean, "", "client_callable"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Accessible from", "[public / package_private]", "", "access"],
                    ["Active", comment_boolean, "", "active"],
                    ["Protection policy", comment_read_only, "", "sys_policy"]
                ]
        },
        {
            "name": "Client Script",
            "aliases": ["client script", "client_script", "clientscript", "cs", "client"],
            "table": "sys_script_client",
            "standard_path_name": "files_client_script",
            "record_name": "name",
            "scripts_list": [
                    ["description", "description.txt"],
                    ["messages", "messages.txt"],
                    ["script", "script.js"]
                ],
            "fields_list": [
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
        },
        # UI System
        {
            "name": "UI Policy",
            "aliases": ["ui policy", "ui_policy", "uipolicy", "user interface policy",
                    "user_interface_policy", "policy", "ui_pol", "ui pol"],
            "table": "sys_ui_policy",
            "standard_path_name": "files_ui_policy",
            "record_name": "short_description",
            "scripts_list": [
                    ["script_false", "script_if_false.js"],
                    ["script_true", "script_if_true.js"]
                ],
            "fields_list": [
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
        },
        {
            "name": "UI Action",
            "aliases": ["ui action", "ui_action", "uiaction", "user interface action",
                    "user_interface_action", "action", "ui"],
            "table": "sys_ui_action",
            "standard_path_name": "files_ui_action",
            "record_name": "name",
            "scripts_list": [
                    ["comments", "comments.txt"],
                    ["script", "script.js"]
                ],
            "fields_list": [
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
        },
        {
            "name": "UI Page",
            "aliases": ["ui page", "ui_page", "uipage", "user interface page", "user_interface_page",
                    "page", "ui_pag", "ui pag"],
            "table": "sys_ui_page",
            "standard_path_name": "files_ui_page",
            "record_name": "name",
            "scripts_list": [
                    ["html", "html.jelly"],
                    ["client_script", "client_script.js"],
                    ["processing_script", "processing_script.js"],
                    ["description", "description.txt"]
                ],
            "fields_list": [
                    "Basic",
                    ["Name", "", "name"],
                    ["Category", "[cms/ general/ homepages/ htmleditor/ kb/ catalog]", "", "category"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Direct", comment_boolean, "", "direct"],
                    ["Prtection policy", comment_read_only, "", "sys_policy"]
                ]
        },
        {
            "name": "UI Macro",
            "aliases": ["ui macro", "ui_macro", "uimacro", "user interface macro", "user_interface_macro",
                    "macro", "ui_mac", "ui mac"],
            "table": "sys_ui_macro",
            "standard_path_name": "files_ui_macro",
            "record_name": "name",
            "scripts_list": [
                    ["description", "description.txt"],
                    ["xml", "xml.jelly"]
                ],
            "fields_list": [
                    "Basic",
                    ["Name", "", "name"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Active", comment_boolean, "", "active"],
                    ["Protection policy", "", "sys_policy"]
                ]
        },
        {
            "name": "UI Script",
            "aliases": ["ui script", "ui_script", "uiscript", "user interface script",
                    "user_interface_script", "script", "ui_sc", "ui sc"],
            "table": "sys_ui_script",
            "standard_path_name": "files_ui_script",
            "record_name": "name",
            "scripts_list": [
                    ["description", "description.txt"],
                    ["script", "script.js"]
                ],
            "fields_list": [
                    "Basic",
                    ["Name", "", "name"],
                    ["Global", comment_boolean, "", "global"],
                    ["Application", comment_read_only, "", "sys_scope.value"],
                    ["Active", comment_boolean, "", "active"]
                ]
        },
        {
            "name": "UI Context Menu",
            "aliases": ["ui context menu", "ui_context_menu", "uicontextmenu",
                    "user interface context menu", "user_interface_context_menu",
                    "context menu", "context_menu", "ui_cm", "ui cm"],
            "table": "sys_ui_context_menu",
            "standard_path_name": "files_ui_context_menu",
            "record_name": "name",
            "scripts_list": [
                    ["action_script", "action_script.js"],
                    ["on_show_script", "onshow_script.js"]
                ],
            "fields_list": [
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
        },
        # Service Catalog
        {
            "name": "Catalog UI Policy",
            "aliases": ["catalog ui policy", "catalog_ui_policy", "cat ui policy",
                    "cat_ui_policy", "catalog user interface policy",
                    "catalog_user_interface_policy", "catalog policy",
                    "catalog_policy", "cat_ui_pol", "cat ui pol", "cataloguipolicy"],
            "table": "catalog_ui_policy",
            "standard_path_name": "files_catalog_ui_policy",
            "record_name": "short_description",
            "scripts_list": [
                    ["script_false", "script_if_false.js"],
                    ["script_true", "script_if_true.js"]
                ],
            "fields_list": [
                    "Basic",
                    ["Applies to", "[item / set]", "", "applies_to"],
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
        },
        {
            "name": "Catalog Client Script",
            "aliases": ["catalog client script", "catalog_client_script",
                    "catalogclientscript", "cat cs", "cat_cs", "cat client", "cat_client",
                    "catalog client", "catalog_client"],
            "table": "catalog_script_client",
            "standard_path_name": "files_catalog_client_script",
            "record_name": "name",
            "scripts_list": [
                    ["script", "script.js"]
                ],
            "fields_list": [
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
        },
        # Custom type
        {
            "name": "Custom",
            "aliases": ["custom", "custom file", "custom_file", "customfile", "user defined",
                    "user_defined", "userdefined"],
            "table": "",
            "standard_path_name": "",
            "record_name": "",
            "scripts_list": [
                ],
            "fields_list": [
                ]
        },
        # Other types
        {
            # blank record for new record type
            "name": "EXAMPLE", # name of record type
            "aliases": [], # all (lower case!) names that means "name" above
            "table": "", # table name in the ServiceNow databse
            "standard_path_name": "", # name defined in file_system.py -> class FileSystem -> standard_paths attribute
            "record_name": "", # variable name where record name is
            "scripts_list": [
                    # 2-element lists
                        # first element = variable
                        # second element = file name
                ],
            "fields_list": [
                    # Srtings are for category name
                    # Lists should contain:
                        # Comments as first strings
                        # then blank string ("")
                        # finally all variables for that comment
                ]
        }
    ]

    def check_correctness_of_databse(self):
        # check if it exists and contains something
        full_check = ["name", "aliases", "table", "standard_path_name",
            "record_name"]
        # check those keys for existence only
        key_only_check = ["scripts_list", "fields_list"]
        # don't check those names
        free_records = ["Custom", "EXAMPLE"]

        any_errors = False

        for itr in range(len(self.database)):
            record = self.database[itr]
            keys = record.keys()
            record_name = "/" + str(itr) + "/"
            if "name" in keys and record["name"]:
                record_name = record["name"]
            if record_name in free_records:
                continue

            error = False

            error_string = "No %s defined in the dictionary"

            for name in full_check:
                if not name in keys or not record[name]:
                    print(error_string % name)
                    error = True
            for name in key_only_check:
                if not name in keys:
                    print(error_string % name)
                    error = True

            if not error:
                if name == "scripts_list":
                    for row in record[name]:
                        if len(row) != 2:
                            print("Wrong format of the row: %s" % str(row))
                            error = True
                if name == "fields_list":
                    for row in record[name]:
                        if type(row) is str:
                            continue
                        else:
                            if "" not in row:
                                print("There is no variables in %s row, add blank \"\"" % str(row))
                                error = True
                            if row[0] == "" or row[-1] == "":
                                print("Blank \"\" can't be in the beggining or the end of row %s" % str(row))
                                error = True
                if name == "aliases":
                    aliases = record[name]
                    if len(list(set(aliases))) != len(aliases):
                        print("There are duplicates in aliases: %s" % str(aliases))
                        error = True

            if error:
                print("> There were some errors with %s record" % record_name)
                any_errors = True

        all_aliases = self.get_all_aliases()
        if len(list(set(all_aliases))) != len(all_aliases):
            print("There are duplicates with aliases")
            any_errors = True

        if not any_errors:
            print("ALL checked and correct")
        return

    def find_data_by_alias(self, alias):
        lower = alias.lower()
        for record in self.database:
            if lower in record['aliases']:
                return record
        return {}

    def get_all_aliases(self):
        aliases = []
        for record in self.database:
            aliases += record['aliases']
        while aliases.count("") > 0:
            aliases.remove("")
        return aliases


class CommandRecognizer(object):

    unknown_command = "push_unknown_command"
    splitting_element = [" ", "\t"]

    database = [
        # EXITING
        {
            'command': 'exit_current_command',
            'aliases': ['exit_current_command']
            },
        {
            'command': 'exit_with_prompt',
            'aliases': ['exit_with_prompt']
            },
        {
            'command': 'exit_all',
            'aliases': ['exit', 'exit()', 'quit', 'quit()']
            },
        # HELP
        {
            'command': 'show_help',
            'aliases': ['help', 'man']
            },
        # SETTINGS
        {
            'command': 'show_settings',
            'aliases': ['show_settings', 'show_setting', 'show settings', 'show setting']
            },
        {
            'command': 'add_settings',
            'aliases': ['add_settings', 'add_setting', 'add settings', 'add setting']
            },
        {
            'command': 'edit_settings',
            'aliases': ['edit_settings', 'edit_setting', 'edit settings', 'edit setting']
            },
        {
            'command': 'delete_settings',
            'aliases': ['delete_settings', 'delete_setting', 'delete settings', 'delete setting',
                'remove_settings', 'remove settings', 'remove_settings', 'remove setting']
            },
        {
            'command': 'read_settings',
            'aliases': ['read_settings', 'read_setting', 'read settings', 'read setting']
            },
        # FILES
        {
            'command': 'show_files',
            'aliases': ['show_files', 'show_file', 'show files', 'show file']
            },
        {
            'command': 'add_files',
            'aliases': ['add_files', 'add_file', 'add files', 'add file']
            },
        {
            'command': 'delete_files',
            'aliases': ['delete_files', 'delete_file', 'delete files', 'delete file',
                'remove_files', 'remove files', 'remove_file', 'remove file']
            },
        {
            'command': 'truncate_files',
            'aliases': ['truncate_files', 'truncate_file', 'truncate files', 'truncate file']
            },
        {
            'command': 'pull_all_files',
            'aliases': ['pull', 'pull_all', 'pull all', 'git_pull', 'git pull']
            },
        {
            'command': 'push_all_files',
            'aliases': ['push', 'push_all', 'push all', 'git_push', 'git push']
            },
        {
            'command': 'show_files_status',
            'aliases': ['status', 'show_status', 'show status']
            },
        {
            'command': 'start_watch',
            'aliases': ['watch', 'start watch', 'start_watch', 'start watching', 'start_watching']
            },
        {
            'command': 'stop_watch',
            'aliases': ['unwatch', 'stop watch', 'stop_watch', 'stop watching', 'stop_watching']
            },
        # RECORDS
        {
            'command': 'show_record',
            'aliases': ['show record', 'show_record', 'show records', 'show_records',
                'read record', 'read_record', 'read records', 'read_records']
            },
        # empty for copy
        {
            'command': '',
            'aliases': []
            }
    ]

    def split_command(self, command):
        splitted_0 = [command]
        splitted_1 = []
        for element in self.splitting_element:
            splitted_1 = []
            for part in splitted_0:
                splitted_1 += part.split(element)
            splitted_0 = list(splitted_1)
        # delete empty records
        splitted_1 = []
        for element in splitted_0:
            if element:
                splitted_1.append(element)
        return splitted_1

    def find_command(self, command):
        splitted = self.split_command(command)
        for record in self.database:
            # for each record in database
            for alias in record['aliases']:
                if type(alias) is str and alias.find(" ") > -1: # contains space
                    alias = self.split_command(alias)
                # check pure string
                if type(alias) is str and splitted[0] == alias:
                    return record['command']
                # check string with spaces / lists
                if type(alias) is list:
                    if len(alias) > len(splitted):
                        continue
                    correct = True
                    for itr in range(len(alias)):
                        if alias[itr] != splitted[itr]:
                            correct = False
                            break
                    if correct:
                        return record['command']
        return self.unknown_command

    def find_alias(self, command):
        if command == '':
            return self.unknown_command
        splitted = self.split_command(command)
        for record in self.database:
            # for each record in database
            for alias in record['aliases']:
                new_alias = alias
                if type(new_alias) is str and new_alias.find(" ") > -1: # contains space
                    new_alias = self.split_command(new_alias)
                # check pure string
                if type(new_alias) is str and splitted[0] == new_alias:
                    return alias
                # check string with spaces / lists
                if type(new_alias) is list:
                    correct = True
                    for itr in range(len(new_alias)):
                        if new_alias[itr] != splitted[itr]:
                            correct = False
                            break
                    if correct:
                        if type(alias) is list:
                            return list(alias)
                        else:
                            return alias
        return self.unknown_command

    def cut_command(self, command, alias_list):
        new_command = command
        while len(alias_list) > 0:
            if new_command.startswith(alias_list[0]):
                new_command = new_command[len(alias_list[0]):]
                alias_list.pop(0)
            # cut splitting_element
            while new_command != ''  and new_command[0] in self.splitting_element:
                new_command = new_command[1:]
        return new_command

    def return_command_arguments(self, command):
        alias = self.find_alias(command)

        # cut arguments
        splitted_alias = alias
        if type(splitted_alias) is str:
            splitted_alias = self.split_command(splitted_alias)
        cutted = self.cut_command(command, splitted_alias)

        # prepare for collecting
        if type(alias) is list:
            alias = self.splitting_element[0].join(alias)
        correct_command = self.find_command(alias)
        splitted_arguments = self.split_command(cutted)

        # collect result
        result = []
        result.append(correct_command)
        result.append(cutted)
        result.append(splitted_arguments)

        # return result
        return result

    def return_command(self, command):
        result = "self."
        result += self.find_command(command)
        result += "(command)"
        return result

