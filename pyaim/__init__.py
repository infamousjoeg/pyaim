import os
import time
from sys import platform

import pyaim.config as cfg
from sarge import capture_stdout, shell_format


class clipasswordsdk:

    def __init__(self):

        wincli = cfg.BaseConfig.WIN_CLIPASSWORDSDK
        nixcli = cfg.BaseConfig.NIX_CLIPASSWORDSDK
        
        # Check for Linux OS
        if platform == 'linux' or platform == 'linux2':
            if os.path.isfile(nixcli):
                self.cli = nixcli
            else:
                raise Exception('CLIPasswordSDK not found in default location', 'Please update NIX_CLIPASSWORDSDK value in pyaim/config.py.')
        # Check for Windows OS
        elif platform == 'win32':
            if os.path.isfile(wincli):
                self.cli = wincli
            else:
                raise Exception('CLIPasswordSDK.exe not found in default location', 'Please update WIN_CLIPASSWORDSDK value in pyaim/config.py.')
        # Check for MacOS
        elif platform == 'darwin':
            raise Exception('Unsupported OS', 'Support only exists for Linux & Windows currently.')
        # Unknown platform returned
        else:
            raise Exception('Cannot detect OS', 'Your platform is unrecognizable. Please use Linux or Windows.')


    @staticmethod
    def GetPassword(self, appid=None, safe=None, obj=None):
        # Check appid is declared
        if appid is None:
            raise Exception('No Application ID', 'Please declare a valid Application ID.')
        elif safe is None:
            raise Exception('No Safe Name', 'Please declare a valid Safe name.')
        elif obj is None:
            raise Exception('No Object Name', 'Please declare a valid Object name.')
        else:
            response = None
            while response is None:
                response = capture_stdout(
                    shell_format('{0} GetPassword -p AppDescs.AppID={1} -p Query="safe={2};Folder=Root;Object={3} -p Reason="Checked out using pyaim" -p FailRequestOnPasswordChange=true -o PassProps.Username, Password, PassProps.Address, PassProps.Port, PasswordChangeInProcess',
                        self.cli,
                        appid,
                        safe,
                        obj
                    )
                )

                if 'APPAP282E' is in response:
                    time.sleep(3)
                    response = None
                else:
                    break

            return response