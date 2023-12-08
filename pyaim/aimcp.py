"""Module providing a class for interacting with CyberArk's Credential Provider CLIPasswordSDK."""
import os
import subprocess
from sys import platform


class CLIPasswordSDK: # pylint: disable=too-few-public-methods
    """Class for interacting with CyberArk's Credential Provider CLIPasswordSDK."""

    def __init__(self, cli_path):

        self._cli_path = cli_path

        # Check for Linux OS
        if platform in ('linux', 'darwin'):
            self.sep = '-'
            if not os.path.isfile(self._cli_path):
                raise OSError('ERROR: CLIPasswordSDK not found',\
                              'Please make sure you provide a proper path to CLIPasswordSDK.')
        # Check for Windows OS
        elif platform == 'win32':
            self.sep = '/'
            if not os.path.isfile(self._cli_path):
                raise OSError('ERROR: CLIPasswordSDK.exe not found',\
                              'Please make sure you provide a proper path to CLIPasswordSDK.exe.')
        # Unknown platform returned
        else:
            raise OSError('Cannot detect OS',\
                          'Your platform is unrecognizable. Please use Linux, MacOS or Windows.')


    def GetPassword(self, appid=None, safe=None, folder=None, object=None, # pylint: disable=redefined-builtin,invalid-name,too-many-arguments,too-many-locals
            username=None, address=None, database=None, policyid=None,
            reason=None, queryformat=None, connport=None, sendhash=False,
            output='Password', delimiter=',', dual_accounts=False):
        """Retrieve Account Object Properties using CLIPasswordSDK."""
        var_dict = {
            'appid': appid,
            'reason': reason,
            'queryformat': queryformat,
            'port': connport,
            'sendhash': sendhash
        }
        # If dual_accounts is True, then set VirtualUsername
        # instead of a normal username property
        if dual_accounts:
            var_query = {'virtualusername': username}
        else:
            var_query = {'username': username}

        var_query['safe'] = safe
        var_query['folder'] = folder
        var_query['object'] = object
        var_query['address'] = address
        var_query['database'] = database
        var_query['policyid'] = policyid

        # Filter out None values from dicts
        var_filtered = dict(filter(lambda x:x[1], var_dict.items()))
        var_query_filtered = dict(filter(lambda x:x[1], var_query.items()))

        # Check that appid and safe have values (required)
        # Check that either object or username has a value (required)
        if 'appid' not in var_filtered:
            raise ValueError('ERROR: appid is a required parameter.')
        if 'safe' not in var_query_filtered:
            raise ValueError('ERROR: safe is a required parameter.')
        if 'username' not in var_query_filtered\
            and 'virtualusername' not in var_query_filtered\
            and 'object' not in var_query_filtered:
            raise ValueError('ERROR: either username or object requires\
                             a value or dual accounts should be true.')

        aim_query = ''
        for key, value in var_query_filtered.items():
            aim_query += f"{key}={value};"
        aim_query = aim_query[:-1]
        query = [
            self._cli_path,
            'GetPassword',
            self.sep + 'p', f"AppDescs.AppID={appid}",
            self.sep + 'p', f"Query={aim_query}",
            self.sep + 'p', 'RequiredProps=*',
            self.sep + 'o', output,
            self.sep + 'd', delimiter
        ]

        try:
            with subprocess.Popen(
                    query,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                ) as proc:
                response, err = proc.communicate()

            if err:
                raise ConnectionError(err.decode('UTF-8').strip())
        except Exception as e:
            raise Exception(e) # pylint: disable=raise-missing-from,broad-exception-raised

        key_list = output.split(',')
        val_list = response.decode('UTF-8').strip().split(delimiter)
        zip_list = zip(key_list,val_list)
        ret_response = dict(zip_list)
        return ret_response
