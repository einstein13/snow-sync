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
            "  status - show status of files on local disk",
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
            'settings': [
                "READ SETTINGS commmand",
                "Reads saved configuration to program memory.",
                "You can define settings by: user defined name (first argument",
                "when you defined new connection), setting number on list",
                "(command show_settings will show correct list)",
                "or by default: first settings on the list.",
                "",
                "Basic usage: \"read settings 1\", \"read settings MyName\" ",
                "",
                "See also: \"show settings\", \"add settings\""
                ],
            'default': 'did you mean \"read settings\"?',
            },
        'add': {
            'settings': [
                "ADD SETTINGS command",
                "Adds new connection with ServiceNow record.",
                "To provide all necessary information,",
                "you will answer several questions:",
                "  * Name of the settings you want to see",
                "      (can be \"my_dev_instance\")",
                "  * Short name of the instance (ex.: dev20354)",
                "  * URL of the instance (based on short name)",
                "  * Username you want to use for connection",
                "  * Password for username (is hidden by \"*\" signs)",
                "After giving that information, the connection will be tested.",
                "Data about connection will be stored on your local drive,",
                "but password will be stored in hashed way.",
                "The connection data will not be used as active settings,",
                "you have to read it by using read_settings command.",
                "",
                "See also: \"show settings\", \"add files\""
                ],
            'files': [
                "ADD FILES command",
                "Adds new file to your local disk and saved files list.",
                "To download a file, you have to provide:",
                "  * Type of file (business rule/ client script/ ...)",
                "  * sys_id of the object",
                "The program will try to connect to ServiceNow instance",
                "and download correct data. After that files will be stored.",
                "All the process will be done automatic.",
                "",
                "Files customization",
                "There is also a possibility to download custom file(s).",
                "You need to provide extra table name",
                "(ex.: u_custom_script) where the object is.",
                "After that data will be downloaded and the rest of process",
                "will contains:",
                "  * Showing data in a table form",
                "  * Asking about scripts (long data)",
                "  * Asking about other data (short forms)",
                "This process is not recommended to standard users.",
                "Also you can define your own form and scripts files",
                "for standard types of files, without making any changes",
                "in a program code.",
                "",
                "See also: \"show files\", \"add setttings\", \"status\"",
                ],
            'default': 'did you mean \"add files\" or \"add settings\"?'
            },
        'edit': {
            'settings': [
                "EDIT SETTINGS command",
                "currently under construction"
                ],
            'default': 'did you mean \"edit settings\"?'
            },
        'delete': {
            'settings': [
                "DELETE SETTINGS command",
                "Deletes chosen settings from stored list.",
                "There are two possibilities of doing this:",
                "  * by providing user name of the settings",
                "  * by choosing from the list of settings.",
                "With the first way you will be aksed",
                "to confirm deletion. While with the second way",
                "you will see a list with all stored settings",
                "and you will be asked do specify correct name.",
                "Deleting will erase data about connection,",
                "but WILL NOT erase stored files on the disk!",
                "Files in the \"project\" folder are safe.",
                "",
                "See also: \"add settings\", \"show settings\", \"delete files\"",
                ],
            'files': '',
            'default': 'did you mean \"delete settings\" or \"delete files\"?'
            },
        # SYNCHRO
        'status': [
            "STATUS command",
            "Shows status of the files: are they available or changed.",
            "First information is about how many changed files are discovered.",
            "A table with all listed files and their statuses can be shown.",
            "",
            "See also: \"pull\", \"push\""
            ],
        'pull': [
            "PULL command",
            "Gets all new information from the server.",
            "If any changes are detected on your local project,",
            "you will be asked if you are sure about this process.",
            "Pulling will not overwrite all the files. Only new",
            "information will be stored and possibly overwrite",
            "changes made by you.",
            "Example: you have downloaded 4 files: A, B, C and D.",
            "Then you modified A and B. Somebody modified B and C",
            "and changes are stored in ServiceNow instance.",
            "After pull command A will stay with your changes,",
            "B will be overwritten to current instance version,",
            "C will be updated, and D will stay as it is.",
            "",
            "See also: \"push\", \"status\", \"watch\", \"synchro\""
            ],
        'push': [
            "PUSH command",
            "Sends all modified files to the ServiceNow instance.",
            "All changes you've done to the tracked files",
            "will be sent to ServiceNow. There is no check",
            "if anybody made any changes there, and all",
            "modified files will be overwritten.",
            "Example: you have downloaded 2 files: A and B.",
            "A was modified on your local disk, and both",
            "of them were modified in ServiceNow instance.",
            "After push command, A file will be overwritten",
            "and B will stay as it was.",
            "",
            "See also: \"pull\", \"status\", \"watch\", \"synchro\"",
            ],
        'watch': [
            "WATCH command",
            "currently under construction"
            ],
        'unwatch': [
            "UNWATCH command",
            "currently under construction"
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
    
    
        