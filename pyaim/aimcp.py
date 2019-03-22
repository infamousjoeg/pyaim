import os
from subprocess import PIPE, Popen
from sys import platform


class CLIPasswordSDK(object):

    def __init__(self, cli_path):

        self._cli_path = cli_path

        # Check for Linux OS
        if platform == 'linux' or platform == 'linux2':
            self.sep = '-'
            if not os.path.isfile(self._cli_path):
                raise Exception('CLIPasswordSDK not found', 'Please make sure you provide a proper path to CLIPasswordSDK.')
        # Check for Windows OS
        elif platform == 'win32':
            self.sep = '/'
            if not os.path.isfile(self._cli_path):
                raise Exception('CLIPasswordSDK.exe not found', 'Please make sure you provide a proper path to CLIPasswordSDK.exe.')
        # Check for MacOS
        elif platform == 'darwin':
            raise Exception('Unsupported OS', 'Support only exists for Linux & Windows currently.')
        # Unknown platform returned
        else:
            raise Exception('Cannot detect OS', 'Your platform is unrecognizable. Please use Linux or Windows.')


    def GetPassword(self, appid=None, safe=None, objectName=None):
        var_checklist = [appid, safe, objectName]
        for var in var_checklist:
            if var is None:
                raise Exception('No {}. Please declare a valid {}.'.format(var,var))

        try:
            response, err = Popen(
                [
                    self._cli_path,
                    'GetPassword',
                    self.sep + 'p', 'AppDescs.AppID={}'.format(appid),
                    self.sep + 'p', 'Query=safe={safe};folder=Root;object={objectName}'.format(safe=safe,objectName=objectName),
                    self.sep + 'o', 'PassProps.UserName,Password,PassProps.Address,PassProps.Port,PasswordChangeInProcess'
                ],
                stdout=PIPE,
                stderr=PIPE
            ).communicate()

            if err:
                raise Exception(err.decode('UTF-8').strip())
        except Exception as e:
            raise Exception(e)
            exit()
            
        key_list = ['Username','Password','Address','Port','PasswordChangeInProcess']
        val_list = response.decode('UTF-8').strip().split(',')
        zip_list = zip(key_list,val_list)
        ret_response = dict(zip_list)
        return ret_response