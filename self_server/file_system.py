from json import loads
from os import path, pardir, makedirs
from shutil import rmtree

class FileSystem(object):

    standard_paths = {
        "settings_folder": "settings",
        "files_list": "files.json",
        "servers_list": "servers.json",
        "projects_home": "projects"
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

    # initialize program enviroment
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
        if path.isdir(project_path):
            return
        makedirs(project_path)
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
