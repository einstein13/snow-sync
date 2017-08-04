#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread

from commons.threads import ThreadCommons
from commons.standard_objects import eol
from self_server.datatypes import CommandRecognizer
from .getch import getch_thread

class Input(ThreadCommons):

    input_command = ''
    input_history = []
    input_history_position = -1

    autofill_old_command = ''
    autofill_position = 0
    autofill_list = []

    command_interpreting = None
    command_valid_list = None
    command_invalid_message = None
    command_case_sensitive = True
    command_default_value = None
    command_character_replacement = None
    command_exit_current_command_on_escape = True

    prepared_arguments = {}

    def __init__(self, inp, out, gen_dat):
        super(Input, self).__init__(inp, out, gen_dat)
        self.input_command = ''
        self.input_history = []
        self.prepared_arguments['signs'] = []
        self.prepared_arguments['run'] = True
        return

    def initialize_scanning(self):
        thread = Thread(target=getch_thread, args=(self.prepared_arguments,))
        thread.start()
        return

    # scanning input
    def scan(self):
        result = []
        while len(self.prepared_arguments['signs']) > 0:
            result.append(self.prepared_arguments['signs'].pop(0))
            sleep(0.002)

        # no input
        if len(result) == 0:
            sleep(0.03)
            return None

        # there is an input
        for itr in range(len(result)):
            try:
                result[itr] = result[itr].decode("utf-8")
            except:
                pass
                # print("Error parsing sign [%d]" % ord(result[itr]))
            # print("=%d=" % ord(result[itr]))

        # it is only one sign
        if len(result) == 1:
            return result[0]
        # more signs
        return result

    # custom reaction
    def cleanup_autofill(self):
        self.autofill_old_command = ''
        self.autofill_position = 0
        self.autofill_list = []
        return

    def cleanup_input_command(self):
        if self.input_command:
            self.input_history.append(self.input_command)
            self.input_history_position = len(self.input_history)
        self.input_command = ''
        return

    def cleanup_command_interpretation(self):
        self.command_interpreting = None
        self.command_valid_list = None
        self.command_invalid_message = None
        self.command_case_sensitive = True
        self.command_default_value = None
        self.command_character_replacement = None
        self.command_exit_current_command_on_escape = True
        return

    def send_completed_command(self):
        self.general_data['server_queue'].append(self.input_command)
        self.push_output(eol, typ='command_sign')
        self.push_output(self.input_command, typ='full_command')
        self.cleanup_input_command()
        self.cleanup_autofill()
        return

    def push_answer(self):
        answer = self.input_command
        self.cleanup_input_command()
        self.cleanup_autofill()
        if answer is not None:
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
        self.cleanup_autofill()

    def autofill_command(self):
        if self.input_command == '':
            # if there is nothing to look for
            return

        # else - there is something written
        # self.push_output(str(self.autofill_position), typ="inset")
        # self.push_output(str(self.autofill_list), typ="inset")
        # self.push_output(str(self.autofill_old_command), typ="inset")
        if self.autofill_old_command == '':
            CD = CommandRecognizer()
            possibilities = CD.find_autofill_commands(self.input_command)
            if len(possibilities) == 0:
                # nothing to do
                return
            self.autofill_position = 0
            self.autofill_list = possibilities
            self.autofill_old_command = self.input_command
            # self.push_output(str(self.autofill_position), typ="inset")
            # self.push_output(str(self.autofill_list), typ="inset")
            # self.push_output(str(self.autofill_old_command), typ="inset")

        command = self.autofill_list[self.autofill_position]
        # self.push_output(command, typ="pretty_text")
        # set next number
        self.autofill_position = (self.autofill_position + 1) % len(self.autofill_list)
        self.abort_written_command()
        self.input_command = command
        self.push_output(self.input_command, typ='command_sign')
        return

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

    def quit_current_command(self):
        self.input_queue[0]['answer'] = None
        self.general_data['server_queue'].append('exit_current_command')
        return

    def copy_from_clipboard(self):
        # http://stackoverflow.com/questions/16188160/how-to-read-data-from-clipboard-and-pass-it-as-value-to-a-variable-in-python/16189232#16189232
        try:
            # Python2
            import Tkinter as tk
        except ImportError:
            # Python3
            import tkinter as tk

        root = tk.Tk()
        # keep the window from showing
        root.withdraw()

        # read the clipboard
        result = root.clipboard_get()
        return result

    def copy_clipboard_to_input(self):
        clipboard = self.copy_from_clipboard()
        for itr in range(len(clipboard)):
            sign = clipboard[itr]
            if ord(sign) in (3, 22, 27, 9, 8):
                # special characters
                continue
            self.interpret_sign(sign)

    # reaction switch
    def interpret_sign(self, sign):

        # standard command
        if self.command_interpreting is None:
            if self.input_command == '' and ord(sign) == 32: # space
                # command can't starts with the space
                pass
            elif ord(sign) == 13: # Enter
                if self.input_command:
                    self.send_completed_command()
                else:
                    self.push_output("", typ="text")
            elif ord(sign) == 9: # Tab
                self.autofill_command()
            elif ord(sign) == 3: # Ctrl + C
                # TO DO
                pass
            elif ord(sign) == 22: # Ctrl + V
                self.copy_clipboard_to_input()
            elif ord(sign) == 27: # Esc
                self.cleanup_autofill()
                if self.input_command == '':
                    # What should be done?
                    self.send_quiet_command('exit_with_prompt')
                else:
                    self.abort_written_command()
            elif ord(sign) == 8 or ord(sign) == 127: # Backspace: Win / Linux
                self.cleanup_autofill()
                if len(self.input_command) == 1:
                    self.abort_written_command()
                elif len(self.input_command) > 1:
                    self.remove_one_character()
            else:
                self.add_command_sign(sign)

        # expected command
        else:
            if self.input_command == '' and ord(sign) == 32: # space
                # command can't starts with the space
                pass
            elif ord(sign) == 13: # Enter
                if self.input_command:
                    if self.command_character_replacement is None:
                        self.push_output(self.input_command, typ='full_command')
                    else:
                        self.push_output(eol, typ="full_command")
                elif self.command_default_value:
                    if self.command_character_replacement is None:
                        self.push_output(self.command_default_value, typ='full_command')
                    self.input_command = self.command_default_value
                self.push_answer() # push answer to the input object
            elif ord(sign) == 9: # Tab
                # TO DO
                pass
            elif ord(sign) == 3: # Ctrl + C
                # TO DO
                pass
            elif ord(sign) == 22: # Ctrl + V
                self.copy_clipboard_to_input()
            elif ord(sign) == 27: # Esc
                self.cleanup_autofill()
                if self.input_command != '':
                    self.abort_written_command()
                else:
                    if self.command_exit_current_command_on_escape:
                        # exit current command
                        self.quit_current_command()
                    else:
                        # send None as an aswer
                        self.input_command = None
                        self.push_answer()
                    self.cleanup_command_interpretation()
            elif ord(sign) == 8 or ord(sign) == 127: # Backspace: Win / Linux
                self.cleanup_autofill()
                if len(self.input_command) == 1:
                    self.abort_written_command()
                elif len(self.input_command) > 1:
                    self.remove_one_character()
            else:
                if self.command_character_replacement is None:
                    self.add_command_sign(sign)
                else:
                    self.input_command += sign
                    self.push_output(self.command_character_replacement, typ='command_sign')
        return

    def get_previous_history_command(self):
        if self.input_history_position > 0:
            # get command
            self.input_history_position -= 1
            command = self.input_history[self.input_history_position]
            # clean memory
            if self.input_command != '':
                self.abort_written_command()
            # push command
            self.push_output(command, typ='command_sign')
            self.input_command = command
        return None

    def get_next_history_command(self):
        if self.input_history_position < len(self.input_history)-1 and\
                self.input_history_position >= 0:
            # get command
            self.input_history_position += 1
            command = self.input_history[self.input_history_position]
            # clean memory
            if self.input_command != '':
                self.abort_written_command()
            # push command
            self.push_output(command, typ='command_sign')
            self.input_command = command
        return None

    def interpret_special_signs(self, signs):
        # arrows: Windows
        if len(signs) == 2 and ord(signs[0]) in (224, 0):
            if signs[1] == 'H': # Arrow UP
                self.get_previous_history_command()
            elif signs[1] == 'P': # Arrow DOWN
                self.get_next_history_command()
        if len(signs) == 3 and ord(signs[0]) == 27 and signs[1] == '[':
            if signs[2] == 'A':
                self.get_previous_history_command()
            if signs[2] == 'B':
                self.get_next_history_command()
        return None

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
                self.command_valid_list = full_command['options']
                # self.command_valid_list.append('exit')

            # what if invalid message
            self.command_invalid_message = 'Invalid command, please try again or exit:'
            if 'invalid_message' in full_command:
                self.command_invalid_message = full_command['invalid_message']

            # if the message is case sensitive
            self.command_case_sensitive = True
            if 'case_sensitive' in full_command:
                self.command_case_sensitive = full_command['case_sensitive']

            # if there is default value
            if 'default_value' in full_command:
                self.command_default_value = full_command['default_value']

            # if there is an character replacement
            if 'character_replacement' in full_command:
                self.command_character_replacement = full_command['character_replacement']

            if 'exit_current_on_escape' in full_command:
                self.command_exit_current_command_on_escape = full_command['exit_current_on_escape']

            # cleaning up old messages
            self.cleanup_input_command()
            self.cleanup_autofill()

        return

    # running thread
    def run_thread(self):
        self.initialize_scanning()
        while self.general_data['running']:
            sign = self.scan()
            if sign is None:
                continue

            self.prepare_new_command_interpret()

            if len(sign) == 1:
                self.interpret_sign(sign)

            else:
                # arrows and ? (what else?)
                self.interpret_special_signs(sign)
                # sleep(0.01)
        self.prepared_arguments['run'] = False
        return
