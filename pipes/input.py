from time import sleep

from commons.threads import ThreadCommons
from .getch import getch

class Input(ThreadCommons):

    input_command = ''

    def __init__(self, inp, out, gen_dat):
        super(Input, self).__init__(inp, out, gen_dat)
        self.input_command = ''
        return

    def scan(self):
        inp = getch()
        # special characters: F1-F12, Arrows
        if ord(inp) in (224, 0):
            # print("SPECIAL sign")
            inp1 = inp
            inp2 = self.scan()
            # TO DO: what with those signs?
            return None
        # standard keyboard sign
        try:
            return inp.decode("utf-8")
        except:
            pass

        print("ERROR parsing the sign [%s]" % ord(inp))
        return None

    def run_thread(self):
        while self.general_data['running']:
            sign = self.scan()
            if sign is None:
                continue
            # self.output_queue.append(str(ord(sign)))
            # self.output_queue.append(sign)
            if len(sign) == 1:
                # print(ord(sign))
                if ord(sign) == 13: # Enter
                    self.general_data['server_queue'].append(self.input_command)
                    self.output_queue.append({'message': '\n', 'type': 'command_sign'})
                    self.output_queue.append({'message': self.input_command, 'type': 'full_command'})
                    self.input_command = ''
                elif ord(sign) == 9: # Tab
                    # TO DO!
                    continue
                elif ord(sign) == 27: # Esc
                    if input_command == '':
                        self.general_data['server_queue'].append('abort_current')
                    else:
                        self.output_queue.append({'message': chr(8)*len(self.input_command), 'type': 'abort_command'})
                        self.input_command = ''
                    continue
                elif ord(sign) == 8: # Backspace
                    if len(self.input_command) == 1:
                        self.output_queue.append({'message': chr(8), 'type': 'abort_command'})
                        self.input_command = ''
                    elif len(self.input_command) > 1:
                        self.input_command = self.input_command[:-1]
                        self.output_queue.append({'message': chr(8), 'type': 'command_sign'})
                    continue
                else:
                    self.input_command += sign
                    self.output_queue.append({'message': sign, 'type': 'command_sign'})
                # print(self.output_queue)
            else:
                sleep(0.01)
        return

