from urllib import request
from urllib.parse import urlencode
from json import loads

class Connection(object):

    headers = {"Content-Type":"application/json", "Accept":"application/json"}

    def full_connect(self, headers=None):
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

    def connect(self, url, custom_settings=None, headers=None, parse_to_dict=True):
        new_settings = custom_settings
        if new_settings is None:
            new_settings = self.settings
        if new_settings is None:
            self.push_output("Connection error: no settings included", typ="inset")
            return None

        if 'authorization' not in new_settings:
            self.push_output("No authorization in settings", typ="inset")
            return None

        new_headers = headers
        if new_headers is None:
            new_headers = self.headers
        new_headers['Authorization'] = "Basic " + new_settings['authorization']

        request_object = request.Request(url, headers=new_headers)
        try:
            connection = request.urlopen(request_object)
        except:
            self.push_output("Connection error", typ="inset")
            return None
        result = connection.read().decode("UTF-8")

        if parse_to_dict:
            try:
                result = loads(result)
            except:
                self.push_output("Error occured while parsing the output", typ="inset")

        return result

    def connect_api(self, table, sys_id=None, params={}):
        url = self.settings['instance_url']
        if not url.endswith("/"):
            url += "/"
        url += "api/now/table/"
        url += table
        if sys_id is not None:
            url += "/" + sys_id

        if params != {}:
            get_params = urlencode(params)
            url += "?" + get_params

        result = self.connect(url)
        # self.push_output(str(result), typ="pretty_text")
        return result

    def test_connection(self, server_data=None):
        old_data = self.settings
        if server_data is not None:
            self.settings = server_data

        result = self.connect_api("sys_properties", params={"sysparm_limit": "1"})

        self.settings = old_data

        if result is None:
            return False
        if type(result) is str:
            return False
        return True