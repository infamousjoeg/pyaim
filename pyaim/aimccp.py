import os
import http.client
import sys.platforms


class CCPPasswordREST(object):

    def __init__(self, base_uri):

        self._base_uri = base_uri

    def check_service(self):

        # Check self._base_uri + "/AIMWebService/v1.1/aim.asmx" for 200 OK

    def GetPassword(self, appid=None, safe=None, objectName=None):
        var_list = [appid, safe, objectName]
        for var in var_list:
            if var is None:
                raise Exception('No {}'.format(var), 'Please declare a valid {}.'.format(var))

        try:
            import http.client

conn = http.client.HTTPConnection("components,cyberarkdemo,example")

payload = ""

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "1a38e59a-7a1a-4c3d-849b-7f42055d6ab7"
    }

conn.request("GET", "AIMWebService,api,Accounts", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
        except e as Exception:
            print(e)
            exit()
        
        # Deal with Python dict for return variable
        key_list = ['Username','Password','Address','Port','PasswordChangeInProcess']
        val_list = response.decode('UTF-8').strip().split(',')
        zip_list = zip(key_list,val_list)
        ret_response = dict(zip_list)
        return ret_response
