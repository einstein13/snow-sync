from json import dumps

def pretty_json_print(data):
    string = dumps(data, indent=4)
    return string