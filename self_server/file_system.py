from os import path, pardir

class FileSystem(object):
    
    def get_project_path(self):
        basic_folder_name = "snow-sync"
        file_path = path.abspath(__file__)
        folder_path = file_path
        while not folder_path.endswith(basic_folder_name):
            old_path = folder_path
            folder_path = path.join(folder_path, pardir)
            if old_path == folder_path:
                self.output_queue.append({'type': 'text', 'message': 'There was a problem with recognizing the path'})
                return None
        return folder_path

    def get_parent_project_path(self):
        project_path = self.get_project_path()
        if project_path is None:
            return None
        folder_path = path.join(folder_path, pardir)
        return folder_path

    def override_servers_file(self):
        project_path = self.get_project_path()
        file_path = path.join(project_path, "settings")
        file_path = path.join(file_path, "servers.json")
        print(file_path)
        # file_path = file_path.replace("\\","/")
        # print(file_path)
        file = open(file_path, "r")
        print(file.read())
        file.close()
        return

    def get_settings_folder(self):
        if self.settings == {}:
            return None
        settings_path = self.get_project_path()
        print(path.isdir(settings_path))
        print(path.exists(settings_path))
        settings_path = path.join(settings_path, "settings")
        print(path.isdir(settings_path))
        print(path.exists(settings_path))
        settings_path = path.join(settings_path, self.settings['name'])
        print(path.isdir(settings_path))
        print(path.exists(settings_path))
        return settings_path
