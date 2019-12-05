import http.client
import json
import mimetypes
import ssl
import urllib.parse


class CCPPasswordREST(object):

    # Runs on Initialization
    def __init__(self, base_uri, verify=True):

        # Declare Init Variables
        self._base_uri = base_uri.rstrip('/').replace('https://','') # Example: https://pvwa.cyberarkexample.com
        self._context = ssl.create_default_context()
        self._headers = {'Content-Type': 'application/json'} # Build Header for GET Request

        if verify is False:
            self._context = ssl.create_unverified_context()


    # Checks that the AIM Web Service is available
    def check_service(self):
        try:
            url = '/AIMWebService/v1.1/aim.asmx'
            conn = http.client.HTTPSConnection(self._base_uri, context=self._context)
            conn.request("GET", url, headers=self._headers)
            res = conn.getresponse()
            data = res.read()
            status_code = res.status
            conn.close()

            if status_code != 200:
                raise Exception('ERROR: AIMWebService Not Found.')

        except Exception as e:
            raise Exception(e)
            exit()

        return 'SUCCESS: AIMWebService Found. Status Code: {}'.format(status_code)

    # Retrieve Account Object Properties using AIM Web Service
    def GetPassword(self, appid=None, safe=None, folder=None, objectName=None, username=None, address=None, database=None, policyid=None, reason=None, query_format=None):
        # Create a dict of potential URL parameters for CCP
        var_dict = {
            'appid': appid,
            'safe': safe,
            'folder': folder,
            'object': objectName,
            'username': username,
            'address': address,
            'database': database,
            'policyid': policyid,
            'reason': reason,
            'query_format': query_format
        }
        
        # Filter out None values from dict
        var_filtered = dict(filter(lambda x:x[1], var_dict.items()))

        # Check that appid and safe have values (required)
        # Check that either object or username has a value (required)
        if 'appid' not in var_filtered:
            raise Exception('ERROR: appid is a required parameter.')
        elif 'safe' not in var_filtered:
            raise Exception('ERROR: safe is a required parameter.')
        elif 'username' not in var_filtered and 'object' not in var_filtered:
            raise Exception('ERROR: either username or object requires a value.')

        # Urlify parameters for GET Request
        params = urllib.parse.urlencode(var_filtered)
        # Build URL for GET Request
        url = '/AIMWebService/api/Accounts?{}'.format(params)

        try:
            conn = http.client.HTTPSConnection(self._base_uri, context=self._context)
            conn.request("GET", url, headers=self._headers)
            res = conn.getresponse()
            data = res.read()
            conn.close()

        # Capture Any Exceptions that Occur
        except Exception as e:
            # Print Exception Details and Exit
            raise Exception(e)
            exit()
        
        # Deal with Python dict for return variable
        ret_response = json.loads(data.decode('UTF-8'))
        # Return Proper Response
        return ret_response
