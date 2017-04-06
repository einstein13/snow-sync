from os import path, pardir

class FileSystem(object):
    
    def get_project_path(self):
        basic_folder_name = "snow-sync"
        file_path = path.abspath(__file__)
        folder_path = file_path
        while not folder_path.endswith(basic_folder_name):
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
        folder_path = path.abspath(path.join(folder_path, pardir))
        return folder_path

