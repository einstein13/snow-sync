import sys

from time import sleep

from commons.threads import ThreadCommons

class DataPrint(object):

    input_command = ''

    def print(self, text, begin='', end="\n"):
        if type(text) is str:
            print(begin + text, end=end)
        else:
            try:
                print(begin + str(text), end=end)
            except:
                print("Unable to print data")
        sys.stdout.flush()
        return

    def print_data(self, data):
        if type(data) is str:
            self.print(data)
        elif type(data) is dict:
            if data['type'] is 'text':
                self.print(data['message'])
            if data['type'] is 'sign':
                self.print(data['message'], end='')
            if data['type'] is 'full_command':
                self.print(data['message'], begin='\n')
        else:
            self.print(data)
        return


class Output(ThreadCommons, DataPrint):

    def __init__(self, inp, out, gen_dat):
        super(Output, self).__init__(inp, out, gen_dat)
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