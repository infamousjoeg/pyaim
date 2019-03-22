import json
import ssl
import urllib.parse
import urllib.request


class CCPPasswordREST(object):

    # Runs on Initialization
    def __init__(self, base_uri, verify=True):

        # Declare Init Variables
        self._base_uri = base_uri.rstrip('/')   # Example: https://pvwa.cyberarkexample.com
        
        if verify is False:
            self._context = ssl.create_default_context()
            self._context.check_hostname = False
            self._context.verify_mode = ssl.CERT_NONE
        else:
            self._context = ssl.create_default_context()


    # Checks that the AIM Web Service is available
    def check_service(self):
        try:
            conn = urllib.request.urlopen(self._base_uri + '/AIMWebService/v1.1/aim.asmx', context=self._context)
            status_code = conn.getcode()
            conn.close()
        except Exception as e:
            return 'AIMWebService Not Found. Exception: {}'.format(e)
            exit()

        return 'AIMWebService Found. Status Code: {}'.format(status_code)

    # Retrieve Account Object Properties using AIM Web Service
    def GetPassword(self, appid=None, safe=None, objectName=None):
        # Check for unassigned variable
        var_list = [appid, safe, objectName]
        for var in var_list:
            if var is None:
                raise Exception('No {}'.format(var), 'Please declare a valid {}.'.format(var))

        try:
            # Urlify parameters for GET Request
            params = urllib.parse.urlencode({'appid': appid, 'folder': 'root', 'safe': safe, 'object': objectName})
            # Build Header for GET Request
            headers = {'Content-Type': 'application/json'}
            # Build URL for GET Request
            url = self._base_uri + '/AIMWebService/api/Accounts?{}'.format(params)
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, context=self._context)
            resp_data = response.read()

        # Capture Any Exceptions that Occur
        except Exception as e:
            # Print Exception Details and Exit
            return(e)
            exit()
        
        # Deal with Python dict for return variable
        ret_response = json.loads(resp_data.decode('UTF-8'))
        # Return Proper Response
        return ret_response
