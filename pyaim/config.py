from pathlib import Path


class BaseConfig:
    """ Base Configuration """
    WIN_CLIPASSWORDSDK = Path('C:/Windows/Program Files (x86)/CyberArk/ApplicationPasswordSdk/CLIPasswordSDK.exe')
    NIX_CLIPASSWORDSDK = Path('/opt/carkaim/sdk/CLIPasswordSDK')