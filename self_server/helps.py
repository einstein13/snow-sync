from .datatypes import CommandRecognizer

class HelpData(object):

    help_texts = {
        # BASIC
        'default': [
            "H E L P",
            "",
            "Possible commands:",
            "BASIC:",
            "  help - shows help (ex.: \"help exit\")",
            "  exit - close down program",
            "SETTINGS:",
            "  show settings - show table with all known settings",
            "  read settings - read chosen settings from recorded file",
            "  add settings - add new settings to recorded file",
            "  edit settings - edit saved settings in recorded file",
            "  delete settings - delete chosen settings from recorded file",
            "FILES:",
            "  show files - show list of files within configuration",
            "  add files - add new file to the configuration",
            "  delete files - delete existing file record from the configuration",
            "  truncate files - delete all records from the configuration",
            "SYNCHRO:",
            "  pull - get all files from the server",
            "  push - update files on the server",
            "  status - show status of files on local disk"
            "",
            "Other topics:",
            "  about",
            "  commands",
            "  settings",
            "  files",
            "  synchro",
            ],
        'help': [
            "HELP command",
            "show explanation about any command available in the program",
            "Usage examples:",
            "  help push",
            "  man exit"
            ],
        'exit': [
            "EXIT command",
            "Exits the program. You can also use Escape button to exit any stage.",
            "Escaping from main stage will start exit procedure with prompt."
            ],
        # FILES & SETTINGS
        'show': {
            'settings': [
                "SHOW SETTINGS command",
                "Shows all available settings in a simple table.",
                "The table conains only name and URL of the instance.",
                "All listed instances are fully defined (url, authorization)",
                "and can be used as valid ones. They may not working because",
                "of wrong password / lack of internet connection.",
                "",
                "See also: \"show files\", \"add settings\", \"read settings\""
                ],
            'files': [
                "SHOW FILES command",
                "Shows all defined files of current settings listed in a table.",
                "It doesn't check changes on server or local side.",
                "Running other commands can modify or use this list",
                "",
                "See also: \"show settings\", \"add files\", \"status\"",
                ],
            'default': 'did you mean \"show files\" or \"show settings\"?'
            },
        'read': {
            'settings': '',
            'default': 'did you mean \"read settings\"?',
            },
        'add': {
            'settings': '',
            'files': '',
            'default': 'did you mean \"add files\" or \"add settings\"?'
            },
        'edit': {
            'settings': '',
            'default': 'did you mean \"edit settings\"?'
            },
        'delete': {
            'settings': '',
            'files': '',
            'default': 'did you mean \"delete settings\" or \"delete files\"?'
            },
        # SYNCHRO
        'status': [
            ],
        'pull': [
            ],
        'push': [
            ],
        'watch': [
            ],
        'unwatch': ['currently under construction'
            ],
        # OTHER TOPICS,
        'about': [
            ],
        'commands': [
            ],
        'settings': [
            ],
        'setting': 'did you mean \"settings\"?',
        'files': [
            ],
        'file': 'did you mean \"files\"?',
        'synchro': ['currently under construction'
            ],
        'synchronizing': 'did you mean \"synchro\"?'
        }

    # help parts
    def show_starting_screen(self):
        string = [
            "Welcome to the SNow synch server",
            "To show help type \"help\", to quit: \"exit\",",
            "then push enter to confirm command."
            ]
        string = "\n".join(string)
        self.push_output(string, typ='pretty_text')
        return

    def show_help(self, command):
        self.exit_silence = True

        CR = CommandRecognizer()
        command_arguments = CR.return_command_arguments(command)
        command_arguments[2].append("default")
        
        display_data = self.help_texts
        unknown_argument_usage = False
        unknown_argument_text = ""
        for keyword in command_arguments[2]:
            if type(display_data) in (str, list):
                break
            if keyword not in display_data.keys():
                unknown_argument_usage = True
                unknown_argument_text = keyword
                display_data = display_data['default']
            else:
                display_data = display_data[keyword]

        if type(display_data) is dict:
            display_data = display_data['default']

        if type(display_data) is list:
            display_data = "\n".join(display_data)

        if unknown_argument_usage:
            self.push_output("Unable to recognize \"%s\" argument" % unknown_argument_text, typ="inset")

        self.push_output(display_data, typ='pretty_text')
        return
    
    
        