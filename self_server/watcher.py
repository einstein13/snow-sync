from time import sleep, time
from threading import Thread

from commons.find import list_dict_find_by_name

class Watcher(object):

    def watcher_recalculate_pull_timediff(self, last_pull_time):
        watcher = self.general_data['watcher']
        minimal = watcher['timediff_minimal']
        current = watcher['timediff_multiplier'] * last_pull_time
        watcher['timediff_pull'] = max(minimal, current)
        return

    def watcher_push_files(self, list_of_changes):
        changes = 0
        files_list = self.get_settings_files_list()
        for record in list_of_changes[:-1]:
            if record[0] == self.file_status_names['changed']:
                file_data = list_dict_find_by_name(files_list, record[1]['name'])[1]
                file_data = self.get_files_content(file_data)
                self.push_one_file(file_data)
                text = "File \"%s\" (%s) pushed automaticly" % (file_data['name'], file_data['type'])
                self.push_output(text, typ="inset")
                changes += 1
        if changes != list_of_changes[-1][0]:
            self.push_output("Error during automatic push occured", typ="pretty_text")
        self.general_data['watcher']['last_push'] = time()
        return

    def watcher_pull_files(self):
        text = "Warning! Pull request in progress."
        self.push_output(text, typ="inset")
        text = "Unpushed changes can be erased."
        self.push_output(text, typ="inset")

        # pull all files
        T0 = time()
        self.pull_all_files_core()

        # save timestamp
        T1 = time()
        self.general_data['watcher']['last_pull'] = T1

        # finish
        text = "Pull request finished (took %.1f seconds)." % (T1 - T0)
        self.push_output(text, typ="inset")
        self.watcher_recalculate_pull_timediff(T1 - T0)
        return

    def watcher_initialize(self):
        self.push_output("Initializing watcher", typ="inset")
        list_of_changes = self.list_files_changes()
        self.watcher_push_files(list_of_changes)
        self.watcher_pull_files()
        self.push_output("Initializing finished", typ="inset")
        return

    def watcher_watch(self):
        self.watcher_initialize()
        watcher = self.general_data['watcher']
        while watcher['running']:
            # check if there are updates on the disk
            list_of_changes = self.list_files_changes()
            # if yes - push them
            if list_of_changes[-1][0] > 0:
                self.watcher_push_files(list_of_changes)

            # check if pull should be done
            if time() - watcher['last_pull'] > watcher['timediff_pull']:
                # if yes - pull
                self.watcher_pull_files()

            sleep(watcher['sleep_time'])

        self.push_output("stopped watching", typ="inset")
        return None
    
    def watcher_start_watch(self):
        thread = Thread(target = self.watcher_watch)
        thread.start()
        return