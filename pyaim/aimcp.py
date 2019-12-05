import os
import subprocess
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


    def GetPassword(self, appid=None, safe=None, folder=None, objectName=None, username=None, address=None, database=None, policyid=None, reason=None, queryformat=None, connport=None, sendhash=False, output='Password'):
        var_dict = {
            'appid': appid,
            'reason': reason,
            'queryformat': queryformat,
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

        aim_query = 'Query='
        for key in var_query_filtered.keys():
            aim_query += '{}={};'.format(key, var_query_filtered[key])
        query = '{clipath} GetPassword {sep}p AppDescs.AppID={appid} {sep}p {query} {sep}p RequiredProps=* {sep}o {output}'.format(clipath=self._cli_path,sep=self.sep,appid=appid,query=aim_query,output=output)
        
        try:
            response = subprocess.run(query, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            if (response.stderr).decode('UTF-8'):
                raise Exception((response.stderr).decode('UTF-8').strip())
        except Exception as e:
            raise Exception(e)

        key_list = output.split(',')
        val_list = (response.stdout).decode('UTF-8').strip().split(',')
        zip_list = zip(key_list,val_list)
        ret_response = dict(zip_list)
        return ret_response