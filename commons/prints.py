from json import dumps
from hashlib import sha1

def pretty_json_print(data):
    string = dumps(data, indent=4)
    return string

def fix_newline_signs(string):
    new_string = string
    new_string = new_string.replace("\r\n", "\n")
    new_string = new_string.replace("\n\r", "\n")
    new_string = new_string.replace("\r", "\n")
    return new_string

def shorten_string(string, length=40):
    new_string = fix_newline_signs(string)
    new_string = new_string.replace("\n", " \\n")
    new_string = new_string.replace("\t", "  ")
    if len(new_string) < length:
        return new_string
    return new_string[:length-3] + "..."

# generates list from dictionary, used for diplaying table form of dicts
def dict_to_list(dictionary, records=[], name_start=None):
    keys = list(dictionary.keys())
    keys.sort()

    name_basic = ""
    if name_start is not None:
        name_basic = name_start + "."

    for key in keys:
        name = name_basic + key
        value = dictionary[key]
        value_to_save = None

        if type(value) is dict:
            dict_to_list(value, records=records, name_start=name)
            continue
        elif type(value) is str:
            if value == "":
                value_to_save = "  (blank)"
            else:
                value_to_save = shorten_string(value)
        else:
            value_to_save = shorten_string(str(value))

        records.append([name, value_to_save])

    return records

# generates text for row data file
def generate_standard_data_file_content(data_dictionary, data_content):
    result = ""
    indent = "    "
    for row in data_content:
        if type(row) is str:
            result += "# " + row + "\n"
        elif type(row) is list:
            comments = True
            for element in row:
                if element == "":
                    comments = False
                    # ends of comments
                else:
                    if comments:
                        # add comment
                        result += indent + "# " + element + "\n"
                    else:
                        # add variable
                        # handle with dot-walking
                        splitted = element.split(".")
                        to_add = dict(data_dictionary)
                        for key in splitted:
                            to_add = to_add[key]
                        result += indent + element + " = " + to_add + "\n"

            result += "\n"
    return result

def generate_hash(string):
    hashed = sha1(string.encode("utf-8"))
    return hashed.hexdigest()