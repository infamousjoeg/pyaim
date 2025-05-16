"""Module providing a class for interacting with CyberArk's CCP REST API."""
import http.client
import json
import os
import ssl
import urllib.parse

class CCPPasswordREST:
    """Class for interacting with CyberArk's CCP REST API.

    Args:
        base_uri: Base URI for the CyberArk server
        service_path: Service path (default: "AIMWebService")
        verify: SSL certificate verification. Can be:
            - True: Use default certificate verification
            - False: Disable certificate verification
            - str: Path to CA bundle file or directory
        cert: Client certificate tuple (certfile, keyfile)
        timeout: Request timeout in seconds
    """

    def __init__(self, base_uri, service_path="AIMWebService", verify=True, cert=None, timeout=30): # pylint: disable=too-many-arguments

        # Declare Init Variables
        self._base_uri = base_uri.rstrip('/').replace('https://','')
        self._service_path = service_path
        self._headers = {'Content-Type': 'application/json'}
        self._timeout = timeout

        if verify is False:
            self._context = ssl._create_unverified_context()
            self._context.check_hostname = False
        elif isinstance(verify, str):
            if not os.path.exists(verify):
                raise ValueError(f"Certificate path does not exist: {verify}")

            if os.path.isfile(verify):
                self._context = ssl.create_default_context(cafile=verify)
            elif os.path.isdir(verify):
                self._context = ssl.create_default_context(capath=verify)
            else:
                raise ValueError(f"Path is neither file nor directory: {verify}")
        elif verify is True:
            self._context = ssl.create_default_context()
        else:
            raise TypeError(f"verify must be bool or str, got {type(verify)}")

        # Client Certificate Authentication
        if cert:
            self._context.load_cert_chain(certfile=cert[0], keyfile=cert[1])


    def check_service(self):
        """Checks that the AIM Web Service is available."""
        try:
            url = f'/{self._service_path}/v1.1/aim.asmx'
            conn = http.client.HTTPSConnection(
                self._base_uri, context=self._context, timeout=self._timeout)
            conn.request("GET", url, headers=self._headers)
            res = conn.getresponse()
            status_code = res.status
            conn.close()

            if status_code != 200:
                raise ConnectionError(f'ERROR: {self._service_path} Not Found.')

        except Exception as e:
            raise Exception(e) # pylint: disable=raise-missing-from,broad-exception-raised

        return f"SUCCESS: {self._service_path} Found. Status Code: {status_code}"

    def GetPassword(self, appid=None, safe=None, folder=None, object=None, # pylint: disable=redefined-builtin,invalid-name,disable=too-many-arguments,too-many-locals
            username=None, address=None, database=None, policyid=None,
            reason=None, query_format=None, dual_accounts=False):
        """Retrieve Account Object Properties using AIM Web Service."""
        # Check for username or virtual username (dual accounts)
        if dual_accounts:
            var_dict = f"{'query': 'VirtualUsername={username}'}"
        else:
            var_dict = {'username': username}

        # Create a dict of potential URL parameters for CCP
        var_dict['appid'] = appid
        var_dict['safe'] = safe
        var_dict['folder'] = folder
        var_dict['object'] = object
        var_dict['address'] = address
        var_dict['database'] = database
        var_dict['policyid'] = policyid
        var_dict['reason'] = reason
        var_dict['query_format'] = query_format

        # Filter out None values from dict
        var_filtered = dict(filter(lambda x:x[1], var_dict.items()))

        # Check that appid and safe have values (required)
        # Check that either object or username has a value (required)
        if 'appid' not in var_filtered:
            raise ValueError('ERROR: appid is a required parameter.')
        if 'safe' not in var_filtered:
            raise ValueError('ERROR: safe is a required parameter.')
        if 'username' not in var_filtered \
            and 'query' not in var_filtered \
            and 'object' not in var_filtered:
            raise ValueError('ERROR: either username or object requires a \
                            value or dual accounts should be true.')

        # Urlify parameters for GET Request
        params = urllib.parse.urlencode(var_filtered)
        # Build URL for GET Request
        url = f"/{self._service_path}/api/Accounts?{params}"

        try:
            conn = http.client.HTTPSConnection(
                self._base_uri, context=self._context, timeout=self._timeout)
            conn.request("GET", url, headers=self._headers)
            res = conn.getresponse()
            data = res.read()
            conn.close()

        # Capture Any Exceptions that Occur
        except Exception as e:
            # Print Exception Details and Exit
            raise Exception(e) # pylint: disable=raise-missing-from,broad-exception-raised

        # Deal with Python dict for return variable
        ret_response = json.loads(data.decode('UTF-8'))
        # Return Proper Response
        return ret_response
