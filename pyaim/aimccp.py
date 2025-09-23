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
        """Validates connection configuration without making API calls.

        Production Mode: This method performs LOCAL validation only to avoid
        generating unnecessary logs in CCP. For actual service health checks,
        use GetPassword() and handle exceptions.

        Returns:
            str: Success message indicating configuration is valid

        Raises:
            ValueError: If connection configuration is invalid

        Note:
            This method does NOT verify if the CCP service is actually running.
            To verify service availability, call GetPassword() with valid
            credentials and handle any ConnectionError or Exception responses.

        Example:
            # Don't rely on check_service() for health checks
            try:
                response = aimccp.GetPassword(appid='healthcheck',
                                             safe='test',
                                             object='testaccount')
                # Service is healthy and credentials valid
            except ConnectionError as e:
                # Service may be down or unreachable
                print(f"Service unhealthy: {e}")
            except Exception as e:
                # Other errors (auth, permissions, etc.)
                print(f"Service error: {e}")
        """
        # Validate that we have minimum connection info
        if not self._base_uri:
            raise ValueError("Base URI is required for connection")

        if not self._service_path:
            raise ValueError("Service path is required for connection")

        if not self._context:
            raise ValueError("SSL context not properly initialized")

        # Return success without making any API calls (Production Mode)
        return f"Configuration validated for {self._base_uri}/{self._service_path}. Use GetPassword() to verify service health."


    def GetPassword(self, appid=None, safe=None, folder=None, object=None, # pylint: disable=redefined-builtin,invalid-name,disable=too-many-arguments,too-many-locals
            username=None, address=None, database=None, policyid=None,
            reason=None, query_format=None, dual_accounts=False):
        """Retrieve Account Object Properties using AIM Web Service.

        This method also serves as the recommended health check mechanism.
        """
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
            status_code = res.status
            data = res.read()
            conn.close()

            # Enhanced error handling for health check use cases
            if status_code == 404:
                raise ConnectionError(
                    f"CCP service not found at {self._base_uri}/{self._service_path}. "
                    f"Status: {status_code}. Check service path and CCP installation."
                )
            elif status_code >= 500:
                raise ConnectionError(
                    f"CCP service error at {self._base_uri}/{self._service_path}. "
                    f"Status: {status_code}. Service may be down or misconfigured."
                )
            elif status_code == 401:
                raise ConnectionError(
                    f"Authentication failed. AppID '{appid}' may not be authorized. "
                    f"Status: {status_code}."
                )
            elif status_code == 403:
                raise ConnectionError(
                    f"Access forbidden. AppID '{appid}' lacks permissions for safe '{safe}'. "
                    f"Status: {status_code}."
                )

        except http.client.HTTPException as e:
            raise ConnectionError(
                f"Network error connecting to {self._base_uri}: {e}"
            ) from e
        except ConnectionError:
            raise
        except Exception as e:
            raise Exception(e) # pylint: disable=raise-missing-from,broad-exception-raised

        # Deal with Python dict for return variable
        ret_response = json.loads(data.decode('UTF-8'))
        # Return Proper Response
        return ret_response
