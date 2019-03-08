import os
from sys import platform

import pyaim.config as cfg


class clipasswordsdk:

    def __init__(self):

        wincli = cfg.BaseConfig.WIN_CLIPASSWORDSDK
        nixcli = cfg.BaseConfig.NIX_CLIPASSWORDSDK
        
        # Check for Linux OS
        if platform == 'linux' or platform == 'linux2':
            if os.path.isfile(self.nixcli):
                self.cli = nixcli
            else:
                raise Exception('CLIPasswordSDK not found in default location', 'Please update NIX_CLIPASSWORDSDK value in pyaim/config.py.')
        # Check for Windows OS
        elif platform == 'win32':
            if os.path.isfile(self.wincli):
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
    def GetPassword(self, appID=None):
        pass