from json import loads

try:
    file = open("settings/servers.json", "r")
except:
    try:
        file = open("servers.json", "r")
    except:
        print("OPEN ERROR")
to_parse = file.read()
file.close()
servers = {}
try:
    servers = loads(to_parse)
except:
    pass