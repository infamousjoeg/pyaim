import json
import ssl
import urllib.parse
import urllib.request


class CCPPasswordREST(object):

    # Runs on Initialization
    def __init__(self, base_uri, verify=True):

        # Declare Init Variables
        self._base_uri = base_uri.rstrip('/')                # Example: https://pvwa.cyberarkexample.com
        self._context = ssl.create_default_context()
        self._headers = {'Content-Type': 'application/json'} # Build Header for GET Request

        if verify is False:
            self._context.check_hostname = False
            self._context.verify_mode = ssl.CERT_NONE


    # Checks that the AIM Web Service is available
    def check_service(self):
        try:
            with urllib.request.urlopen(
                self._base_uri + '/AIMWebService/v1.1/aim.asmx',
                context=self._context
            ) as conn:
                status_code = conn.getcode()

            if status_code != 200:
                raise Exception('AIMWebService Not Found')

        except Exception as e:
            raise Exception(e)
            exit()

        return 'AIMWebService Found. Status Code: {}'.format(status_code)

    # Retrieve Account Object Properties using AIM Web Service
    def GetPassword(self, appid=None, safe=None, objectName=None):
        # Check for unassigned variable
        var_checklist = [appid, safe, objectName]
        for var in var_checklist:
            if var is None:
                raise Exception('No {}. Please declare a valid {}.'.format(var,var))

        # Urlify parameters for GET Request
        params = urllib.parse.urlencode({'appid': appid, 'folder': 'root', 'safe': safe, 'object': objectName})
        # Build URL for GET Request
        url = '{}/AIMWebService/api/Accounts?{}'.format(self._base_uri,params)

        try:
            request = urllib.request.Request(url, headers=self._headers)
            response = urllib.request.urlopen(request, context=self._context)
            resp_data = response.read()

        # Capture Any Exceptions that Occur
        except Exception as e:
            # Print Exception Details and Exit
            raise Exception(e)
            exit()
        
        # Deal with Python dict for return variable
        ret_response = json.loads(resp_data.decode('UTF-8'))
        # Return Proper Response
        return ret_response
