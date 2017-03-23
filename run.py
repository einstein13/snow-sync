from settings.servers import servers


from urllib import request
from base64 import b64encode
from json import loads

username = b"admin"
password = b"Einstein.13"
authstr = (b'Basic ' + b64encode(b':'.join((username, password)))).decode("UTF-8")

headers = {"Content-Type":"application/json","Accept":"application/json", "Authorization": authstr}
url = 'https://dev30036.service-now.com/api/now/table/x_103706_marketing_atendees'
url = 'https://dev30036.service-now.com/api/now/table/sys_script?sysparm_limit=2'


req = request.Request(url, headers=headers)
w=request.urlopen(req)
s=w.read()
q=loads(s.decode("utf-8"))
q1=q['result']
print("- - - - - ")
print(q1[0])
print("- - - - - ")
print(q1[1])
print("- - - - - ")



from threading import Thread
from time import sleep

def threaded_function(input_stream, output_stream):
	while input_stream['running']:
		inp = input(">>> ")
		if(inp == "exit"):
			output_stream['exit'] = True
			input_stream['running'] = False
		else:
			print(inp)

w_inp = {'running': True}
w_out = {'exit': False}
thread = Thread(target = threaded_function, args = (w_inp, w_out))
thread.start()
while w_out['exit'] == False:
	print("waiting for exit")
	sleep(2)
print("Exited!")
