from threading import Thread
from time import sleep

class Output(object):
        
    def __init__(self, inp, out, gen_dat):
        super(Output, self).__init__()
        self.input_queue = inp
        self.output_queue = out
        self.general_data = gen_dat
        return

    def print(self, text, end="\n"):
        if type(text) is str:
            print(text, end=end)
        return

    def run_thread(self):
        while self.general_data['running']:
            if len(self.output_queue) > 0:
                print_data = self.output_queue.pop(0)
                self.print(print_data)
            else:
                sleep(0.01)
        self.print("writing thread closed")
        return

    def run(self):
        thread = Thread(target = self.run_thread)
        thread.start()
        return