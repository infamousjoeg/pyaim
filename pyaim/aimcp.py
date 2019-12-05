import os
from subprocess import PIPE, Popen
from sys import platform


class CLIPasswordSDK(object):

    def __init__(self, cli_path):

        self._cli_path = cli_path

        # Check for Linux OS
        if platform == 'linux' or platform =='darwin':
            self.sep = '-'
            if not os.path.isfile(self._cli_path):
                raise Exception('ERROR: CLIPasswordSDK not found', 'Please make sure you provide a proper path to CLIPasswordSDK.')
        # Check for Windows OS
        elif platform == 'win32':
            self.sep = '/'
            if not os.path.isfile(self._cli_path):
                raise Exception('ERROR: CLIPasswordSDK.exe not found', 'Please make sure you provide a proper path to CLIPasswordSDK.exe.')
        # Unknown platform returned
        else:
            raise Exception('Cannot detect OS', 'Your platform is unrecognizable. Please use Linux, MacOS or Windows.')


    def GetPassword(self, appid=None, safe=None, folder=None, objectName=None, username=None, address=None, database=None, policyid=None, reason=None, queryformat=None, credfilepath=None, requiredprops=None, connport=None, sendhash=False):
        var_dict = {
            'appid': appid,
            'reason': reason,
            'queryformat': query_format,
            'credfilepath': credfilepath,
            'requiredprops': requiredprops,
            'port': connport,
            'sendhash': sendhash
        }
        var_query = {
            'safe': safe,
            'folder': folder,
            'object': objectName,
            'username': username,
            'address': address,
            'database': database,
            'policyid': policyid,
        }

        var_filtered = dict(filter(lambda x:x[1], var_dict.items()))
        var_query_filtered = dict(filter(lambda x:x[1], var_query.items()))

        # Check that appid and safe have values (required)
        # Check that either object or username has a value (required)
        if 'appid' not in var_filtered:
            raise Exception('ERROR: appid is a required parameter.')
        elif 'safe' not in var_query_filtered:
            raise Exception('ERROR: safe is a required parameter.')
        elif 'username' not in var_query_filtered and 'object' not in var_query_filtered:
            raise Exception('ERROR: either username or object requires a value.')

        query = []
        query.append(self._cli_path)
        query.append('GetPassword')
        query.append(self.sep + 'p', 'AppDescs.AppID={}'.format(appid))
        aim_query = 'Query='
        for key in var_query_filtered.keys():
            aim_query += '{}={};'.format(key, var_query_filtered[key])
        query.append(aim_query)

        try:
            response, err = Popen(
                query,
                stdout=PIPE,
                stderr=PIPE
            ).communicate()

            if err:
                raise Exception(err.decode('UTF-8').strip())
        except Exception as e:
            raise Exception(e)

        print(response)
        key_list = ['Username','Password','Address','Port','PasswordChangeInProcess']
        val_list = response.decode('UTF-8').strip().split(',')
        zip_list = zip(key_list,val_list)
        ret_response = dict(zip_list)
        return ret_response