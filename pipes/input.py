from threading import Thread
from time import sleep

from .getch import getch

class Input(object):

    input_command = ''

    def __init__(self, inp, out, gen_dat):
        super(Input, self).__init__()
        self.input_queue = inp
        self.output_queue = out
        self.general_data = gen_dat
        self.input_command = ''
        return

    def scan(self):
        inp = getch()
        # special characters: F1-F12, Arrows
        if ord(inp) in (224, 0):
            print("SPECIAL sign")
            return self.scan()
        # standard keyboard sign
        try:
            return inp.decode("utf-8")
        except:
            pass

        print("ERROR parsing the sign [%s]" % ord())
        return "E"



        inp = getch()
        print("[%s]"%ord(inp),end="")
        if ord(inp) in (224, 0):
            x = self.scan()
            return b"UNKNOWN"
        try:
            sign = inp.decode("utf-8")
            print(sign)
            return sign
        except:
            print("ERROR")
        # self.input_command += inp.decode("utf-8")
        return inp

    def run_thread(self):
        from random import randint
        while self.general_data['running']:
            sign = self.scan()
            # self.output_queue.append(str(ord(sign)))
            # self.output_queue.append(sign)
            print(sign)
            if len(sign) == 1 and ord(sign) == 69:
                self.general_data['server_queue'].append('exit_all')
            else:
                sleep(0.01)
        return

    def run(self):
        thread = Thread(target = self.run_thread)
        thread.start()
        return thread

