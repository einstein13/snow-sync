from urllib import request
from json import loads

class Link(object):

    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    server_data = None

    def __init__(self, server_data):
        super(Link, self).__init__()
        self.server_data = server_data
        return

    def connect(self, headers=None):
        # headers
        new_headers = headers
        if new_headers is None:
            new_headers = self.headers
        new_headers['Authorization'] = "Basic " + self.server_data['authorization']
        # url
        new_url = 'https://dev30036.service-now.com/api/now/table/sys_script?sysparm_limit=2'
        request_object = request.Request(new_url, headers=new_headers)
        url_connection=request.urlopen(request_object)
        connection_result=url_connection.read()
        dict_result=loads(connection_result.decode("utf-8"))
        return dict_result

    def test_connection(self):
        to_open="sys_properties_list.do"
        url = self.server_data['']