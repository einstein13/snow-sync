import sys

from time import sleep

from commons.threads import ThreadCommons
from commons.prints import pretty_json_print

class DataPrint(object):

    input_command = ''
    flags = {
        'input_command_writing': False, # the command is being writing
        'input_command_interrupted': False # the command finnished
        }

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

    def pretty_print(self, text):
        prettiness = "* * * * * * * * * * * * * * * * * * * *"
        self.print(prettiness, begin="\n")
        self.print(text)
        self.print(prettiness, end="\n\n")
        return

    def clean_comand_line(self, length):
        self.print(chr(8)*length, end="")
        if not self.flags['input_command_interrupted']:
            self.print(" "*length, end="")
            self.print(chr(8)*length, end="")
        return

    def abort_command(self, text):
        # command was interrupted - some characters are in other part of command line
        if self.flags['input_command_interrupted']:
            self.flags['input_command_writing'] = False
            self.flags['input_command_interrupted'] = False
            self.print("\n", end="")
            return
        # command wasn't interrupted
        self.clean_comand_line(len(text))
        self.flags['input_command_writing'] = False
        return

    def write_command_sign(self, text):
        # the sign is a Backspace
        if text == chr(8):
            self.clean_comand_line(1)
            return
        self.flags['input_command_writing'] = True
        self.print(text, end="")
        return

    def write_full_command(self, text):
        # command wasn't written at all
        if not self.flags['input_command_writing']:
            self.print(text)
            self.flags['input_command_interrupted'] = False
            return
        # command was interrupted when writing
        if self.flags['input_command_interrupted']:
            self.print(text, begin="\n")
            self.flags['input_command_interrupted'] = False
            self.flags['input_command_writing'] = False
            return
        # command wasn't interrupted and was writing
        self.flags['input_command_writing'] = False
        return

    def table_print(self, data):
        # length of columns
        lengths = [0] * len(data[0])
        for itr1 in range(len(data)):
            row = data[itr1]
            for itr2 in range(len(row)):
                if len(row[itr2]) > lengths[itr2]:
                    lengths[itr2] = len(row[itr2])
        for itr1 in range(len(lengths)):
            lengths[itr1] += 2

        # print header
        line_to_print = "┌" + "─" * (lengths[0])
        for itr1 in range(1, len(lengths)):
            line_to_print += "┬" + "─" * (lengths[itr1])
        line_to_print += "┐"
        self.print(line_to_print)

        line_to_print = ""
        for itr1 in range(len(lengths)):
            element = data[0][itr1]
            additional_spaces = (lengths[itr1] - len(element) -1)
            line_to_print += "│ " + element + " " * additional_spaces
        line_to_print += "│"
        self.print(line_to_print)

        line_to_print = "├" + "─" * (lengths[0])
        for itr1 in range(1, len(lengths)):
            line_to_print += "┼" + "─" * (lengths[itr1])
        line_to_print += "┤"
        self.print(line_to_print)

        # print body
        line_to_print = ""
        for itr1 in range(1, len(data)):
            row = data[itr1]
            for itr2 in range(len(row)):
                element = row[itr2]
                additional_spaces = (lengths[itr2] - len(element) -1)
                line_to_print += "│ " + element + " " * additional_spaces
            line_to_print += "│"
            self.print(line_to_print)

        # end table
        line_to_print = "└" + "─" * (lengths[0])
        for itr1 in range(1, len(lengths)):
            line_to_print += "┴" + "─" * (lengths[itr1])
        line_to_print += "┘"
        self.print(line_to_print)

        return

    def json_print(self, data):
        result = pretty_json_print(data)
        self.print(result)
        return

    def print_data(self, data):
        if type(data) is str:
            self.print(data)
        elif type(data) is dict:
            if data['type'] is 'text':
                self.print(data['message'])
            elif data['type'] is 'command_sign':
                self.write_command_sign(data['message'])
            elif data['type'] is 'full_command':
                self.write_full_command(data['message'])
            elif data['type'] is 'abort_command':
                self.abort_command(data['message'])
            elif data['type'] is 'pretty_text':
                self.pretty_print(data['message'])
            elif data['type'] is 'table':
                self.table_print(data['message'])
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
        # self.print("writing thread closed")
        return