from threading import Thread
from time import sleep

class Input(object):

    def __init__(self, inp, out, gen_dat):
        super(Input, self).__init__()
        self.input_queue = inp
        self.output_queue = out
        self.general_data = gen_dat
        return

    def scan(self):
        inp = input('')
        self.input_queue.append(inp)
        return inp

    def run_thread(self):
        from random import randint
        while self.general_data['running']:
            if len(self.input_queue['requests']) >= 0:
                # inp = input()
                x = randint(1,1000)
                inp2 = False
                if x < 20:
                    inp = 'exit ' + str(x)
                    inp2 = True
                else:
                    inp = str(x)
                self.output_queue.append(inp)
                if inp2:
                    sleep(0.5)
                    self.general_data['running'] = False
            else:
                sleep(0.03)
        return

    def run(self):
        thread = Thread(target = self.run_thread)
        thread.start()
        return

