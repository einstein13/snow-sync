from threading import Thread
from time import sleep

class DataPrint(object):

    input_command = ''

    def print(self, text, end="\n"):
        if type(text) is str:
            print(text, end=end)
        else:
            try:
                print(str(text), end=end)
            except:
                print("Unable to print data")
        return

    def print_data(self, data):
        if type(data) is str:
            self.print(data)
        elif type(data) is dict:
            if data['type'] is 'text':
                self.print(data['message'])
        else:
            self.print(data)
        return


class Output(DataPrint):

    def __init__(self, inp, out, gen_dat):
        super(Output, self).__init__()
        self.input_queue = inp
        self.output_queue = out
        self.general_data = gen_dat
        self.input_command = ''
        return

    def run_thread(self):
        while self.general_data['running']:
            if len(self.output_queue) > 0:
                data = self.output_queue.pop(0)
                self.print_data(data)
            else:
                sleep(0.01)
        self.print("writing thread closed")
        return

    def run(self):
        thread = Thread(target = self.run_thread)
        thread.start()
        return thread