import os
import time
from subprocess import PIPE, Popen
from sys import platform


class clipasswordsdk(object):

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


    def GetPassword(self, appid=None, safe=None, obj=None):
        # Check appid is declared
        if appid is None:
            raise Exception('No Application ID', 'Please declare a valid Application ID.')
        # Check safe is declared
        elif safe is None:
            raise Exception('No Safe Name', 'Please declare a valid Safe name.')
        # Check object name is declared
        elif obj is None:
            raise Exception('No Object Name', 'Please declare a valid Object name.')
        else:
            try:
                response, err = Popen(
                    [
                        '{}'.format(self._cli_path),
                        'GetPassword',
                        '{}p'.format(self.sep), 'AppDescs.AppID={}'.format(appid),
                        '{}p'.format(self.sep), 'Query=safe={safe};folder=Root;object={obj}'.format(safe=safe,obj=obj),
                        '{}o'.format(self.sep), 'PassProps.UserName,Password,PassProps.Address,PassProps.Port,PasswordChangeInProcess'
                    ],
                    stdout=PIPE,
                    stderr=PIPE
                ).communicate()

                if err:
                    raise Exception(err.decode('UTF-8').strip())
            except:
                print(err.decode('UTF-8').strip())
                exit()
            else:
                key_list = ['Username','Password','Address','Port','PasswordChangeInProcess']
                val_list = response.decode('UTF-8').strip().split(',')
                zip_list = zip(key_list,val_list)
                ret_response = dict(zip_list)
                return ret_response