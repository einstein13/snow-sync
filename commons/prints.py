from json import dumps
from hashlib import sha1
from base64 import b64encode

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

def generate_hash(string):
    hashed = sha1(string.encode("utf-8"))
    return hashed.hexdigest()

def hash_password(username, password):
    string = username + ":" + password
    hashed = b64encode(bytes(string, "UTF-8")).decode("UTF-8")
    return hashed