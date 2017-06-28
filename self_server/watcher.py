from time import sleep
from threading import Thread

class Watcher(object):

    def watcher_watch(self):
        watcher = self.general_data['watcher']
        while watcher['running']:
            # check if there are updates on the disk

            # if yes - push them

            # check if pull should be done

            # if yes - pull


            sleep(watcher['sleep_time'])
        
        self.push_output("stopped watching", typ="inset")
        return None
    
    def watcher_start_watch(self):
        thread = Thread(target = self.watcher_watch)
        thread.start()
        return