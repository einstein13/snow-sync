from time import sleep

from commons.threads import ThreadCommons
from .getch import getch

class Input(ThreadCommons):

    input_command = ''
    input_history = []

    command_interpreting = None
    command_valid_list = None
    command_invalid_message = None
    command_case_sensitive = True

    def __init__(self, inp, out, gen_dat):
        super(Input, self).__init__(inp, out, gen_dat)
        self.input_command = ''
        self.interpreting_command = None
        return

    # scanning input
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

    # custom reaction
    def cleanup_input_command(self):
        if self.input_command:
            self.input_history.append(self.input_command)
            self.input_command = ''
        return

    def cleanup_command_interpretation(self):
        self.command_interpreting = None
        self.command_valid_list = None
        self.command_invalid_message = None
        self.command_case_sensitive = True
        return

    def send_completed_command(self):
        self.general_data['server_queue'].append(self.input_command)
        self.push_output('\n', typ='command_sign')
        self.push_output(self.input_command, typ='full_command')
        self.cleanup_input_command()
        return

    def push_answer(self):
        answer = self.input_command
        self.cleanup_input_command()
        if not self.command_case_sensitive:
            answer = answer.lower()

        # command not in list
        if self.command_valid_list and answer not in self.command_valid_list:
            self.push_output(self.command_invalid_message)
            return
        
        self.input_queue[0]['answer'] = answer
        self.cleanup_command_interpretation()
        return



    def send_quiet_command(self, command):
        self.general_data['server_queue'].append(command)
        self.cleanup_input_command()

    def autofill_command(self):
        # TO DO!
        pass

    def abort_written_command(self):
        self.push_output(chr(8)*len(self.input_command), typ='abort_command')
        self.input_command = ''
        return

    def remove_one_character(self):
        self.input_command = self.input_command[:-1]
        self.push_output(chr(8), typ='command_sign')
        return

    def add_command_sign(self, sign):
        self.input_command += sign
        self.push_output(sign, typ='command_sign')
        return

    def abort_current_command(self):
        self.general_data['server_queue'].append('abort_current')
        return

    # reaction switch
    def interpret_sign(self, sign):

        if self.command_interpreting is None:
            if ord(sign) == 13: # Enter
                if self.input_command:
                    self.send_completed_command()
            elif ord(sign) == 9: # Tab
                self.autofill_command()
            elif ord(sign) == 27: # Esc
                if self.input_command == '':
                    # What should be done?
                    self.send_quiet_command('exit_with_prompt')
                else:
                    self.abort_written_command()
            elif ord(sign) == 8: # Backspace
                if len(self.input_command) == 1:
                    self.abort_written_command()
                elif len(self.input_command) > 1:
                    self.remove_one_character()
            else:
                self.add_command_sign(sign)

        else:
            if ord(sign) == 13: # Enter
                if self.input_command:
                    self.push_output('\n', typ='command_sign')
                    self.push_output(self.input_command, typ='full_command')
                    self.push_answer()
            elif ord(sign) == 9: # Tab
                # TO DO
                pass
            elif ord(sign) == 27: # Esc
                if self.input_command == '':
                    # What should be done?
                    self.send_quiet_command('exit_with_prompt')
                else:
                    self.abort_written_command()
            elif ord(sign) == 8: # Backspace
                if len(self.input_command) == 1:
                    self.abort_written_command()
                elif len(self.input_command) > 1:
                    self.remove_one_character()
            else:
                self.add_command_sign(sign)

        return

    # varoius things
    def prepare_new_command_interpret(self):
        if self.command_interpreting is None and len(self.input_queue) > 0:
            # get new command
            full_command = self.input_queue[0]
            if 'answer' in full_command and full_command['answer']:
                # don't think about answered command
                return

            # basic info
            self.command_interpreting = full_command['command']

            # possible messages
            if 'options' in full_command:
                self.command_valid_list
                self.command_valid_list.append('exit')

            # what if invalid message
            self.command_invalid_message = 'Invalid command, please try again or exit:'
            if 'invalid_message' in full_command:
                self.command_invalid_message = full_command['invalid_message']

            # if the message is case sensitive
            self.command_case_sensitive = True
            if 'case_sensitive' in full_command:
                self.command_case_sensitive = full_command['case_sensitive']

            # cleaning up old messages
            self.cleanup_input_command()

        return

    # running thread
    def run_thread(self):
        while self.general_data['running']:
            sign = self.scan()
            if sign is None:
                continue

            self.prepare_new_command_interpret()

            if len(sign) == 1:
                self.interpret_sign(sign)

            else:
                # special signs! (arrows?)
                # TO DO!
                sleep(0.01)
        return

