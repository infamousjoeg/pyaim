import os
from sys import platform

import requests


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
            # Send the request to AIM CCP and receive JSON response
        except e as Exception:
            print(e)
            exit()
        
        # Deal with Python dict for return variable
        key_list = ['Username','Password','Address','Port','PasswordChangeInProcess']
        val_list = response.decode('UTF-8').strip().split(',')
        zip_list = zip(key_list,val_list)
        ret_response = dict(zip_list)
        return ret_response
