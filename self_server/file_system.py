from json import loads
from os import path, pardir, makedirs
from shutil import rmtree

class FileSystem(object):

    standard_paths = {
        "settings_folder": "settings",
        "files_list": "files.json",
        "servers_list": "servers.json",
        "projects_home": "projects",
        # folders
        "files_business_rule": "business_rule",
        "files_script_include": "script_include",
        "files_ui_policy": "ui_policy",
        "files_ui_action": "ui_action",
        "files_data_policy": "data_policy",
        "files_client_script": "client_script",
        "files_custom": "custom",
        "file_standard_file": "row_data.data"
        }
    
    # paths
    def get_project_path(self):
        basic_folder_names = ["snow-sync", "snow-sync-master"]
        file_path = path.abspath(__file__)
        folder_path = file_path
        while len(folder_path.split("\\")) > 0 and \
                    folder_path.split("\\")[-1] not in basic_folder_names:
            old_path = folder_path
            folder_path = path.abspath(path.join(folder_path, pardir))
            if old_path == folder_path:
                self.output_queue.append({'type': 'text', 'message': 'There was a problem with recognizing the path'})
                return None
        return folder_path

    def get_parent_project_path(self):
        project_path = self.get_project_path()
        if project_path is None:
            return None
        folder_path = path.abspath(path.join(project_path, pardir))
        return folder_path

    def get_settings_folder_path(self, name):
        project_path = self.get_project_path()
        folder_path = path.join(project_path, self.standard_paths['settings_folder'])
        folder_path = path.join(folder_path, name)
        return folder_path

    def get_files_folder_path(self, name=None):
        parent_path = self.get_parent_project_path()
        parent_path = path.join(parent_path, self.standard_paths['projects_home'])

        looking_name = name
        if looking_name is None:
            looking_name = self.settings['name']

        files_folder_path = path.join(parent_path, looking_name)
        return files_folder_path

    # initialize program enviroment
    def create_if_not_exist(self, test_path):
        if path.isdir(test_path):
            return
        makedirs(test_path)
        return

    def initialize_servers_json(self):
        project_path = self.get_project_path()
        file_path = path.join(project_path, self.standard_paths['settings_folder'])
        file_path = path.join(file_path, self.standard_paths['servers_list'])

        if not path.exists(file_path):
            file = open(file_path, "w")
            file.write("[\n]")
            file.close()
        return

    def initialize_projects_home(self):
        project_path = self.get_parent_project_path()
        project_path = path.join(project_path, self.standard_paths['projects_home'])
        self.create_if_not_exist(project_path)
        return

    def initialize_files_type_folder(self, files_type_path):
        parent_path = self.get_files_folder_path()
        new_path = path.join(parent_path, files_type_path)
        self.create_if_not_exist(new_path)
        return

    def initialize_files_folder(self, name=None):
        parent_path = self.get_files_folder_path(name=name)
        # main folder
        self.create_if_not_exist(parent_path)
            # # Business Rule
            # new_path = path.join(parent_path, self.standard_paths['files_business_rule'])
            # self.create_if_not_exist(new_path)
            # # Script Include
            # new_path = path.join(parent_path, self.standard_paths['files_script_include'])
            # self.create_if_not_exist(new_path)
            # # UI Policy
            # new_path = path.join(parent_path, self.standard_paths['files_ui_policy'])
            # self.create_if_not_exist(new_path)
            # # UI Action
            # new_path = path.join(parent_path, self.standard_paths['files_ui_action'])
            # self.create_if_not_exist(new_path)
            # # Data Policy
            # new_path = path.join(parent_path, self.standard_paths['files_data_policy'])
            # self.create_if_not_exist(new_path)
            # # Client Script
            # new_path = path.join(parent_path, self.standard_paths['files_client_script'])
            # self.create_if_not_exist(new_path)
            # # Custom folder
            # new_path = path.join(parent_path, self.standard_paths['files_custom'])
            # self.create_if_not_exist(new_path)
        return

    # all servers file
    def override_servers_settings_file(self, string_data):
        project_path = self.get_project_path()
        file_path = path.join(project_path, self.standard_paths['settings_folder'])
        file_path = path.join(file_path, self.standard_paths['servers_list'])
        file = open(file_path, "w")
        file.write(string_data)
        file.close()
        return

    # server folder & files
    def create_settings_folder(self, name):
        folder_path = self.get_settings_folder_path(name)
        file_path = path.join(folder_path, self.standard_paths['files_list'])
        try:
            makedirs(folder_path)
            file = open(file_path, "w")
            file.write("[\n]")
            file.close()
        except:
            self.push_output("There was a problem with creating settings path")
        return

    def get_settings_files_list(self):
        # get file path
        folder_path = self.get_settings_folder_path(self.settings['name'])
        file_path = path.join(folder_path, self.standard_paths['files_list'])
        # open file
        file = open(file_path, "r")
        json_text = file.read()
        file.close()
        # put content into a list
        files_list = loads(json_text)
        # return result
        return files_list

    def remove_settings_folder(self, name):
        project_path = self.get_project_path()
        folder_path = path.join(project_path, self.standard_paths['settings_folder'])
        folder_path = path.join(folder_path, name)
        try:
            rmtree(folder_path)
        except:
            self.push_output("There was a problem with deleting saved data")
        return

    def get_settings_folder(self):
        # TO DO?
        if self.settings == {}:
            return None
        settings_path = self.get_project_path()
        print(path.isdir(settings_path))
        print(path.exists(settings_path))
        settings_path = path.join(settings_path, self.standard_paths['settings_folder'])
        print(path.isdir(settings_path))
        print(path.exists(settings_path))
        settings_path = path.join(settings_path, self.settings['name'])
        print(path.isdir(settings_path))
        print(path.exists(settings_path))
        return settings_path

    def create_record_folder(self, typ, record_name):
        # initialize folder, if not exist:
        self.initialize_files_type_folder(typ)
        # create folder
        parent_path = self.get_files_folder_path() # from self.settings
        new_path = path.join(parent_path, typ)
        new_path = path.join(new_path, record_name)
        self.create_if_not_exist(new_path)
        return

    def override_record_file(self, file_data):
        # file_data - all needed data:
            # [0] - row type (business rule/ ui script/ ... / custom)
            # [1] - row name (name of the record in the database)
            # [2] - file name on disk (script name or standard row data)
            # [3] - file content
        parent_path = self.get_files_folder_path()
        new_path = path.join(parent_path, file_data[0])
        new_path = path.join(new_path, file_data[1])
        new_path = path.join(new_path, file_data[2])
        file = open(new_path, "w")
        file.write(file_data[3])
        file.close()
        return